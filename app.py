"""
Bot Decifrando - App Principal
Detecta ambiente (Local, Render, ou .exe empacotado) e configura automaticamente
"""

import os
import sys
import threading
import webbrowser
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from bot_decifrando import BotDecifrando
from datetime import datetime
import json

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

# Item pedido: virar um instalador/app de verdade (igual o NEXT GAME
# Desktop), não só um script que só funciona com Python + cmd. Quando
# empacotado com PyInstaller (--onefile), os arquivos (interface.html)
# ficam extraídos numa pasta temporária apontada por sys._MEIPASS — fora
# disso (rodando o .py direto), é a pasta normal do projeto.
IS_FROZEN = getattr(sys, 'frozen', False)
BASE_DIR = Path(sys._MEIPASS) if IS_FROZEN else Path(__file__).parent

# CORRIGIDO (bug real — "o Groq não funciona pra calcular/decifrar"): esse
# arquivo nunca chamava load_dotenv() em lugar nenhum! A variável
# GROQ_API_KEY do .env nunca era lida de verdade pro processo — por isso
# groq_configurado() sempre voltava False e o fallback do Groq nunca rodava,
# mesmo com a chave preenchida certinho no arquivo. Só o bot_discord.py
# chamava load_dotenv(), e o app.py (usado pelo .exe/app de desktop) não.
#
# Também precisa procurar o .env no lugar certo: quando empacotado em .exe,
# sys._MEIPASS é uma pasta TEMPORÁRIA que o PyInstaller apaga ao fechar —
# colocar o .env lá dentro não funcionaria. O lugar certo é do lado do
# próprio .exe (sys.executable), onde a pessoa realmente consegue editar o
# arquivo depois de instalado.
from dotenv import load_dotenv

if IS_FROZEN:
    env_path = Path(sys.executable).parent / '.env'
else:
    env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__, static_folder=None)
CORS(app)

# Inicializa o bot
decifrando = BotDecifrando()

# Log de requisições
requisicoes_log = []

# Detecta ambiente
IS_RENDER = os.getenv('RENDER') == 'true'
PORT = int(os.getenv('PORT', 5000))
HOST = '0.0.0.0' if IS_RENDER else 'localhost'

# ============================================================================
# ROTAS
# ============================================================================

@app.route('/')
def index():
    """Página inicial"""
    return send_file(BASE_DIR / 'interface.html'), 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/health', methods=['GET'])
