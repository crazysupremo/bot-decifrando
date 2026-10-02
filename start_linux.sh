#!/bin/bash

# Script para iniciar o Bot Decifrando no Mac/Linux

echo ""
echo "🚀 Iniciando Bot Decifrando..."
echo ""

# Verifica se ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute 'bash install.sh' primeiro"
    exit 1
fi

# Ativa ambiente virtual
source venv/bin/activate

echo "✅ Ambiente ativado"
echo "🌐 Abrindo http://localhost:5000..."

# Tenta abrir no navegador (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 1
    open http://localhost:5000
fi

# Inicia o servidor
echo ""
echo "🎮 Bot rodando!"
echo "📍 http://localhost:5000"
echo "🛑 Pressione CTRL+C para parar"
echo ""

python app.py
