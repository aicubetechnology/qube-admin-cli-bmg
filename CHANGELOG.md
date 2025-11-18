# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
