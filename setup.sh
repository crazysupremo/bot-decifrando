#!/bin/bash

# Script de Setup - Bot Decifrando
# Executa: bash setup.sh

echo "=========================================="
echo "🚀 Bot Decifrando - Setup Automático"
echo "=========================================="

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "💾 Baixe em: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Cria ambiente virtual
echo ""
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Ativa ambiente virtual
echo "✅ Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo ""
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Cria arquivo .env
if [ ! -f .env ]; then
    echo ""
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  Edite o arquivo .env com seus dados (DISCORD_TOKEN)"
else
    echo "✅ Arquivo .env já existe"
fi

echo ""
echo "=========================================="
echo "✨ Setup concluído com sucesso!"
echo "=========================================="
echo ""
echo "📚 Próximos passos:"
echo ""
echo "1️⃣  Teste básico (sem dependências externas):"
echo "   python bot_decifrando.py"
echo ""
echo "2️⃣  API Webhook (para integração):"
echo "   python bot_api_webhook.py"
echo ""
echo "3️⃣  Bot Discord (requer DISCORD_TOKEN em .env):"
echo "   python bot_discord.py"
echo ""
echo "4️⃣  Cliente de teste:"
echo "   python cliente_teste.py"
echo ""
echo "📖 Leia o README.md para mais informações!"
echo ""
