<?php
$productName = $_GET['product'] ?? 'JBL Boombox 3';
$price = 6779;
$formattedPrice = 'R$ ' . number_format($price / 100, 2, ',', '.');
$initialName = $_GET['name'] ?? 'JBL Boombox 3';
$successMessage = 'Pedido confirmado. Em breve você receberá o código de pagamento.';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    if ($name !== '' && $email !== '' && $phone !== '') {
        $successMessage = 'Pedido confirmado para ' . htmlspecialchars($name) . '. O pagamento foi registrado com sucesso.';
    }
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Checkout | <?php echo htmlspecialchars($productName); ?></title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { font-family: Inter, Arial, sans-serif; background: #f3f4f6; }
    .checkout-shell { max-width: 980px; margin: 0 auto; padding: 24px 16px 60px; }
    .card { background: #fff; border-radius: 18px; box-shadow: 0 8px 22px rgba(0,0,0,.08); }
    .input { width: 100%; border: 1px solid #dfe3e8; border-radius: 12px; padding: 12px 14px; }
  </style>
</head>
<body>
  <div class="checkout-shell">
    <div class="card p-4 md:p-8">
      <div class="mb-6 flex items-center justify-between gap-3 border-b pb-4">
        <div>
          <p class="text-sm uppercase tracking-wide text-green-600 font-bold">Checkout seguro</p>
          <h1 class="text-2xl md:text-3xl font-bold text-slate-800"><?php echo htmlspecialchars($initialName); ?></h1>
        </div>
        <div class="text-right">
          <p class="text-xs text-slate-500">Total</p>
          <p class="text-2xl font-black text-green-600"><?php echo $formattedPrice; ?></p>
        </div>
      </div>

      <?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>
        <div class="rounded-2xl border border-green-200 bg-green-50 p-5 text-green-700 font-medium">
          <?php echo $successMessage; ?>
        </div>
        <div class="mt-6">
          <a href="/loja/produtos/jbl/index.html" class="inline-block rounded-xl bg-slate-800 text-white px-5 py-3 font-bold">Voltar para o produto</a>
        </div>
      <?php else: ?>
        <form method="POST" class="grid grid-cols-1 lg:grid-cols-[1.3fr_0.7fr] gap-6">
          <section class="space-y-5">
            <div>
              <h2 class="text-xl font-bold mb-3">Dados do cliente</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <label class="block">
                  <span class="block text-sm font-medium text-slate-700 mb-1">Nome completo</span>
                  <input class="input" type="text" name="name" value="" placeholder="Seu nome" required />
                </label>
                <label class="block">
                  <span class="block text-sm font-medium text-slate-700 mb-1">Telefone</span>
                  <input class="input" type="tel" name="phone" placeholder="(11) 99999-9999" required />
                </label>
              </div>
            </div>

            <div>
              <h2 class="text-xl font-bold mb-3">Contato</h2>
              <label class="block">
                <span class="block text-sm font-medium text-slate-700 mb-1">E-mail</span>
                <input class="input" type="email" name="email" placeholder="seuemail@email.com" required />
              </label>
            </div>

            <div>
              <h2 class="text-xl font-bold mb-3">Endereço</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <label class="block md:col-span-2">
                  <span class="block text-sm font-medium text-slate-700 mb-1">Rua</span>
                  <input class="input" type="text" name="street" placeholder="Rua das Flores" required />
                </label>
                <label class="block">
                  <span class="block text-sm font-medium text-slate-700 mb-1">Número</span>
                  <input class="input" type="text" name="number" placeholder="123" required />
                </label>
                <label class="block">
                  <span class="block text-sm font-medium text-slate-700 mb-1">CEP</span>
                  <input class="input" type="text" name="zip" placeholder="00000-000" required />
                </label>
              </div>
            </div>
          </section>

          <aside class="space-y-4">
            <div class="rounded-2xl bg-slate-50 border border-slate-200 p-4">
              <p class="text-sm text-slate-500">Produto</p>
              <div class="mt-3 flex items-center gap-3">
                <img src="/loja/produtos/jbl/images/poco_preto.png" alt="JBL Boombox 3" class="w-16 h-16 object-cover rounded-xl border" />
                <div>
                  <p class="font-bold text-slate-800"><?php echo htmlspecialchars($initialName); ?></p>
                  <p class="text-sm text-slate-500">Entrega expressa</p>
                </div>
              </div>
            </div>

            <div class="rounded-2xl bg-slate-50 border border-slate-200 p-4">
              <div class="flex justify-between py-2 text-sm text-slate-600">
                <span>Subtotal</span>
                <span><?php echo $formattedPrice; ?></span>
              </div>
              <div class="flex justify-between py-2 text-sm text-slate-600">
                <span>Frete</span>
                <span>Grátis</span>
              </div>
              <div class="flex justify-between py-3 border-t mt-2 pt-3 text-lg font-bold text-slate-800">
                <span>Total</span>
                <span class="text-green-600"><?php echo $formattedPrice; ?></span>
              </div>
            </div>

            <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white text-lg font-bold py-4 rounded-2xl transition">
              Pagar agora
            </button>
            <p class="text-xs text-center text-slate-500">Pagamento 100% seguro • PIX • cartão • garantia</p>
          </aside>
        </form>
      <?php endif; ?>
    </div>
  </div>
</body>
</html>
