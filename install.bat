@echo off
REM Script de instalação para Windows - Bot Decifrando

echo.
echo ==========================================
echo 🚀 Bot Decifrando - Setup para Windows
echo ==========================================
echo.

REM CORRIGIDO: muita gente tem o Python instalado mas o comando "python"
REM não está disponível (só o "py", o Python Launcher) — o instalador antigo
REM desistia na hora achando que o Python não estava instalado. Agora testa
REM os dois antes de desistir de verdade.
set PY_CMD=
python --version >nul 2>&1
if not errorlevel 1 set PY_CMD=python
if not defined PY_CMD (
    py --version >nul 2>&1
    if not errorlevel 1 set PY_CMD=py
)

if not defined PY_CMD (
    echo ❌ Python não encontrado nem como "python" nem como "py"!
    echo 💾 Baixe e instale em: https://www.python.org/downloads/
    echo ⚠️  IMPORTANTE: marque a caixinha "Add Python to PATH" durante a instalação.
    echo    Depois de instalar, feche esta janela e rode install.bat de novo.
    pause
    exit /b 1
)

echo ✅ Python encontrado (comando: %PY_CMD%):
%PY_CMD% --version
echo.

REM Cria ambiente virtual
echo 📦 Criando ambiente virtual...
%PY_CMD% -m venv venv
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Não deu pra criar o ambiente virtual. Verifique se o Python foi instalado corretamente.
    pause
    exit /b 1
)

REM Ativa ambiente virtual
echo ✅ Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instala dependências
echo.
echo 📥 Instalando dependências (pode demorar um minuto)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Deu erro ao instalar as dependências. Verifique sua conexão com a internet e tente de novo.
    pause
    exit /b 1
)

REM Cria arquivo .env
if not exist .env (
    echo.
    echo 📝 Criando arquivo .env...
    copy .env.example .env >nul
    echo ⚠️  Edite o arquivo .env com o Notepad e preencha DISCORD_TOKEN ^(e GROQ_API_KEY, opcional^)
) else (
    echo ✅ Arquivo .env já existe
)

echo.
echo ==========================================
echo ✨ Setup concluído com sucesso!
echo ==========================================
echo.
echo 🚀 Pra iniciar o bot, dá dois cliques em start_windows.bat
echo    ^(ou rode "%PY_CMD% app.py" manualmente^)
echo.
echo 📖 Leia o COMECE_AQUI.md para mais informações!
echo.
pause
