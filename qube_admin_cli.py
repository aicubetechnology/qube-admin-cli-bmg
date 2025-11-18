#!/usr/bin/env python3
"""
Qube Admin CLI - Ferramenta de administração para o BMG
Permite criar usuários, alterar senhas e associar workers
"""

import requests
import json
import sys
import os
from getpass import getpass
from typing import Optional, Dict, Any

# Configurações da API
# Prioridade: API_HOST > QUBE_API_URL > default
API_BASE_URL = os.getenv("API_HOST", os.getenv("QUBE_API_URL", "https://api.qube.aicube.ca"))
API_VERSION = "v1"


class QubeAdminCLI:
    def __init__(self):
        self.token: Optional[str] = None
        self.user_info: Optional[Dict[str, Any]] = None
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def _make_url(self, endpoint: str) -> str:
        """Constrói a URL completa da API"""
        return f"{API_BASE_URL}/api/{API_VERSION}/{endpoint}"
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                      require_auth: bool = True) -> Optional[Dict]:
        """Faz requisição HTTP para a API"""
        url = self._make_url(endpoint)
        
        if require_auth and self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=data, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=30)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=30)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=30)
            else:
                print(f"❌ Método HTTP inválido: {method}")
                return None
            
            if response.status_code in [200, 201, 204]:
                if response.status_code == 204:
                    return {"success": True}
                try:
                    return response.json() if response.text else {"success": True}
                except json.JSONDecodeError:
                    print(f"⚠️  Resposta da API não está em formato JSON válido")
                    return {"success": True, "raw_response": response.text}
            else:
                # Tratar diferentes tipos de erro
                try:
                    error_data = response.json() if response.text else {}
                except json.JSONDecodeError:
                    error_data = {"detail": response.text or "Erro desconhecido"}
                
                error_detail = error_data.get('detail', error_data.get('message', str(error_data)))
                
                # Mensagens mais amigáveis por código de status
                if response.status_code == 401:
                    print(f"❌ Não autorizado: {error_detail}")
                    print("💡 Dica: Verifique suas credenciais ou faça login novamente")
                elif response.status_code == 403:
                    print(f"❌ Acesso negado: {error_detail}")
                    print("💡 Dica: Você não tem permissão para esta operação")
                elif response.status_code == 404:
                    print(f"❌ Não encontrado: {error_detail}")
                    print(f"💡 Dica: Verifique se o endpoint existe: {url}")
                elif response.status_code == 422:
                    print(f"❌ Dados inválidos: {error_detail}")
                    if isinstance(error_data, dict) and 'detail' in error_data:
                        if isinstance(error_data['detail'], list):
                            print("📋 Detalhes da validação:")
                            for err in error_data['detail']:
                                field = err.get('loc', ['unknown'])[-1]
                                msg = err.get('msg', 'erro desconhecido')
                                print(f"   • {field}: {msg}")
                elif response.status_code == 500:
                    print(f"❌ Erro interno do servidor: {error_detail}")
                    print("💡 Dica: Contate o suporte ou tente novamente mais tarde")
                else:
                    print(f"❌ Erro {response.status_code}: {error_detail}")
                
                return None
                
        except requests.exceptions.ConnectionError as e:
            print(f"\n❌ Erro de conexão com a API")
            print(f"🌐 URL: {API_BASE_URL}")
            print(f"💡 Dica: Verifique se:")
            print(f"   • A API está rodando")
            print(f"   • A URL está correta (use API_HOST para mudar)")
            print(f"   • Você tem acesso à rede")
            return None
        except requests.exceptions.Timeout:
            print(f"\n❌ Timeout na requisição (>30s)")
            print(f"💡 Dica: A API pode estar lenta ou indisponível")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Erro na requisição HTTP: {e}")
            return None
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Operação cancelada pelo usuário")
            raise  # Re-lança para ser tratado no nível superior
        except Exception as e:
            print(f"\n❌ Erro inesperado: {type(e).__name__}: {e}")
            print(f"💡 Dica: Se o problema persistir, reporte este erro")
            return None
    
    def login(self) -> bool:
        """Realiza login do usuário administrador"""
        print("\n" + "="*60)
        print("🔐  QUBE ADMIN CLI - LOGIN")
        print("="*60)
        
        try:
            email = input("📧 Email: ").strip()
            
            if not email:
                print("❌ Email não pode ser vazio")
                return False
            
            password = getpass("🔑 Senha: ")
            
            if not password:
                print("❌ Senha não pode ser vazia")
                return False
            
        except EOFError:
            print("\n\n❌ Entrada cancelada (EOF)")
            return False
        except KeyboardInterrupt:
            print("\n\n⚠️  Login cancelado pelo usuário")
            return False
        
        data = {
            "email": email,
            "password": password
        }
        
        print("\n⏳ Autenticando...")
        
        try:
            response = self._make_request("POST", "auth/login", data, require_auth=False)
            
            if response and "access_token" in response:
                self.token = response["access_token"]
                print("✅ Login realizado com sucesso!\n")
                
                # Buscar informações do usuário
                user_response = self._make_request("GET", "users/me")
                if user_response:
                    self.user_info = user_response
                    print(f"👤 Usuário: {self.user_info.get('name', 'N/A')}")
                    print(f"📧 Email: {self.user_info.get('email', 'N/A')}")
                    print(f"🏢 Empresa: {self.user_info.get('company_name', 'N/A')}")
                    print(f"👔 Role: {self.user_info.get('role', 'N/A')}")
                
                return True
            else:
                print("❌ Falha no login. Verifique suas credenciais.\n")
                return False
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Login cancelado pelo usuário")
            return False
    
    def criar_usuario(self):
        """Cria um novo usuário"""
        print("\n" + "="*60)
        print("➕ CRIAR NOVO USUÁRIO")
        print("="*60)
        
        try:
            email = input("📧 Email do usuário: ").strip()
            if not email:
                print("❌ Email não pode ser vazio")
                return
            
            name = input("👤 Nome completo: ").strip()
            if not name:
                print("❌ Nome não pode ser vazio")
                return
            
            password = getpass("🔑 Senha (deixe vazio para gerar automaticamente): ")
            
            # Usar company_id do usuário logado
            company_id = self.user_info.get("company_id") if self.user_info else None
            
            if not company_id:
                company_id = input("🏢 Company ID: ").strip()
                if not company_id:
                    print("❌ Company ID não pode ser vazio")
                    return
            
            # Perguntar sobre envio de email
            send_email_input = input("📮 Enviar email de boas-vindas? (S/n): ").strip().lower()
            send_email = send_email_input != 'n'
            
        except (EOFError, KeyboardInterrupt):
            print("\n\n⚠️  Operação cancelada")
            return
        
        data = {
            "email": email,
            "name": name,
            "company_id": company_id,
            "send_email": send_email
        }
        
        # Adicionar senha se fornecida
        if password:
            data["password"] = password
        
        print("\n⏳ Criando usuário...")
        response = self._make_request("POST", "users/", data)
        
        if response:
            print("\n✅ Usuário criado com sucesso!")
            print(f"   ID: {response.get('id', 'N/A')}")
            print(f"   Nome: {response.get('name', 'N/A')}")
            print(f"   Email: {response.get('email', 'N/A')}")
            if not password and send_email:
                print("   📮 Email com senha temporária foi enviado")
        else:
            print("\n❌ Falha ao criar usuário")
    
    def alterar_senha(self):
        """Altera a senha do usuário logado"""
        print("\n" + "="*60)
        print("🔐 ALTERAR SENHA")
        print("="*60)
        
        try:
            current_password = getpass("🔑 Senha atual: ")
            if not current_password:
                print("❌ Senha atual não pode ser vazia")
                return
            
            new_password = getpass("🔑 Nova senha (mínimo 8 caracteres): ")
            if not new_password:
                print("❌ Nova senha não pode ser vazia")
                return
            
            confirm_password = getpass("🔑 Confirme a nova senha: ")
            
        except (EOFError, KeyboardInterrupt):
            print("\n\n⚠️  Operação cancelada")
            return
        
        if new_password != confirm_password:
            print("❌ As senhas não coincidem!")
            return
        
        if len(new_password) < 8:
            print("❌ A senha deve ter no mínimo 8 caracteres!")
            return
        
        data = {
            "current_password": current_password,
            "new_password": new_password
        }
        
        print("\n⏳ Alterando senha...")
        response = self._make_request("POST", "auth/change-password", data)
        
        if response:
            print("\n✅ Senha alterada com sucesso!")
        else:
            print("\n❌ Falha ao alterar senha")
    
    def listar_usuarios(self) -> Optional[list]:
        """Lista usuários da empresa"""
        print("\n⏳ Buscando usuários...")
        
        # Filtrar pela company_id do usuário logado
        params = {}
        if self.user_info and self.user_info.get("company_id"):
            params["company_id"] = self.user_info.get("company_id")
        
        response = self._make_request("GET", "admin/users", params)
        
        if response and "users" in response:
            return response["users"]
        return None
    
    def listar_agents(self) -> Optional[list]:
        """Lista workers/agents disponíveis"""
        print("\n⏳ Buscando workers...")
        
        response = self._make_request("GET", "agents/")
        
        if response and isinstance(response, list):
            return response
        elif response and "agents" in response:
            return response["agents"]
        return None
    
    def associar_usuario_worker(self):
        """Associa um worker a um usuário"""
        print("\n" + "="*60)
        print("🔗 ASSOCIAR USUÁRIO/WORKER")
        print("="*60)
        
        # Listar usuários
        print("\n📋 Usuários disponíveis:")
        usuarios = self.listar_usuarios()
        
        if not usuarios:
            print("❌ Nenhum usuário encontrado ou erro ao buscar")
            return
        
        for idx, user in enumerate(usuarios, 1):
            print(f"{idx}. {user.get('name', 'N/A')} - {user.get('email', 'N/A')} (ID: {user.get('id', 'N/A')})")
        
        # Selecionar usuário
        try:
            user_choice = int(input("\n👤 Selecione o número do usuário: ").strip())
            if user_choice < 1 or user_choice > len(usuarios):
                print("❌ Seleção inválida!")
                return
            selected_user = usuarios[user_choice - 1]
        except ValueError:
            print("❌ Entrada inválida! Digite apenas números")
            return
        except (EOFError, KeyboardInterrupt):
            print("\n\n⚠️  Operação cancelada")
            return
        
        # Listar workers
        print("\n📋 Workers disponíveis:")
        agents = self.listar_agents()
        
        if not agents:
            print("❌ Nenhum worker encontrado ou erro ao buscar")
            return
        
        for idx, agent in enumerate(agents, 1):
            status = agent.get('status', 'N/A')
            print(f"{idx}. {agent.get('name', 'N/A')} - Status: {status} (ID: {agent.get('id', 'N/A')})")
        
        # Selecionar worker
        try:
            agent_choice = int(input("\n🤖 Selecione o número do worker: ").strip())
            if agent_choice < 1 or agent_choice > len(agents):
                print("❌ Seleção inválida!")
                return
            selected_agent = agents[agent_choice - 1]
        except ValueError:
            print("❌ Entrada inválida! Digite apenas números")
            return
        except (EOFError, KeyboardInterrupt):
            print("\n\n⚠️  Operação cancelada")
            return
        
        # Confirmar associação
        print(f"\n⚠️  Confirmar associação:")
        print(f"   Usuário: {selected_user.get('name')} ({selected_user.get('email')})")
        print(f"   Worker: {selected_agent.get('name')}")
        
        try:
            confirm = input("\n   Continuar? (S/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n\n⚠️  Operação cancelada")
            return
        
        if confirm == 'n':
            print("❌ Operação cancelada")
            return
        
        # Fazer a associação
        data = {"user_id": selected_user.get('id')}
        agent_id = selected_agent.get('id')
        
        print("\n⏳ Associando...")
        response = self._make_request("POST", f"agents/{agent_id}/assign", data)
        
        if response:
            print("\n✅ Associação realizada com sucesso!")
            print(f"   Usuário '{selected_user.get('name')}' agora tem acesso ao worker '{selected_agent.get('name')}'")
        else:
            print("\n❌ Falha ao associar usuário ao worker")
    
    def mostrar_menu(self):
        """Mostra o menu principal"""
        print("\n" + "="*60)
        print("📋 MENU PRINCIPAL")
        print("="*60)
        print("1 - Criar Usuário")
        print("2 - Alterar Senha")
        print("3 - Associar Usuário/Worker")
        print("0 - Sair")
        print("="*60)
    
    def run(self):
        """Executa o CLI"""
        print("\n")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                                                            ║")
        print("║              🎯 QUBE ADMIN CLI - BMG                       ║")
        print("║         Gerenciamento de Usuários e Workers               ║")
        print("║                                                            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"\n🌐 API: {API_BASE_URL}")
        
        # Login
        if not self.login():
            sys.exit(1)
        
        # Loop do menu
        while True:
            self.mostrar_menu()
            
            try:
                opcao = input("\n➤ Escolha uma opção: ").strip()
                
                if opcao == "1":
                    self.criar_usuario()
                elif opcao == "2":
                    self.alterar_senha()
                elif opcao == "3":
                    self.associar_usuario_worker()
                elif opcao == "0":
                    print("\n👋 Até logo!\n")
                    sys.exit(0)
                else:
                    print("\n❌ Opção inválida! Escolha 1, 2, 3 ou 0")
                
                # Pausa para continuar (com tratamento de erro)
                try:
                    input("\n⏎ Pressione ENTER para continuar...")
                except (EOFError, KeyboardInterrupt):
                    print("\n\n👋 Saindo...\n")
                    sys.exit(0)
                
            except EOFError:
                print("\n\n❌ Entrada cancelada (EOF)")
                print("👋 Saindo...\n")
                sys.exit(0)
            except KeyboardInterrupt:
                print("\n\n👋 Saindo...\n")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Erro inesperado: {type(e).__name__}: {e}")
                print(f"💡 Dica: Se o problema persistir, reporte este erro")
                try:
                    input("\n⏎ Pressione ENTER para continuar...")
                except (EOFError, KeyboardInterrupt):
                    print("\n\n👋 Saindo...\n")
                    sys.exit(0)


def main():
    """Função principal com tratamento de erros global"""
    try:
        cli = QubeAdminCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!\n")
        sys.exit(0)
    except EOFError:
        print("\n\n❌ Entrada cancelada (EOF). Encerrando...\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro fatal não tratado!")
        print(f"❌ {type(e).__name__}: {e}")
        print(f"\n💡 Por favor, reporte este erro ao suporte com os detalhes acima")
        sys.exit(1)


if __name__ == "__main__":
    main()
