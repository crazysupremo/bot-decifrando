"""
groq_helper.py - Integração com o Groq pra responder automático quando o
dicionário local não dá conta (item pedido: "coloque o groq pra responder
automática no aplicativo").

Usado em dois momentos:
1. Fallback de desembaralhar palavra — quando a palavra não está no
   dicionário local (que hoje só tem umas 70 palavras), pergunta pro Groq.
2. Detecção passiva de quiz — o bot fica "inativo" até perceber uma
   mensagem que parece um quiz (palavra em maiúsculas sem espaço, ou uma
   expressão matemática) e só aí responde sozinho, sem precisar de comando.
"""

import os
import re
import json
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")


def groq_configurado():
    """Retorna True se a chave do Groq está configurada no .env."""
    return bool(os.getenv("GROQ_API_KEY"))


def perguntar_groq(prompt, max_tokens=200):
    """Manda um prompt pro Groq e devolve a resposta em texto puro.
    Se não tiver chave configurada, ou der erro, devolve None (quem chamou
    decide o que fazer — ex: manter a resposta antiga de "não encontrei")."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        resposta = requests.post(
            GROQ_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": GROQ_MODEL,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=15,
        )
        if not resposta.ok:
            return None
        dados = resposta.json()
        return dados["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def desembaralhar_com_groq(palavra_embaralhada, idioma="pt"):
    """Pede pro Groq decifrar uma palavra embaralhada que o dicionário local
    não encontrou. Devolve uma lista de palavras possíveis (ou lista vazia)."""
    idioma_nome = "português" if idioma == "pt" else "espanhol"
    prompt = (
        f"As letras a seguir foram embaralhadas de uma palavra real em {idioma_nome}: "
        f'"{palavra_embaralhada}". Descubra a palavra original. Responda SOMENTE com '
        f"a palavra em minúsculas, sem pontuação, sem explicação nenhuma. Se não tiver "
        f"certeza, responda com sua melhor tentativa mesmo assim."
    )
    resposta = perguntar_groq(prompt, max_tokens=20)
    if not resposta:
        return []
    # Pega só a primeira "palavra" de verdade da resposta, ignorando lixo.
    match = re.search(r"[a-zA-ZÀ-ÿ]+", resposta)
    return [match.group(0).lower()] if match else []


def responder_quiz_generico(texto):
    """Fallback final: a mensagem parece um quiz mas não é nem palavra
    embaralhada nem matemática clara (ex: uma pergunta de conhecimento geral
    digitada solta na sala). Deixa o Groq tentar responder como se fosse uma
    pergunta de quiz mesmo."""
    prompt = (
        "Você é um assistente de quiz num servidor de jogos. Alguém escreveu a "
        f'mensagem a seguir, que parece ser uma pergunta de quiz: "{texto}". '
        "Responda de forma direta e curta (no máximo 2 frases), em português, "
        "como se estivesse respondendo o quiz."
    )
    return perguntar_groq(prompt, max_tokens=150)


# ---------- Detecção passiva de "isso parece um quiz" ----------
_MATH_RE = re.compile(r"^[\s0-9+\-*/().%]+$")


def eh_mensagem_quiz(texto):
    """Decide se uma mensagem solta no chat (sem comando /desembaralha ou
    /math na frente) parece um quiz e merece resposta automática. Critério
    de propósito conservador — só dispara em casos bem claros, pra não ficar
    respondendo conversa normal do servidor."""
    texto = (texto or "").strip()
    if not texto or len(texto) > 60:
        return False

    # Expressão matemática pura (ex: "12*5+3", "(10/2)-1").
    if _MATH_RE.match(texto) and any(op in texto for op in "+-*/%"):
        return True

    # Palavra única, só letras, maiúscula (clássico "palavra embaralhada"
    # apresentada em jogo/quiz: ex "OTEPMOC"), com 4+ letras.
    palavras = texto.split()
    if len(palavras) == 1:
        p = palavras[0]
        if p.isalpha() and len(p) >= 4 and p == p.upper():
            return True

    return False
