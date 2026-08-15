#!/bin/bash

# Script para fazer push do projeto no GitHub
# Use: bash push-to-github.sh <seu-usuario-github> <nome-repo-github>

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: bash push-to-github.sh seu-usuario seu-repo"
    echo "Exemplo: bash push-to-github.sh juca-proads ml-site"
    exit 1
fi

GITHUB_USER=$1
REPO_NAME=$2
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "🚀 Iniciando push para: $REPO_URL"

# Adicionar os arquivos do projeto
echo "📝 Adicionando arquivos..."
git add .

# Fazer commit se houver mudanças
if [ -n "$(git status --porcelain)" ]; then
    echo "💾 Commitando arquivos do projeto..."
    git commit -m "Add project files from ML/site"
fi

# Adicionar remote
echo "🔗 Conectando ao repositório remoto..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# Fazer push
echo "📤 Fazendo push para GitHub..."
git branch -M main
git push -u origin main

echo "✅ Pronto! Seu projeto está no GitHub: $REPO_URL"