def health():
    """Verifica saúde da API"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'servico': 'Bot Decifrando',
        'ambiente': 'Render' if IS_RENDER else 'Local'
    }), 200


@app.route('/desembaralha', methods=['POST'])
def desembaralha_api():
    """Desembaralha uma palavra"""
    try:
        dados = request.get_json()

        if not dados or 'palavra' not in dados:
            return jsonify({
                'erro': 'Campo "palavra" é obrigatório',
                'exemplo': {'palavra': 'OTEPMOC', 'idioma': 'pt'}
            }), 400

        palavra = dados.get('palavra', '')
        idioma = dados.get('idioma', 'pt')

        if idioma not in ['pt', 'es']:
            return jsonify({'erro': 'Idioma deve ser "pt" ou "es"'}), 400

        resultado = decifrando.desembaralhar_palavra(palavra, idioma)

        resposta = {
            'tipo': 'palavra_embaralhada',
            'entrada': palavra,
            'idioma': idioma,
            'soluções': resultado,
            'quantidade': len(resultado),
            'timestamp': datetime.now().isoformat()
        }

        requisicoes_log.append(resposta)
        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/math', methods=['POST'])
def math_api():
    """Resolve expressão matemática"""
    try:
        dados = request.get_json()

        if not dados or 'expressao' not in dados:
            return jsonify({
                'erro': 'Campo "expressao" é obrigatório',
                'exemplo': {'expressao': '2+2'}
            }), 400

        expressao = dados.get('expressao', '')
        resultado = decifrando.resolver_matematica(expressao)

        resposta = {
            'tipo': 'matematica',
            'entrada': expressao,
            'resultado': resultado,
            'timestamp': datetime.now().isoformat()
        }

        requisicoes_log.append(resposta)
        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/auto', methods=['POST'])
def auto_api():
    """Detecta automaticamente o tipo de entrada"""
    try:
        dados = request.get_json()

        if not dados or 'texto' not in dados:
            return jsonify({
                'erro': 'Campo "texto" é obrigatório',
                'exemplo': {'texto': 'desembaralha OTEPMOC', 'idioma': 'pt'}
            }), 400

        texto = dados.get('texto', '')
        idioma = dados.get('idioma', 'pt')

        if idioma not in ['pt', 'es']:
            return jsonify({'erro': 'Idioma deve ser "pt" ou "es"'}), 400

        resultado = decifrando.processar_entrada(texto, idioma)

        resposta = {
            'tipo': resultado['tipo'],
            'entrada': resultado['input'],
            'idioma': idioma,
            'resultado': resultado['resultado'],
            'timestamp': datetime.now().isoformat()
        }

        requisicoes_log.append(resposta)
        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/batch', methods=['POST'])
def batch_api():
    """Processa múltiplas requisições em lote"""
    try:
        dados = request.get_json()

        if not dados or 'requisicoes' not in dados:
            return jsonify({
                'erro': 'Campo "requisicoes" é obrigatório',
                'exemplo': {
                    'requisicoes': [
                        {'tipo': 'desembaralha', 'palavra': 'OTEPMOC'},
                        {'tipo': 'math', 'expressao': '2+2'}
                    ]
                }
            }), 400

        requisicoes = dados.get('requisicoes', [])
        idioma = dados.get('idioma', 'pt')
        resultados = []

        for req in requisicoes:
            try:
                tipo = req.get('tipo', '')

                if tipo == 'desembaralha':
                    resultado = decifrando.desembaralhar_palavra(req['palavra'], idioma)
                    resultados.append({
                        'tipo': 'palavra_embaralhada',
                        'entrada': req['palavra'],
                        'soluções': resultado,
                        'status': 'sucesso'
                    })

                elif tipo == 'math':
                    resultado = decifrando.resolver_matematica(req['expressao'])
                    resultados.append({
                        'tipo': 'matematica',
                        'entrada': req['expressao'],
                        'resultado': resultado,
                        'status': 'sucesso'
                    })

                elif tipo == 'auto':
                    resultado = decifrando.processar_entrada(req['texto'], idioma)
                    resultados.append({
                        'tipo': resultado['tipo'],
                        'entrada': req['texto'],
                        'resultado': resultado['resultado'],
                        'status': 'sucesso'
                    })
                else:
                    resultados.append({
                        'entrada': req,
                        'status': 'erro',
                        'mensagem': f"Tipo desconhecido: {tipo}"
                    })

            except KeyError as e:
                resultados.append({
                    'entrada': req,
                    'status': 'erro',
                    'mensagem': f"Campo obrigatório faltando: {str(e)}"
                })

        resposta = {
            'tipo': 'batch',
            'total': len(requisicoes),
            'processadas': len(resultados),
            'resultados': resultados,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """Retorna log das últimas requisições"""
    limite = request.args.get('limite', 50, type=int)
    return jsonify({
        'total': len(requisicoes_log),
        'limitado_a': limite,
        'logs': requisicoes_log[-limite:]
    }), 200


@app.route('/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas de uso"""
    palavras = sum(1 for r in requisicoes_log if r.get('tipo') == 'palavra_embaralhada')
    matematica = sum(1 for r in requisicoes_log if r.get('tipo') == 'matematica')

    return jsonify({
        'total_requisicoes': len(requisicoes_log),
        'palavras_desembaraçadas': palavras,
        'expressoes_matematicas': matematica,
        'outros': len(requisicoes_log) - palavras - matematica,
        'ambiente': 'Render' if IS_RENDER else 'Local'
    }), 200


@app.errorhandler(404)
def nao_encontrado(e):
    """Tratamento de rota não encontrada"""
    return jsonify({
        'erro': 'Rota não encontrada',
        'mensagem': 'Visite GET / para a interface visual'
    }), 404


@app.errorhandler(500)
def erro_interno(e):
    """Tratamento de erro interno"""
    return jsonify({
        'erro': 'Erro interno do servidor',
        'mensagem': str(e)
    }), 500


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == '__main__':
    ambiente = 'Render' if IS_RENDER else 'Local'
    print("=" * 60)
    print(f"🚀 Bot Decifrando - Ambiente: {ambiente}")
    print(f"📍 URL: http://{HOST}:{PORT}")
    print(f"🌐 Interface: http://{HOST}:{PORT}/")
    print(f"📚 API: http://{HOST}:{PORT}/health")
    print("=" * 60)
    print()

    # Item pedido ("não quero que vá pra uma página da web, quero um app de
    # desktop de verdade"): quando esse app.py roda COMO BACKEND de dentro do
    # Electron (ver electron-main.js), quem abre a janela é o próprio
    # Electron — abrir o navegador aqui também criaria uma aba solta extra,
    # duplicando a tela. ELECTRON_BACKEND=1 é a variável que o Electron
    # define ao chamar esse processo, exatamente pra evitar isso.
    is_electron_backend = os.getenv('ELECTRON_BACKEND') == '1'
    if not IS_RENDER and not is_electron_backend:
        url_abertura = f"http://{HOST}:{PORT}/"
        threading.Timer(1.2, lambda: webbrowser.open(url_abertura)).start()

    # Executa o app (debug=False quando empacotado — o reloader do Flask não
    # funciona dentro de um .exe gerado pelo PyInstaller e trava a abertura).
    app.run(host=HOST, port=PORT, debug=(not IS_RENDER and not IS_FROZEN))
