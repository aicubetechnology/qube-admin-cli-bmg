#!/bin/bash
# Script de teste da CLI

echo "=========================================="
echo "🧪 TESTE 1: Verificar se a CLI inicia"
echo "=========================================="
echo ""
echo "Tentando executar com opção de saída (0)..."
echo ""

# Teste 1: Verificar se a CLI inicia e mostra o menu de login
echo "0" | timeout 5 python3 qube_admin_cli.py 2>&1 | head -30

echo ""
echo "=========================================="
echo "🧪 TESTE 2: Verificar estrutura do código"
echo "=========================================="
echo ""
python3 -m py_compile qube_admin_cli.py && echo "✅ Código Python válido (sem erros de sintaxe)" || echo "❌ Erro de sintaxe no código"

echo ""
echo "=========================================="
echo "🧪 TESTE 3: Verificar imports"
echo "=========================================="
echo ""
python3 -c "
import sys
try:
    import requests
    print('✅ requests importado com sucesso')
except ImportError as e:
    print(f'❌ Erro ao importar requests: {e}')
    
try:
    import json
    print('✅ json importado com sucesso')
except ImportError as e:
    print(f'❌ Erro ao importar json: {e}')

try:
    from getpass import getpass
    print('✅ getpass importado com sucesso')
except ImportError as e:
    print(f'❌ Erro ao importar getpass: {e}')
"

echo ""
echo "=========================================="
echo "🧪 TESTE 4: Verificar classe QubeAdminCLI"
echo "=========================================="
echo ""
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')

# Importar sem executar
with open('qube_admin_cli.py', 'r') as f:
    code = f.read()
    
# Verificar presença de componentes essenciais
checks = {
    "Classe QubeAdminCLI": "class QubeAdminCLI" in code,
    "Método login": "def login" in code,
    "Método criar_usuario": "def criar_usuario" in code,
    "Método alterar_senha": "def alterar_senha" in code,
    "Método associar_worker": "def associar_worker" in code or "def associar_usuario_worker" in code,
    "Menu principal": "def menu_principal" in code or "def show_menu" in code,
}

for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check}")
PYEOF

echo ""
echo "=========================================="
echo "✅ TESTES CONCLUÍDOS"
echo "=========================================="
