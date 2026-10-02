@echo off
REM Script para iniciar o Bot Decifrando no Windows

echo.
echo 🚀 Iniciando Bot Decifrando...
echo.

REM Verifica se ambiente virtual existe
if not exist "venv" (
    echo ❌ Ambiente virtual não encontrado!
    echo Execute "install.bat" primeiro
    pause
    exit /b 1
)

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

REM Inicia o bot
echo ✅ Ambiente ativado
echo 🌐 Abrindo http://localhost:5000...
timeout /t 2

REM Tenta abrir no navegador
start http://localhost:5000

REM Inicia o servidor
echo.
echo 🎮 Bot rodando!
echo 📍 http://localhost:5000
echo 🛑 Pressione CTRL+C para parar
echo.

python app.py
