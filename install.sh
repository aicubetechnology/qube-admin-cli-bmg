#!/bin/bash
# Script de instalação do Qube Admin CLI

echo "🚀 Instalando Qube Admin CLI..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.7+"
    exit 1
fi

echo "✅ Python $(python3 --version) encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    sudo apt-get update && sudo apt-get install -y python3-pip
fi

echo "✅ pip3 encontrado"

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install requests --user

# Tornar executável
chmod +x qube_admin_cli.py

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Para executar:"
echo "  python3 qube_admin_cli.py"
echo ""
echo "ou"
echo ""
echo "  ./qube_admin_cli.py"
echo ""
