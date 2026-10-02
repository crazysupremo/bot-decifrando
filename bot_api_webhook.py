"""
Bot Decifrando - API Webhook
Recebe requisições HTTP do jogo/evento
Requer: pip install flask flask-cors
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from bot_decifrando import BotDecifrando
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inicializa o bot
decifrando = BotDecifrando()

# Log de requisições
requisicoes_log = []


@app.route('/health', methods=['GET'])
def health():
    """Verifica saúde da API"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'servico': 'Bot Decifrando'
    }), 200


@app.route('/desembaralha', methods=['POST'])
def desembaralha_api():
    """
    POST /desembaralha
    Body JSON:
    {
        "palavra": "OTEPMOC",
        "idioma": "pt"  // opcional: "pt" ou "es"
    }
    """
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

        # Log
        requisicoes_log.append(resposta)

        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/math', methods=['POST'])
def math_api():
    """
    POST /math
    Body JSON:
    {
        "expressao": "2+2"
    }
    """
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

        # Log
        requisicoes_log.append(resposta)

        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/auto', methods=['POST'])
def auto_api():
    """
    POST /auto
    Detecta automaticamente o tipo de entrada
    Body JSON:
    {
        "texto": "desembaralha OTEPMOC",
        "idioma": "pt"  // opcional
    }
    """
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

        # Log
        requisicoes_log.append(resposta)

        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/batch', methods=['POST'])
def batch_api():
    """
    POST /batch
    Processa múltiplas requisições em um lote
    Body JSON:
    {
        "requisicoes": [
            {"tipo": "desembaralha", "palavra": "OTEPMOC"},
            {"tipo": "math", "expressao": "2+2"},
            {"tipo": "auto", "texto": "..."}
        ],
        "idioma": "pt"
    }
    """
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
        'outros': len(requisicoes_log) - palavras - matematica
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Página inicial com documentação"""
    return jsonify({
        'servico': 'Bot Decifrando API',
        'versao': '1.0',
        'endpoints': {
            'GET /health': 'Verifica saúde da API',
            'POST /desembaralha': 'Desembaralha uma palavra',
            'POST /math': 'Resolve expressão matemática',
            'POST /auto': 'Detecta automaticamente tipo de entrada',
            'POST /batch': 'Processa múltiplas requisições',
            'GET /logs': 'Retorna log de requisições',
            'GET /stats': 'Retorna estatísticas'
        },
        'exemplos': {
            'desembaralha': {
                'url': 'POST /desembaralha',
                'body': {'palavra': 'OTEPMOC', 'idioma': 'pt'}
            },
            'math': {
                'url': 'POST /math',
                'body': {'expressao': '2+2'}
            },
            'batch': {
                'url': 'POST /batch',
                'body': {
                    'requisicoes': [
                        {'tipo': 'desembaralha', 'palavra': 'OTEPMOC'},
                        {'tipo': 'math', 'expressao': '10*5'}
                    ],
                    'idioma': 'pt'
                }
            }
        }
    }), 200


@app.errorhandler(404)
def nao_encontrado(e):
    """Tratamento de rota não encontrada"""
    return jsonify({
        'erro': 'Rota não encontrada',
        'mensagem': 'Visite GET / para documentação'
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
    print("🚀 Bot Decifrando - API Webhook iniciado")
    print("📍 URL: http://localhost:5000")
    print("📚 Documentação: GET http://localhost:5000/")
    print("=" * 60)

    # Debug mode pode ser ativado com:
    # app.run(debug=True, host='0.0.0.0', port=5000)

    app.run(debug=False, host='0.0.0.0', port=5000)
