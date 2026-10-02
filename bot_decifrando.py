"""
Bot Decifrando - Desembaraça palavras e resolve questões de matemática
Idiomas: Português e Espanhol
"""

import re
import itertools
from typing import List, Tuple, Dict
import requests
from groq_helper import (
    groq_configurado,
    desembaralhar_com_groq,
    responder_quiz_generico,
    eh_mensagem_quiz,
)


class BotDecifrando:
    def __init__(self):
        # Dicionários de palavras (você pode expandir)
        self.palavras_pt = self._carregar_palavras_pt()
        self.palavras_es = self._carregar_palavras_es()

    def _carregar_palavras_pt(self) -> set:
        """Carrega dicionário português básico"""
        palavras = {
            'python', 'jogo', 'desafio', 'inteligencia', 'artificial', 'linguagem',
            'computador', 'tecnologia', 'internet', 'programa', 'aplicativo', 'sistema',
            'dado', 'informacao', 'rede', 'servidor', 'cliente', 'banco', 'dados',
            'seguranca', 'criptografia', 'algoritmo', 'estrutura', 'funcao', 'classe',
            'objeto', 'instancia', 'variavel', 'constante', 'operador', 'condicao',
            'laco', 'repeticao', 'lista', 'dicionario', 'tupla', 'conjunto',
            'arquivo', 'pasta', 'caminho', 'permissao', 'usuario', 'administrador',
            'palavra', 'texto', 'string', 'numero', 'inteiro', 'decimal', 'booleano',
            'verdadeiro', 'falso', 'nulo', 'vazio', 'cheio', 'completo', 'parcial',
            'inicio', 'fim', 'meio', 'lado', 'canto', 'borda', 'centro', 'ponto',
            'linha', 'coluna', 'matriz', 'tabela', 'grafico', 'imagem', 'som', 'video',
            'tempo', 'espaco', 'velocidade', 'tamanho', 'peso', 'altura', 'largura',
            'profundidade', 'cor', 'forma', 'textura', 'padrao', 'estilo', 'design'
        }
        return palavras

    def _carregar_palavras_es(self) -> set:
        """Carrega dicionário espanhol básico"""
        palavras = {
            'python', 'juego', 'desafio', 'inteligencia', 'artificial', 'lenguaje',
            'computadora', 'tecnologia', 'internet', 'programa', 'aplicacion', 'sistema',
            'dato', 'informacion', 'red', 'servidor', 'cliente', 'banco', 'datos',
            'seguridad', 'criptografia', 'algoritmo', 'estructura', 'funcion', 'clase',
            'objeto', 'instancia', 'variable', 'constante', 'operador', 'condicion',
            'bucle', 'repeticion', 'lista', 'diccionario', 'tupla', 'conjunto',
            'archivo', 'carpeta', 'ruta', 'permiso', 'usuario', 'administrador',
            'palabra', 'texto', 'cadena', 'numero', 'entero', 'decimal', 'booleano',
            'verdadero', 'falso', 'nulo', 'vacio', 'lleno', 'completo', 'parcial',
            'inicio', 'fin', 'medio', 'lado', 'esquina', 'borde', 'centro', 'punto'
        }
        return palavras

    def desembaralhar_palavra(self, palavra_embaralhada: str, idioma: str = 'pt') -> List[str]:
        """
        Desembaralha uma palavra usando combinações

        Args:
            palavra_embaralhada: palavra embaralhada
            idioma: 'pt' para português ou 'es' para espanhol

        Returns:
            Lista de possíveis palavras
        """
        palavra_embaralhada = palavra_embaralhada.lower().strip()
        dicionario = self.palavras_pt if idioma == 'pt' else self.palavras_es

        resultados = []

        # Busca palavras com as mesmas letras
        for palavra in dicionario:
            if len(palavra) == len(palavra_embaralhada):
                if sorted(palavra) == sorted(palavra_embaralhada):
                    resultados.append(palavra)

        # Fallback: dicionário local é pequeno (~70 palavras). Se não achou
        # nada e o Groq está configurado (GROQ_API_KEY no .env), pergunta pro
        # Groq em vez de desistir — item pedido: "coloque o groq pra
        # responder automática no aplicativo".
        if not resultados and groq_configurado():
            resultados = desembaralhar_com_groq(palavra_embaralhada, idioma)

        return resultados if resultados else ["Nenhuma palavra encontrada"]

    def resolver_matematica(self, expressao: str) -> str:
        """
        Resolve expressões matemáticas

        Args:
            expressao: expressão matemática (ex: "2+2", "10/5", "3**2")

        Returns:
            Resultado da operação
        """
        try:
            # Remove espaços
            expressao = expressao.strip()

            # Validação básica de segurança
            caracteres_permitidos = set('0123456789+-*/.()% ')
            if not all(c in caracteres_permitidos for c in expressao):
                return "❌ Expressão inválida! Use apenas: números, +, -, *, /, (, ), %"

            # Avalia a expressão
            resultado = eval(expressao)

            # Formata o resultado
            if isinstance(resultado, float):
                # Remove zeros desnecessários
                resultado = round(resultado, 2)
                if resultado == int(resultado):
                    return str(int(resultado))

            return str(resultado)

        except ZeroDivisionError:
            return "❌ Erro: Divisão por zero!"
        except SyntaxError:
            return "❌ Erro: Expressão matemática inválida!"
        except Exception as e:
            return f"❌ Erro: {str(e)}"

    def processar_entrada(self, texto: str, idioma: str = 'pt') -> Dict[str, str]:
        """
        Processa entrada do usuário e identifica o tipo de comando

        Args:
            texto: entrada do usuário
            idioma: idioma esperado

        Returns:
            Dicionário com tipo e resposta
        """
        texto = texto.lower().strip()

        # Detecta tipo de pergunta
        if any(cmd in texto for cmd in ['desembaralha', 'embaralha', 'palavra', 'decifrá']):
            # É uma palavra embaralhada
            palavras = texto.split()
            for palavra in palavras:
                if len(palavra) > 2 and palavra[0].isalpha():
                    resultado = self.desembaralhar_palavra(palavra, idioma)
                    return {
                        'tipo': 'palavra_embaralhada',
                        'input': palavra,
                        'resultado': resultado
                    }

        # Detecta expressão matemática
        if any(op in texto for op in ['+', '-', '*', '/', '(', ')', '%', '=']):
            # Extrai apenas a expressão matemática
            expressao = re.sub(r'[^0-9+\-*/().% ]', '', texto).strip()
            if expressao:
                resultado = self.resolver_matematica(expressao)
                return {
                    'tipo': 'matematica',
                    'input': expressao,
                    'resultado': resultado
                }

        # Tenta processar como palavra simples
        palavras = texto.split()
        for palavra in palavras:
            if len(palavra) > 2:
                resultado = self.desembaralhar_palavra(palavra, idioma)
                if resultado[0] != "Nenhuma palavra encontrada":
                    return {
                        'tipo': 'palavra_embaralhada',
                        'input': palavra,
                        'resultado': resultado
                    }

        # Último recurso: nada bateu com palavra embaralhada nem matemática,
        # mas se o Groq estiver configurado, tenta responder como se fosse
        # uma pergunta de quiz solta (ex: pergunta de conhecimento geral).
        if groq_configurado():
            resposta_groq = responder_quiz_generico(texto)
            if resposta_groq:
                return {
                    'tipo': 'quiz_groq',
                    'input': texto,
                    'resultado': resposta_groq
                }

        return {
            'tipo': 'desconhecido',
            'input': texto,
            'resultado': "Não entendi. Use: /desembaralha PALAVRA ou /math EXPRESSÃO"
        }

    def formatar_resposta(self, resultado: Dict) -> str:
        """Formata a resposta de forma legível"""
        tipo = resultado['tipo']
        input_text = resultado['input']
        resposta = resultado['resultado']

        if tipo == 'palavra_embaralhada':
            if isinstance(resposta, list):
                resposta_texto = ', '.join(resposta[:5])  # Mostra até 5 opções
                if len(resposta) > 5:
                    resposta_texto += f", e mais {len(resposta)-5}..."
                return f"🔤 **Palavra embaralhada**: {input_text}\n✅ **Possíveis soluções**: {resposta_texto}"
            else:
                return f"🔤 Palavra embaralhada: {input_text}\n❌ {resposta}"

        elif tipo == 'matematica':
            return f"🧮 **Expressão**: {input_text}\n✅ **Resultado**: {resposta}"

        elif tipo == 'quiz_groq':
            return f"🤖 **Groq respondeu**: {resposta}"

        else:
            return f"❓ {resposta}"


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    bot = BotDecifrando()

    print("=" * 60)
    print("BOT DECIFRANDO - Exemplo de Uso")
    print("=" * 60)

    # Teste 1: Desembaralhar palavra em português
    print("\n📝 Teste 1: Desembaralhar palavra (PT)")
    resultado = bot.processar_entrada("desembaralha: OTEPMOC")
    print(bot.formatar_resposta(resultado))

    # Teste 2: Matemática
    print("\n📝 Teste 2: Resolver matemática")
    resultado = bot.processar_entrada("quanto é 25 + 17")
    print(bot.formatar_resposta(resultado))

    # Teste 3: Expressão mais complexa
    print("\n📝 Teste 3: Expressão mais complexa")
    resultado = bot.processar_entrada("(10 * 5) + (20 / 4)")
    print(bot.formatar_resposta(resultado))

    # Teste 4: Palavra em espanhol
    print("\n📝 Teste 4: Desembaralhar palavra (ES)")
    resultado = bot.processar_entrada("JEGUOJ", idioma='es')
    print(bot.formatar_resposta(resultado))

    print("\n" + "=" * 60)
