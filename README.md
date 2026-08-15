# ML Site - Repositório Git

## Status Atual
✅ Repositório Git inicializado  
✅ Arquivos adicionados  
⏳ Pronto para fazer push no GitHub

## Próximos Passos

### 1️⃣ Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name**: `ml-site`
   - **Description**: Seu projeto ML
   - **Visibility**: Escolha entre Public ou Private
3. Clique em "Create repository"

### 2️⃣ Conectar e Fazer Push
Após criar o repositório, copie e execute UM DOS COMANDOS ABAIXO no terminal:

#### Opção A: HTTPS (mais fácil, mas pede senha toda vez)
```bash
cd /Users/juca-proads/Desktop/ML/site
git remote add origin https://github.com/SEU-USUARIO/ml-site.git
git branch -M main
git push -u origin main
```

#### Opção B: SSH (mais seguro, sem pedir senha)
```bash
cd /Users/juca-proads/Desktop/ML/site
git remote add origin git@github.com:SEU-USUARIO/ml-site.git
git branch -M main
git push -u origin main
```

### 3️⃣ Editar o Projeto
Depois que tudo estiver no GitHub, para fazer mudanças:

```bash
# Faça suas edições nos arquivos...

# Depois execute:
cd /Users/juca-proads/Desktop/ML/site
git add .
git commit -m "Descrição da mudança"
git push
```

### 4️⃣ Ver o Status
```bash
cd /Users/juca-proads/Desktop/ML/site
git status
git log
```

## Dicas
- **GitHub CLI**: Se tiver `gh` instalado, pode usar `gh repo create`
- **VS Code**: Integração Git nativa facilita tudo
- **Clonar em outro lugar**: `git clone https://github.com/SEU-USUARIO/ml-site.git`

---
**Configurar identidade Git** (uma única vez):
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```
