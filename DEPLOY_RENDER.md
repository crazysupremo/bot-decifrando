# 🚀 Deploy no Render.com

## Como colocar seu bot na nuvem (GRÁTIS)

### 1️⃣ Preparar o Repositório Git

```bash
# Inicialize Git (se ainda não fez)
git init
git add .
git commit -m "Bot Decifrando - Versão inicial"

# Crie um repositório no GitHub
# https://github.com/new

# Faça push
git remote add origin https://github.com/seu-usuario/bot-decifrando.git
git branch -M main
git push -u origin main
```

### 2️⃣ Criar Conta no Render

1. Acesse https://render.com
2. Clique em **"Sign up"**
3. Conecte sua conta GitHub
4. Autorize o Render acessar seus repositórios

### 3️⃣ Deploy Automático

1. No dashboard do Render, clique **"New +"** → **"Web Service"**
2. Selecione seu repositório `bot-decifrando`
3. Preencha os dados:
   - **Name**: `bot-decifrando`
   - **Environment**: `Python 3.9`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
4. Clique **"Create Web Service"**

### 4️⃣ Pronto! 🎉

Seu bot estará disponível em:
```
https://seu-projeto.onrender.com/
```

O Render faz deploy automático quando você faz push no GitHub!

---

## 📱 Acessar no Celular/Outro Computador

A URL do Render funciona de qualquer lugar:

```
https://seu-projeto.onrender.com/  ← Interface visual bonita
https://seu-projeto.onrender.com/health  ← Verificar status
```

---

## 🔧 Integração via API

Seu jogo/evento pode usar a API diretamente:

```python
import requests

API_URL = "https://seu-projeto.onrender.com"

# Desembaralhar
response = requests.post(
    f"{API_URL}/desembaralha",
    json={"palavra": "OTEPMOC", "idioma": "pt"}
)
print(response.json())
```

---

## 💡 Dicas

- **Render free tier**: app dorme após inatividade (15 minutos)
- **Quer 24/7?**: Contrate um plano pago
- **Logs**: Veja em "Logs" no dashboard do Render
- **Redeploy**: Push no GitHub dispara novo deploy automaticamente

---

## ❓ Problemas?

Se der erro no Render:
1. Verifique os logs no dashboard
2. Certifique-se que `app.py` existe
3. Verifique `requirements.txt`
4. Se tiver `DISCORD_TOKEN`, adicione em "Environment Variables"

---

**Seu bot está na nuvem! 🌐**
