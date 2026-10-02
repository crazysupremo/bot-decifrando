"""
Cliente de Teste - Exemplos de Integração com a API Bot Decifrando
"""

import requests
import json
from typing import Dict, List

class ClienteDecifrando:
    """Cliente para interagir com a API Bot Decifrando"""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    def health_check(self) -> bool:
        """Verifica se a API está online"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

    def desembaralha(self, palavra: str, idioma: str = "pt") -> List[str]:
        """Desembaralha uma palavra"""
        try:
            response = requests.post(
                f"{self.base_url}/desembaralha",
                json={"palavra": palavra, "idioma": idioma}
            )
            dados = response.json()
            return dados.get("soluções", [])
        except Exception as e:
            print(f"Erro: {e}")
            return []

    def resolver_math(self, expressao: str) -> str:
        """Resolve uma expressão matemática"""
        try:
            response = requests.post(
                f"{self.base_url}/math",
                json={"expressao": expressao}
            )
            dados = response.json()
            return dados.get("resultado", "Erro")
        except Exception as e:
            print(f"Erro: {e}")
            return "Erro"

    def auto(self, texto: str, idioma: str = "pt") -> Dict:
        """Detecta automaticamente o tipo de entrada"""
        try:
            response = requests.post(
                f"{self.base_url}/auto",
                json={"texto": texto, "idioma": idioma}
            )
            return response.json()
        except Exception as e:
            print(f"Erro: {e}")
            return {}

    def batch(self, requisicoes: List[Dict], idioma: str = "pt") -> List[Dict]:
        """Processa múltiplas requisições em lote"""
        try:
            response = requests.post(
                f"{self.base_url}/batch",
                json={"requisicoes": requisicoes, "idioma": idioma}
            )
            dados = response.json()
            return dados.get("resultados", [])
        except Exception as e:
            print(f"Erro: {e}")
            return []

    def get_logs(self, limite: int = 50) -> List[Dict]:
        """Obtém o histórico de requisições"""
        try:
            response = requests.get(f"{self.base_url}/logs?limite={limite}")
            dados = response.json()
            return dados.get("logs", [])
        except Exception as e:
            print(f"Erro: {e}")
            return []

    def get_stats(self) -> Dict:
        """Obtém estatísticas de uso"""
        try:
            response = requests.get(f"{self.base_url}/stats")
            return response.json()
        except Exception as e:
            print(f"Erro: {e}")
            return {}


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

def exemplo_basico():
    """Exemplo básico de uso"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Uso Básico")
    print("="*70)

    cliente = ClienteDecifrando()

    # Verifica conexão
    if not cliente.health_check():
        print("❌ API não está disponível!")
        print("💡 Execute: python bot_api_webhook.py")
        return

    print("✅ API conectada!")

    # Desembaralha palavra
    print("\n🔤 Desembaraçando: OTEPMOC")
    soluções = cliente.desembaralha("OTEPMOC", idioma="pt")
    print(f"✅ Soluções: {soluções}")

    # Resolve matemática
    print("\n🧮 Resolvendo: 2+2")
    resultado = cliente.resolver_math("2+2")
    print(f"✅ Resultado: {resultado}")

    # Espanhol
    print("\n🔤 Desembaraçando em espanhol: JEGUOJ")
    soluções_es = cliente.desembaralha("JEGUOJ", idioma="es")
    print(f"✅ Soluções: {soluções_es}")


def exemplo_jogo_evento():
    """Exemplo simulando um jogo/evento que manda palavras e questões"""
    print("\n" + "="*70)
    print("EXEMPLO 2: Simulando Jogo/Evento")
    print("="*70)

    cliente = ClienteDecifrando()

    if not cliente.health_check():
        print("❌ API não está disponível!")
        return

    # Simula questões do jogo
    questoes = [
        {"tipo": "evento", "id": 1, "texto": "Desembaralhe: OTEPMOC"},
        {"tipo": "evento", "id": 2, "texto": "Quanto é: (10*5)+20"},
        {"tipo": "evento", "id": 3, "texto": "Desembaralhe: ERUTURCAETXUS"},
    ]

    print("\n📋 Questões do Jogo:")
    for q in questoes:
        print(f"\n  {q['id']}. {q['texto']}")

    # Processa automaticamente
    print("\n🤖 Processando automaticamente...")

    requisicoes_batch = [
        {"tipo": "desembaralha", "palavra": "OTEPMOC"},
        {"tipo": "math", "expressao": "(10*5)+20"},
        {"tipo": "desembaralha", "palavra": "ERUTURCAETXUS"},
    ]

    resultados = cliente.batch(requisicoes_batch, idioma="pt")

    print("\n✅ Respostas:")
    for i, resultado in enumerate(resultados, 1):
        print(f"\n  {i}. {resultado}")


