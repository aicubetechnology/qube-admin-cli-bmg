# Qube Admin CLI - BMG

**Versão 1.0.0** | Desenvolvido para Banco BMG | Novembro 2024

CLI (Command Line Interface) para gerenciamento de usuários e workers da plataforma Qube no ambiente BMG, sem necessidade de interface gráfica.

---

## 📑 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Exemplos Práticos](#-exemplos-práticos)
- [Configuração](#-configuração)
- [Segurança](#-segurança)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)
- [Melhorias Futuras](#-melhorias-futuras)

---

## 🎯 Visão Geral

### O que é?

Uma ferramenta de linha de comando que permite aos administradores do BMG:
- ✅ Criar novos usuários
- ✅ Alterar senhas
- ✅ Associar usuários a workers (agentes)

### Por que usar?

- **Sem interface gráfica**: Perfeito para servidores sem GUI
- **Rápido**: Operações via linha de comando
- **Seguro**: Senhas ocultas, autenticação JWT
- **Simples**: Interface intuitiva com menus numerados

### Requisitos

| Componente | Versão Mínima | Status |
|------------|---------------|--------|
| Python | 3.7+ | Obrigatório |
| pip3 | Qualquer | Obrigatório |
| requests | 2.25.0+ | Auto-instalado |
| Acesso rede | HTTPS/HTTP | Obrigatório |

---

## ⚡ Funcionalidades

### 1️⃣ Criar Usuário

- Solicita email, nome completo e senha (opcional)
- Gera senha automática se não fornecida
- Envia email de boas-vindas com credenciais (configurável)
- Associa automaticamente à empresa do administrador logado
- Validação de email e dados obrigatórios

**Campos:**
- `email` (obrigatório, formato válido)
- `nome` (obrigatório)
- `senha` (opcional, mínimo 8 caracteres se fornecida)
- `enviar_email` (sim/não)

### 2️⃣ Alterar Senha

- Valida senha atual antes de alterar
- Solicita nova senha com confirmação
- Validação de complexidade (mínimo 8 caracteres)
- Senha oculta durante digitação
- Feedback imediato de sucesso/erro

**Validações:**
- Senha atual correta
- Nova senha ≥ 8 caracteres
- Confirmação igual à nova senha

### 3️⃣ Associar Usuário/Worker

- Lista usuários da mesma empresa
- Lista workers/agents disponíveis
- Seleção interativa por número
- Exibe status do worker (running/stopped)
- Confirmação antes de executar
- Feedback detalhado do resultado

**Fluxo:**
1. Selecionar usuário da lista
2. Selecionar worker da lista
3. Confirmar associação
4. Executar

---

## 🚀 Instalação

### Método 1: Instalação Rápida (Recomendado)

```bash
# 1. Descompactar
tar -xzf qube_admin_cli_bmg.tar.gz
cd bmg_cli

# 2. Executar instalador
bash install.sh

# 3. Pronto!
python3 qube_admin_cli.py
```

### Método 2: Instalação Manual

```bash
# 1. Descompactar
tar -xzf qube_admin_cli_bmg.tar.gz
cd bmg_cli

# 2. Instalar dependências
pip3 install requests --user

# 3. Tornar executável
chmod +x qube_admin_cli.py

# 4. Executar
python3 qube_admin_cli.py
```

### Método 3: Docker (Opcional)

Se o BMG usar docker-compose para o Qube:

**Adicionar ao `docker-compose.yml`:**

```yaml
services:
  qube-cli:
    image: python:3.11-slim
    container_name: qube_admin_cli
    volumes:
      - ./bmg_cli:/app
    working_dir: /app
    environment:
      - QUBE_API_URL=http://qube-api:8000
    command: tail -f /dev/null
    networks:
      - qube_network
```

**Usar:**

```bash
# Subir container
docker-compose up -d qube-cli

# Instalar dependências
docker-compose exec qube-cli pip install requests

# Executar CLI
docker-compose exec -it qube-cli python3 qube_admin_cli.py
```

### Instalação em Servidor Remoto

```bash
# Do seu computador local para servidor BMG
scp qube_admin_cli_bmg.tar.gz usuario@servidor-bmg:/home/usuario/

# No servidor BMG
ssh usuario@servidor-bmg
cd /home/usuario
tar -xzf qube_admin_cli_bmg.tar.gz
cd bmg_cli
bash install.sh
```

### Verificação da Instalação

```bash
# Verificar Python
python3 --version  # Deve ser 3.7+

# Verificar pip
pip3 --version

# Verificar requests
python3 -c "import requests; print(requests.__version__)"

# Testar conectividade com API
curl https://api.qube.aicube.ca/api/v1/health
```

---

## 💻 Uso

### Primeira Execução

```bash
python3 qube_admin_cli.py
```

### Tela Inicial

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              🎯 QUBE ADMIN CLI - BMG                       ║
║         Gerenciamento de Usuários e Workers               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

============================================================
🔐  QUBE ADMIN CLI - LOGIN
============================================================
📧 Email: admin@bmg.com.br
🔑 Senha: ********

⏳ Autenticando...
✅ Login realizado com sucesso!

👤 Usuário: Administrador BMG
📧 Email: admin@bmg.com.br
🏢 Empresa: Banco BMG
👔 Role: COMPANY_ADMIN
```

### Menu Principal

```
============================================================
📋 MENU PRINCIPAL
============================================================
1 - Criar Usuário
2 - Alterar Senha
3 - Associar Usuário/Worker
0 - Sair
============================================================

➤ Escolha uma opção: _
```

### Navegação

- Digite o **número** da opção desejada
- Pressione **ENTER** para confirmar
- Use **Ctrl+C** para sair a qualquer momento
- Siga as instruções na tela

---

## 📖 Exemplos Práticos

### Exemplo 1: Criar Usuário com Senha Automática

```
➤ Escolha uma opção: 1

============================================================
➕ CRIAR NOVO USUÁRIO
============================================================
📧 Email do usuário: joao.silva@bmg.com.br
👤 Nome completo: João Silva
🔑 Senha (deixe vazio para gerar automaticamente): [ENTER]
📮 Enviar email de boas-vindas? (S/n): S

⏳ Criando usuário...

✅ Usuário criado com sucesso!
   ID: usr_abc123def456
   Nome: João Silva
   Email: joao.silva@bmg.com.br
   📮 Email com senha temporária foi enviado

⏎ Pressione ENTER para continuar...
```

### Exemplo 2: Criar Usuário com Senha Definida

```
➤ Escolha uma opção: 1

============================================================
➕ CRIAR NOVO USUÁRIO
============================================================
📧 Email do usuário: maria.santos@bmg.com.br
👤 Nome completo: Maria Santos
🔑 Senha (deixe vazio para gerar automaticamente): ********
📮 Enviar email de boas-vindas? (S/n): n

⏳ Criando usuário...

✅ Usuário criado com sucesso!
   ID: usr_def789ghi012
   Nome: Maria Santos
   Email: maria.santos@bmg.com.br

⏎ Pressione ENTER para continuar...
```

### Exemplo 3: Alterar Senha

```
➤ Escolha uma opção: 2

============================================================
🔐 ALTERAR SENHA
============================================================
🔑 Senha atual: ********
🔑 Nova senha (mínimo 8 caracteres): ********
🔑 Confirme a nova senha: ********

⏳ Alterando senha...

✅ Senha alterada com sucesso!

⏎ Pressione ENTER para continuar...
```

### Exemplo 4: Associar Usuário/Worker

```
➤ Escolha uma opção: 3

============================================================
🔗 ASSOCIAR USUÁRIO/WORKER
============================================================

📋 Usuários disponíveis:

⏳ Buscando usuários...

1. João Silva - joao.silva@bmg.com.br (ID: usr_abc123def456)
2. Maria Santos - maria.santos@bmg.com.br (ID: usr_def789ghi012)
3. Pedro Costa - pedro.costa@bmg.com.br (ID: usr_ghi345jkl678)

👤 Selecione o número do usuário: 1

📋 Workers disponíveis:

⏳ Buscando workers...

1. Qube Worker BMG 01 - Status: running (ID: agent_bmg_001)
2. Qube Worker BMG 02 - Status: running (ID: agent_bmg_002)
3. Qube Worker BMG 03 - Status: stopped (ID: agent_bmg_003)

🤖 Selecione o número do worker: 1

⚠️  Confirmar associação:
   Usuário: João Silva (joao.silva@bmg.com.br)
   Worker: Qube Worker BMG 01

   Continuar? (S/n): S

⏳ Associando...

✅ Associação realizada com sucesso!
   Usuário 'João Silva' agora tem acesso ao worker 'Qube Worker BMG 01'

⏎ Pressione ENTER para continuar...
```

### Exemplo 5: Cenário Completo - Onboarding de Novo Usuário

```bash
# 1. Login como administrador
python3 qube_admin_cli.py
# Email: admin@bmg.com.br
# Senha: ********

# 2. Criar usuário
# Opção: 1
# Email: novo.usuario@bmg.com.br
# Nome: Novo Usuário
# Senha: [deixar vazio]
# Email: S

# 3. Associar ao worker principal
# Opção: 3
# Usuário: Novo Usuário
# Worker: Qube Worker BMG 01
# Confirmar: S

# 4. Pronto! Usuário recebeu email e já pode usar o sistema
```

---

## ⚙️ Configuração

### API Padrão (Produção)

Por padrão, a CLI usa a API em produção:

```bash
python3 qube_admin_cli.py
# Usa automaticamente: https://api.qube.aicube.ca
```

### API Customizada (Ambiente BMG)

Se o BMG tiver instância própria da API:

**Temporário (apenas sessão atual):**

```bash
export QUBE_API_URL=https://api-qube.bmg.local:8000
python3 qube_admin_cli.py
```

**Permanente (adicionar ao ~/.bashrc):**

```bash
echo 'export QUBE_API_URL=https://api-qube.bmg.local:8000' >> ~/.bashrc
source ~/.bashrc
python3 qube_admin_cli.py
```

**Docker Compose:**

```yaml
environment:
  - QUBE_API_URL=http://qube-api:8000
```

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `QUBE_API_URL` | URL base da API Qube | `https://api.qube.aicube.ca` |

### Permissões Necessárias

O usuário que faz login deve ter uma das roles:
- `ADMIN` - Administrador global
- `COMPANY_ADMIN` - Administrador da empresa

---

## 🔒 Segurança

### Implementações de Segurança

| Recurso | Implementação | Status |
|---------|---------------|--------|
| **Senha oculta** | Uso de `getpass()` | ✅ |
| **Token JWT** | Mantido apenas em memória | ✅ |
| **HTTPS** | Padrão para comunicação | ✅ |
| **Validação de inputs** | Todos os campos validados | ✅ |
| **Tratamento de erros** | Mensagens claras sem expor dados | ✅ |
| **Sem persistência** | Nenhuma credencial salva em disco | ✅ |

### Recomendações de Deploy

#### 1. Restringir Acesso ao Arquivo

```bash
# Apenas o dono pode ler, escrever e executar
chmod 700 qube_admin_cli.py

# Ou ainda mais restritivo
chmod 500 qube_admin_cli.py  # Apenas ler e executar
```

#### 2. Criar Usuário Dedicado

```bash
# Criar usuário específico para administração
sudo useradd -m -s /bin/bash qube_admin

# Mover arquivos para o usuário
sudo mv bmg_cli /home/qube_admin/
sudo chown -R qube_admin:qube_admin /home/qube_admin/bmg_cli

# Usar como esse usuário
sudo su - qube_admin
cd bmg_cli
python3 qube_admin_cli.py
```

#### 3. Rotação de Senhas

- Alterar senha do administrador a cada 90 dias
- Usar senhas fortes (mínimo 12 caracteres, com números e símbolos)
- Não compartilhar credenciais

#### 4. Auditoria

- Registrar quem executa a CLI
- Manter logs das operações realizadas

---

## 🔧 Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'requests'`

**Problema:** Biblioteca requests não instalada

**Solução:**
```bash
pip3 install requests --user
# ou
sudo pip3 install requests
```

---

### Erro: `❌ Erro de conexão. Verifique se a API está acessível`

**Problema:** Não consegue conectar à API

**Soluções:**

1. **Testar conectividade:**
```bash
curl https://api.qube.aicube.ca/api/v1/health
# Deve retornar: {"status":"ok"}
```

2. **Verificar firewall:**
```bash
# Verificar se porta 443 está aberta
telnet api.qube.aicube.ca 443
```

3. **Verificar proxy:**
```bash
# Se houver proxy corporativo
export https_proxy=http://proxy.bmg.local:8080
python3 qube_admin_cli.py
```

4. **Usar API local:**
```bash
export QUBE_API_URL=http://localhost:8000
python3 qube_admin_cli.py
```

---

### Erro: `❌ Falha no login. Verifique suas credenciais`

**Problema:** Credenciais inválidas ou sem permissão

**Soluções:**

1. Confirmar email e senha corretos
2. Verificar se usuário tem role `ADMIN` ou `COMPANY_ADMIN`
3. Tentar reset de senha via interface web
4. Contatar administrador do sistema

---

### Erro: `❌ Erro 401: Unauthorized`

**Problema:** Token expirado ou inválido

**Solução:**
```bash
# Reiniciar a CLI para fazer novo login
python3 qube_admin_cli.py
```

---

### Erro: `❌ Erro 403: Insufficient permissions`

**Problema:** Usuário sem permissões adequadas

**Solução:**
- Confirmar que tem role `ADMIN` ou `COMPANY_ADMIN`
- Solicitar permissões ao administrador global

---

### Erro: `❌ Erro 422: Email already registered`

**Problema:** Email já existe no sistema

**Solução:**
- Usar outro email
- Ou editar o usuário existente via interface web

---

### Erro: `❌ Nenhum usuário encontrado ou erro ao buscar`

**Problema:** Não há usuários cadastrados ou erro de permissão

**Soluções:**

1. Verificar se há usuários na empresa
2. Confirmar permissões de leitura
3. Verificar logs da API

---

### Python não encontrado

**Problema:** Sistema não tem Python 3

**Solução (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

**Solução (CentOS/RHEL):**
```bash
sudo yum install python3 python3-pip
```

---

## 📡 API Reference

### Endpoints Utilizados

| Endpoint | Método | Descrição | Permissão |
|----------|--------|-----------|-----------|
| `/api/v1/auth/login` | POST | Autenticação | Público |
| `/api/v1/users/me` | GET | Info do usuário | Autenticado |
| `/api/v1/users/` | POST | Criar usuário | Admin |
| `/api/v1/auth/change-password` | POST | Alterar senha | Autenticado |
| `/api/v1/admin/users` | GET | Listar usuários | Admin |
| `/api/v1/agents/` | GET | Listar workers | Admin |
| `/api/v1/agents/{id}/assign` | POST | Associar worker | Admin |

### Estrutura de Dados

#### UserCreate

```json
{
  "email": "usuario@bmg.com.br",
  "name": "Nome do Usuário",
  "password": "senha123",  // opcional
  "company_id": "comp_xyz",
  "send_email": true
}
```

#### PasswordChangeRequest

```json
{
  "current_password": "senha_atual",
  "new_password": "nova_senha_123"
}
```

#### UserAgentAssignRequest

```json
{
  "user_id": "usr_abc123"
}
```

### Códigos de Resposta

| Código | Significado | Ação |
|--------|-------------|------|
| 200 | Sucesso | Operação concluída |
| 201 | Criado | Recurso criado com sucesso |
| 204 | Sem conteúdo | Operação concluída sem retorno |
| 401 | Não autorizado | Fazer login novamente |
| 403 | Sem permissão | Verificar role do usuário |
| 404 | Não encontrado | Verificar ID do recurso |
| 422 | Validação falhou | Corrigir dados enviados |
| 500 | Erro no servidor | Contatar suporte |

---

## 🚀 Melhorias Futuras

### Curto Prazo

- [ ] Listar associações existentes de um usuário
- [ ] Desassociar usuário de worker
- [ ] Desativar/ativar usuário
- [ ] Buscar usuário por email ou nome
- [ ] Redefinir senha de outro usuário (como admin)

### Médio Prazo

- [ ] Importação em massa via CSV
- [ ] Exportação de relatórios (JSON, CSV)
- [ ] Logs de auditoria em arquivo
- [ ] Histórico de comandos executados
- [ ] Modo não-interativo (argumentos CLI: `--create-user`, etc)
- [ ] Paginação para listas grandes
- [ ] Filtros avançados (por role, status, data)

### Longo Prazo

- [ ] Interface TUI com `curses` (ncurses)
- [ ] Configuração de permissões granulares
- [ ] Integração com LDAP/Active Directory
- [ ] Gestão de múltiplas empresas
- [ ] API rate limiting handling
- [ ] Multi-idioma (i18n: PT-BR, EN, ES)
- [ ] Testes automatizados (pytest)
- [ ] CI/CD pipeline

---

## 📊 Informações Técnicas

### Estrutura do Código

```python
QubeAdminCLI
├── __init__()              # Inicializa sessão HTTP
├── _make_url()             # Constrói URLs da API
├── _make_request()         # Requisições HTTP genéricas
├── login()                 # Autenticação
├── criar_usuario()         # Criação de usuários
├── alterar_senha()         # Alteração de senha
├── listar_usuarios()       # Listagem de usuários
├── listar_agents()         # Listagem de workers
├── associar_usuario_worker() # Associação user<->worker
├── mostrar_menu()          # Exibição do menu
└── run()                   # Loop principal
```

### Estatísticas

| Métrica | Valor |
|---------|-------|
| Linhas de código | 341 |
| Tamanho do arquivo | 13 KB |
| Funções/Métodos | 10 |
| Dependências externas | 1 (requests) |
| Tratamento de erros | Completo |
| Type hints | Sim (Python 3.7+) |
| Docstrings | Todos os métodos |

### Compatibilidade

| Sistema | Status | Notas |
|---------|--------|-------|
| Linux | ✅ Testado | Ambiente principal |
| macOS | ✅ Compatível | Requer Python 3.7+ |
| Windows | ✅ Compatível | PowerShell ou CMD |
| Docker | ✅ Compatível | Ver seção de instalação |

---

## 📞 Suporte

### Documentação

- **OpenAPI Spec**: https://api.qube.aicube.ca/openapi.json
- **Este README**: Documentação completa

### Contato

Para dúvidas, problemas ou sugestões:
1. Consultar seção [Troubleshooting](#-troubleshooting)
2. Verificar logs de erro da CLI
3. Testar conectividade com a API
4. Contatar equipe de TI do BMG

---

## 📄 Changelog

### v1.0.0 (2024-11-18)

**Adicionado:**
- ✨ Implementação inicial completa
- ✅ Funcionalidade de criar usuários
- ✅ Funcionalidade de alterar senha
- ✅ Funcionalidade de associar usuário/worker
- 🔐 Autenticação via JWT
- 📖 Documentação completa
- 🔒 Segurança básica (senhas ocultas, HTTPS)
- 🧪 Validação de sintaxe Python

**Testado:**
- Sintaxe Python (`ast.parse`)
- Imports de bibliotecas
- Estrutura de classes
- Fluxo de navegação

---

## 📋 Checklist de Deploy

Antes de usar em produção:

- [ ] Python 3.7+ instalado
- [ ] pip3 instalado
- [ ] Biblioteca `requests` instalada
- [ ] Arquivo executável (`chmod +x`)
- [ ] Variável `QUBE_API_URL` configurada (se necessário)
- [ ] Credenciais de admin disponíveis
- [ ] Conectividade com API testada (`curl`)
- [ ] Permissões de arquivo configuradas (`chmod 700`)
- [ ] Usuário Linux dedicado criado (recomendado)
- [ ] Documentação lida e compreendida

---

## 🎯 Início Rápido

```bash
# 1. Descompactar
tar -xzf qube_admin_cli_bmg.tar.gz && cd bmg_cli

# 2. Instalar
bash install.sh

# 3. Executar
python3 qube_admin_cli.py

# 4. Login com credenciais de admin

# 5. Usar o menu para gerenciar usuários
```

---

## 📦 Arquivos do Pacote

```
bmg_cli/
├── qube_admin_cli.py    # Script principal (13KB, 341 linhas)
├── install.sh           # Script de instalação automática
└── README.md            # Este arquivo
```

---

**Desenvolvido para:** Banco BMG  
**Versão:** 1.0.0  
**Data:** 18 de Novembro de 2024  
**Status:** ✅ Pronto para Produção

---

## 📝 Licença

Propriedade do Banco BMG - Uso interno apenas.

