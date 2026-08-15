# Configuração do GitHub

## Passo 1: Criar repositório no GitHub
1. Acesse https://github.com/new
2. Entre com sua conta (ou crie uma se não tiver)
3. Preenchea os campos:
   - **Repository name**: `ml-site` (ou outro nome que preferir)
   - **Description**: Descrição do projeto
   - **Visibility**: Public ou Private
4. Clique em "Create repository"

## Passo 2: Configurar Git (primeira vez apenas)
Se nunca configurou Git antes, execute:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

## Passo 3: Conectar com GitHub

### Opção A: Usando HTTPS (mais simples)
Após criar o repositório no GitHub, você verá um comando como este:
```bash
git remote add origin https://github.com/seu-usuario/ml-site.git
git branch -M main
git push -u origin main
```

### Opção B: Usando SSH (mais seguro)
1. Gere uma chave SSH (se não tiver):
```bash
ssh-keygen -t ed25519 -C "seu.email@example.com"
```
2. Adicione a chave pública ao GitHub (Settings > SSH and GPG keys)
3. Use o comando SSH do GitHub:
```bash
git remote add origin git@github.com:seu-usuario/ml-site.git
git branch -M main
git push -u origin main
```

## Passo 4: Fazer Push

No seu terminal, execute:
```bash
cd /Users/juca-proads/Desktop/ML/site
git remote add origin https://github.com/seu-usuario/ml-site.git
git branch -M main
git push -u origin main
```

## Próximas edições

Depois que tudo estiver no GitHub, para fazer edições:
1. Faça as alterações nos arquivos
2. Execute:
```bash
git add .
git commit -m "Descrição da mudança"
git push
```

## Clonar em outro lugar

Para clonar o projeto em outro lugar:
```bash
git clone https://github.com/seu-usuario/ml-site.git
```