def exemplo_tempo_real():
    """Exemplo de processamento em tempo real"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Processamento em Tempo Real (Modo Interativo)")
    print("="*70)

    cliente = ClienteDecifrando()

    if not cliente.health_check():
        print("❌ API não está disponível!")
        return

    print("\n💡 Digite 'sair' para finalizar")
    print("   Formatos:")
    print("   - Palavra embaralhada: OTEPMOC")
    print("   - Expressão: 2+2, (10*5)+20")
    print("   - Com idioma: JEGUOJ --es")

    while True:
        entrada = input("\n> Digite a entrada: ").strip()

        if entrada.lower() == "sair":
            print("👋 Até logo!")
            break

        # Detecta idioma
        idioma = "es" if "--es" in entrada else "pt"
        entrada = entrada.replace("--es", "").strip()

        # Processa automaticamente
        resultado = cliente.auto(entrada, idioma)

        print(f"✅ Tipo: {resultado.get('tipo')}")
        print(f"   Resultado: {resultado.get('resultado')}")


def exemplo_estatisticas():
    """Exemplo de monitoramento e estatísticas"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Estatísticas e Monitoramento")
    print("="*70)

    cliente = ClienteDecifrando()

    if not cliente.health_check():
        print("❌ API não está disponível!")
        return

    # Processa algumas requisições
    print("\n📊 Processando requisições para gerar estatísticas...")
    cliente.desembaralha("OTEPMOC")
    cliente.resolver_math("10+20")
    cliente.desembaralha("AMARGORP")
    cliente.resolver_math("100/5")

    # Mostra estatísticas
    stats = cliente.get_stats()
    print("\n📈 Estatísticas:")
    print(f"   Total de requisições: {stats.get('total_requisicoes')}")
    print(f"   Palavras desembaraçadas: {stats.get('palavras_desembaraçadas')}")
    print(f"   Expressões matemáticas: {stats.get('expressoes_matematicas')}")

    # Mostra últimos logs
    logs = cliente.get_logs(limite=5)
    print(f"\n📝 Últimas 5 requisições:")
    for i, log in enumerate(logs[-5:], 1):
        print(f"   {i}. {log.get('tipo')}: {log.get('entrada', 'N/A')}")


def exemplo_integracao_game():
    """Exemplo de como integrar com um jogo real"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Integração com Jogo (Exemplo de Código)")
    print("="*70)

    codigo_exemplo = '''
from cliente_teste import ClienteDecifrando

class Jogo:
    def __init__(self):
        self.bot = ClienteDecifrando()
        self.pontos = 0

    def processar_desafio(self, tipo, conteudo):
        """Processa um desafio do jogo"""

        if tipo == "embaralhar":
            soluções = self.bot.desembaralha(conteudo)
            if soluções:
                print(f"Resposta: {soluções[0]}")
                self.pontos += 10
                return True

        elif tipo == "matematica":
            resultado = self.bot.resolver_math(conteudo)
            print(f"Resultado: {resultado}")
            self.pontos += 5
            return True

        return False

    def jogar(self):
        """Loop principal do jogo"""
        desafios = [
            ("embaralhar", "OTEPMOC"),
            ("matematica", "50+50"),
            ("embaralhar", "ERUTURCAETXUS"),
        ]

        for tipo, conteudo in desafios:
            print(f"Desafio: {conteudo}")
            self.processar_desafio(tipo, conteudo)
            print(f"Pontos: {self.pontos}\\n")

# Usar
jogo = Jogo()
jogo.jogar()
    '''

    print(codigo_exemplo)


def menu_principal():
    """Menu interativo"""
    while True:
        print("\n" + "="*70)
        print("🎮 CLIENTE BOT DECIFRANDO - EXEMPLOS")
        print("="*70)
        print("\n1. Exemplo Básico")
        print("2. Simulando Jogo/Evento")
        print("3. Modo Interativo (Tempo Real)")
        print("4. Estatísticas e Monitoramento")
        print("5. Exemplo de Integração com Game")
        print("6. Sair")

        escolha = input("\nEscolha uma opção (1-6): ").strip()

        if escolha == "1":
            exemplo_basico()
        elif escolha == "2":
            exemplo_jogo_evento()
        elif escolha == "3":
            exemplo_tempo_real()
        elif escolha == "4":
            exemplo_estatisticas()
        elif escolha == "5":
            exemplo_integracao_game()
        elif escolha == "6":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    menu_principal()
