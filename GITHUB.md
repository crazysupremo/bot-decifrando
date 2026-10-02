# 📱 Bot Decifrando - GitHub & Git

## 🚀 Como Usar

### Clone este Repositório

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/bot-decifrando.git
cd bot-decifrando

# Para Windows
install.bat

# Para Mac/Linux
bash install.sh
```

### Ou Baixe o ZIP

1. Clique no botão verde **"Code"**
2. Selecione **"Download ZIP"**
3. Extraia a pasta
4. Execute `install.bat` (Windows) ou `bash install.sh` (Mac/Linux)

---

## ⚡ Iniciar Localmente

```bash
# Ative o ambiente virtual
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Inicie o bot
python app.py
```

Abra http://localhost:5000 no navegador

---

## 🌐 Deploy na Nuvem (Render)

Veja **DEPLOY_RENDER.md** para instruções passo a passo

```bash
git push origin main
```

O Render fará deploy automaticamente!

---

## 📂 Estrutura do Projeto

```
bot-decifrando/
├── app.py                    # Entrada principal
├── bot_decifrando.py        # Lógica do bot
├── bot_api_webhook.py       # API REST (alternativa)
├── bot_discord.py           # Bot Discord (opcional)
├── interface.html           # Interface visual
├── cliente_teste.py         # Exemplos de uso
├── requirements.txt         # Dependências
├── .env.example            # Configuração exemplo
├── .gitignore              # Arquivo ignorados Git
├── Procfile                # Para Render
├── render.yaml             # Config Render
├── install.bat             # Setup Windows
├── setup.sh                # Setup Mac/Linux
├── README.md               # Documentação
├── COMECE_AQUI.md         # Guia rápido
├── DEPLOY_RENDER.md       # Deploy na nuvem
└── GITHUB.md              # Este arquivo
```

---

## 🔧 Contribuir

1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b feature/sua-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona feature'`
4. Push: `git push origin feature/sua-feature`
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é open source. Use livremente!

---

## 💡 Dicas

- **Expandir dicionário**: Edite `_carregar_palavras_pt()` e `_carregar_palavras_es()`
- **Adicionar idiomas**: Crie novo método `_carregar_palavras_novo_idioma()`
- **Customizar interface**: Edite `interface.html`
- **Mais funcionalidades**: Adicione rotas em `app.py`

---

**Quer contribuir? Faça um Fork! 🍴**

