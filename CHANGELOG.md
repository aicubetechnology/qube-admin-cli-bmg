# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.4.0] - 2025-11-14

### Adicionado
- **Modo debug completo (`QUBE_CLI_DEBUG`)**
  - Exibe URL completa das requisições
  - Mostra método HTTP utilizado (GET, POST, PUT, DELETE)
  - Exibe parâmetros enviados (query string ou body)
  - Mostra status code das respostas (200, 401, 404, etc.)
  - Exibe estrutura do JSON retornado pela API
  - Informações detalhadas em tempo real no console

- **Suporte a múltiplos formatos de resposta da API**
  - Lista direta de usuários (formato atual da API)
  - Dicionário com chave "users" (formato legacy)
  - Dicionário com chave "data" (formato alternativo)

- **Variável de ambiente `API_HOST`**
  - Prioridade sobre `QUBE_API_URL` (mantida para compatibilidade)
  - Suporte a múltiplos ambientes:
    - `http://localhost:8080` - Desenvolvimento local
    - `https://api.qube.aicube.ca` - Produção
    - `https://api.qilbee.io` - Ambiente alternativo
  - API em uso é exibida no cabeçalho da CLI

- **QUICK_START.md**
  - Guia rápido de instalação
  - Exemplos de configuração de ambiente
  - Seção de resolução de problemas

### Corrigido
- **Listagem de usuários retornando vazia**
  - API retorna lista direta, não dicionário com chave "users"
  - Método `listar_usuarios()` agora aceita múltiplos formatos
  - Método `_make_request()` agora usa parâmetro `params` para GET requests
  - 65 usuários listados com sucesso após correção

- **Sanitização de inputs com caracteres ANSI**
  - Remove sequências de escape ANSI de todos os inputs
  - Limpa caracteres de controle do terminal
  - Previne problemas com validação de email e outros campos

### Melhorado
- **UX na criação de usuários**
  - Email de boas-vindas enviado automaticamente quando senha é gerada
  - Pergunta sobre email apenas quando senha é fornecida manualmente
  - Mensagem informativa: "📮 Email de boas-vindas será enviado automaticamente com a senha gerada."
  - Reduz passos desnecessários e evita erro de não enviar senha gerada

- **Debug e troubleshooting**
  - Modo debug muito mais verboso e útil
  - Logs detalhados de requisições e respostas
  - Facilita identificação de problemas de integração com API

## [1.3.0] - 2024-11-18

### Adicionado
- **Sistema completo de logging** com saída configurável
  - Logging de todas as requisições HTTP e respostas
  - Logging de operações de login, criação de usuário, alteração de senha
  - Logging de erros de conexão e validação
  - Logging de exceções com stack trace completo
  - Rotação diária de logs automática

- **Variáveis de ambiente para controle de logs**:
  - `QUBE_CLI_LOG_FILE`: Caminho completo customizado para arquivo de log
  - `QUBE_CLI_LOG_DIR`: Diretório customizado para logs (padrão: ~/.qube_cli/logs)
  - `QUBE_CLI_LOG_LEVEL`: Nível de log (DEBUG, INFO, WARNING, ERROR)
  - `QUBE_CLI_DISABLE_LOGS`: Desabilitar logs em arquivo completamente
  - `QUBE_CLI_DEBUG`: Exibir logs também no console (stdout)

### Melhorado
- CLI agora exibe o caminho do arquivo de log no cabeçalho
- Mensagem "Logs: Desabilitados" quando logs estão desabilitados
- Documentação completa de configuração de logs no README
- .gitignore atualizado para excluir arquivos de log

## [1.2.0] - 2024-11-18

### Melhorado
- **Tratamento de erros robusto** em toda a aplicação
  - Suporte completo para Ctrl+C (KeyboardInterrupt) em todos os inputs
  - Tratamento de EOF em todas as entradas do usuário
  - Validação de campos vazios antes de processar
  - Mensagens de erro mais claras e acionáveis

- **Mensagens HTTP aprimoradas** por código de status:
  - 401: Não autorizado - com dicas de credenciais
  - 403: Acesso negado - com dicas de permissões
  - 404: Não encontrado - com verificação de endpoint
  - 422: Dados inválidos - com detalhes de validação por campo
  - 500: Erro interno - com sugestão de contato ao suporte

- **Tratamento de requisições HTTP**:
  - Timeout de 30 segundos em todas as requisições
  - Tratamento de erros de JSON malformado
  - Tratamento de erro de conexão com dicas de troubleshooting
  - Tratamento de RequestException genérica

- **Validações de entrada**:
  - Email não vazio no login e criação de usuário
  - Nome completo obrigatório
  - Senha não vazia
  - Company ID obrigatório (quando necessário)
  - Validação de entrada numérica com mensagens amigáveis

- **Tratamento global de exceções** na função main()

### Adicionado
- Indicadores emoji claros para diferentes tipos de mensagem
- Dicas acionáveis (💡 Dica:) em todas as mensagens de erro
- Suporte para cancelamento gracioso de operações

## [1.1.0] - 2024-11-18

### Adicionado
- Suporte para variável de ambiente `API_HOST`
- Exibição da URL da API no cabeçalho inicial
- Documentação de exemplos para diferentes ambientes
- Prioridade de variáveis: API_HOST > QUBE_API_URL > default

### Melhorado
- README atualizado com exemplos de uso para:
  - Ambiente local (localhost:8080)
  - Ambiente de produção (api.qube.aicube.ca)
  - Ambiente alternativo (api.qilbee.io)
- Compatibilidade retroativa com QUBE_API_URL

## [1.0.0] - 2024-11-18

### Adicionado
- CLI interativa para gerenciamento de usuários e workers
- Autenticação JWT com API Qube
- Funcionalidade de criação de usuários
- Funcionalidade de alteração de senha
- Funcionalidade de associação usuário/worker
- Script de instalação automatizado
- Script de testes
- Documentação completa no README
- Suporte para ambientes sem GUI
