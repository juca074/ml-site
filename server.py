import base64
import html
import hmac
import hashlib
import json
import os
import re
import secrets
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
API_BASE_URL = "https://api.pagflexbr.com/v1"


def json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def save_webhook_event(payload):
    events_dir = ROOT / "data"
    events_dir.mkdir(exist_ok=True)
    with (events_dir / "pagflex-events.jsonl").open("a", encoding="utf-8") as event_file:
        event_file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def product_details(slug):
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", slug or ""):
        raise ValueError("Produto inválido")

    product_file = ROOT / "loja" / "produtos" / slug / "index.html"
    if not product_file.is_file():
        raise ValueError("Produto não encontrado")

    source = product_file.read_text(encoding="utf-8", errors="ignore")
    title_match = re.search(r'class="title"[^>]*>(.*?)</p>', source, re.S | re.I)
    price_match = re.search(r'class="new-price2"[^>]*>(.*?)</span>', source, re.S | re.I)
    if not title_match or not price_match:
        raise ValueError("Dados do produto incompletos")

    title = re.sub(r"<[^>]+>", " ", title_match.group(1))
    title = re.sub(r"\s+", " ", html.unescape(title)).strip()
    price_text = re.sub(r"<[^>]+>", "", price_match.group(1)).strip()
    price_text = re.sub(r"[^0-9,.]", "", price_text).replace(".", "").replace(",", ".")
    amount = int(round(float(price_text) * 100))
    return title, amount


def create_payment(payload):
    api_key = os.environ.get("PAGFLEX_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("PAGFLEX_API_KEY não configurada no servidor")

    slug = str(payload.get("produto", ""))
    product_name, amount = product_details(slug)
    payer = payload.get("payer") or {}
    required = ("name", "email", "phone")
    if any(not str(payer.get(field, "")).strip() for field in required):
        raise ValueError("Nome, e-mail e telefone são obrigatórios")

    order_ref = f"order_{secrets.token_urlsafe(12)}"
    request_payload = {
        "amount": amount,
        "currency": "BRL",
        "method": "PIX",
        "description": product_name[:120],
        "externalRef": order_ref,
        "notificationUrl": os.environ.get("PAGFLEX_NOTIFICATION_URL", ""),
        "payer": {
            "name": str(payer["name"]).strip(),
            "email": str(payer["email"]).strip(),
            "phone": re.sub(r"\D", "", str(payer["phone"])),
        },
        "items": [{"quantity": 1, "name": product_name[:120], "price": amount, "type": "PHYSICAL"}],
        "metadata": {"productSlug": slug, "orderId": order_ref},
    }
    address = payload.get("address") or {}
    if any(str(address.get(field, "")).strip() for field in ("street", "number", "zipCode")):
        request_payload["delivery"] = {
            "fee": 0,
            "address": {
                "country": "BR",
                "street": str(address.get("street", "")).strip(),
                "number": str(address.get("number", "")).strip(),
                "zipCode": str(address.get("zipCode", "")).strip(),
            },
        }
    request_payload = {key: value for key, value in request_payload.items() if value != ""}
    request = urllib.request.Request(
        f"{API_BASE_URL}/payment",
        data=json.dumps(request_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            gateway_response = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            details = json.loads(error.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            details = {"message": "Gateway recusou a criação do pagamento"}
        raise RuntimeError(details.get("message", "Gateway recusou a criação do pagamento")) from error
    except urllib.error.URLError as error:
        raise RuntimeError("Não foi possível conectar ao gateway de pagamento") from error

    payment_data = gateway_response.get("data") or {}
    copypaste = payment_data.get("copypaste")
    if not copypaste:
        raise RuntimeError("Gateway não retornou o código PIX")

    return {
        "id": gateway_response.get("id"),
        "status": gateway_response.get("status"),
        "amount": amount,
        "product": product_name,
        "copypaste": copypaste,
    }


class CheckoutHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/webhooks/pagflex":
            self.handle_webhook()
            return
        if self.path != "/api/payments":
            json_response(self, 404, {"message": "Rota não encontrada"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            json_response(self, 200, create_payment(payload))
        except (ValueError, json.JSONDecodeError) as error:
            json_response(self, 400, {"message": str(error) or "Dados inválidos"})
        except RuntimeError as error:
            json_response(self, 502, {"message": str(error)})

    def handle_webhook(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)
        secret = os.environ.get("PAGFLEX_WEBHOOK_SECRET", "").encode("utf-8")
        signature = self.headers.get("X-Signature", "")
        expected = hmac.new(secret, raw_body, hashlib.sha256).digest()
        received = signature.encode("utf-8")
        if not secret or not hmac.compare_digest(received, base64.b64encode(expected)):
            json_response(self, 401, {"message": "Assinatura inválida"})
            return
        try:
            payload = json.loads(raw_body.decode("utf-8"))
            save_webhook_event(payload)
            json_response(self, 200, {"received": True})
        except (json.JSONDecodeError, UnicodeDecodeError):
            json_response(self, 400, {"message": "Payload inválido"})

    def log_message(self, format_string, *args):
        if self.path.startswith("/api/"):
            super().log_message(format_string, *args)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", port), CheckoutHandler)
    print(f"Preview e checkout em http://127.0.0.1:{port}")
    server.serve_forever()
