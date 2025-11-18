# 🚀 Quick Start - Qube Admin CLI

## Instalação Rápida

```bash
# 1. Extrair o arquivo
tar -xzf qube_admin_cli_vX.X.X.tar.gz
cd bmg_cli

# 2. Executar
python3 qube_admin_cli.py
```

## Configuração de Ambiente

### Ambientes Disponíveis

```bash
# Produção (padrão)
python3 qube_admin_cli.py

# Desenvolvimento Local
API_HOST=http://localhost:8080 python3 qube_admin_cli.py

# Qilbee
API_HOST=https://api.qilbee.io python3 qube_admin_cli.py
```

### Modo Debug

```bash
# Ativar debug detalhado
QUBE_CLI_DEBUG=true python3 qube_admin_cli.py
```

O modo debug mostra:
- 🔍 URL completa da requisição
- 🔍 Método HTTP (GET, POST, PUT, DELETE)
- 🔍 Parâmetros enviados
- 🔍 Status code da resposta
- 🔍 Estrutura do JSON retornado

## Funcionalidades

### 1️⃣ Criar Usuário
- Cria novos usuários no sistema
- Define email, nome, senha e role
- Valida permissões antes de criar

### 2️⃣ Alterar Senha
- Altera senha de qualquer usuário (requer permissões)
- Valida formato da senha
- Confirma alteração

### 3️⃣ Associar Usuário/Worker
- Lista todos os usuários disponíveis
- Lista todos os workers disponíveis
- Associa usuário a worker específico

### 0️⃣ Sair
- Logout seguro
- Limpa token de autenticação

## Logs

Logs são salvos em:
```
~/.qube_cli/logs/qube_cli_YYYYMMDD.log
```

### Desabilitar Logs

```bash
QUBE_CLI_DISABLE_LOGS=true python3 qube_admin_cli.py
```

### Alterar Nível de Log

```bash
QUBE_CLI_LOG_LEVEL=DEBUG python3 qube_admin_cli.py
```

Níveis disponíveis: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Resolução de Problemas

### Usuários não aparecem

1. Verifique se você tem permissões (ADMIN ou COMPANY_ADMIN)
2. Ative o modo debug: `QUBE_CLI_DEBUG=true`
3. Verifique os logs em `~/.qube_cli/logs/`
4. Confirme que a API está acessível

### Erro de conexão

1. Verifique a URL da API exibida no cabeçalho
2. Teste conectividade: `curl -I <API_URL>`
3. Verifique firewall/proxy

### Token inválido

1. Faça logout (opção 0)
2. Faça login novamente
3. Se persistir, limpe os logs e tente novamente

## Exemplo de Uso Completo

```bash
# 1. Configurar ambiente de desenvolvimento local
export API_HOST=http://localhost:8080

# 2. Ativar debug para ver detalhes
export QUBE_CLI_DEBUG=true

# 3. Executar
python3 qube_admin_cli.py

# 4. Login com suas credenciais
# Email: seu@email.com
# Senha: ********

# 5. Escolher opção do menu
# 1 - Criar Usuário
# 2 - Alterar Senha
# 3 - Associar Usuário/Worker
# 0 - Sair
```

## Suporte

Para mais informações, consulte o README.md completo.

**Repositório:** https://github.com/aicubetechnology/qube-admin-cli-bmg
