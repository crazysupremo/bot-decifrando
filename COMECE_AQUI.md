# 🚀 COMECE AQUI - Bot Decifrando

## 📋 O que é?

Um **bot inteligente** que:
- ✅ Desembaralha palavras (PT/ES)
- ✅ Resolve questões de matemática
- ✅ Roda em múltiplas plataformas (API, Discord, Interface Web)

---

## ⚡ Quick Start (3 Passos)

### 1️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Rode a API
```bash
python bot_api_webhook.py
```

Você vai ver:
```
🚀 Bot Decifrando - API Webhook iniciado
📍 URL: http://localhost:5000
```

### 3️⃣ Abra a interface visual
- Abra o arquivo **`interface.html`** no navegador
- Ou acesse http://localhost:5000 (documentação da API)

---

## 🎯 O que você descobrirá

Ao abrir a **interface.html**, você verá:

### 🔤 Desembaralhar Palavras
```
Entrada:  OTEPMOC
Resultado: COMPUTADOR ✅
```

### 🧮 Resolver Matemática
```
Entrada:  (10*5)+20
Resultado: 70 ✅
```

### 🤖 Modo Automático
O bot detecta automaticamente se é palavra ou matemática!

---

## 📁 Arquivos Criados

| Arquivo | Função |
|---------|--------|
| **bot_decifrando.py** | Classe principal (lógica) |
| **bot_api_webhook.py** | API REST para integração |
| **bot_discord.py** | Bot Discord (opcional) |
| **interface.html** | Interface visual bonita |
| **cliente_teste.py** | Cliente para testar |
| **requirements.txt** | Dependências |
| **README.md** | Documentação completa |

---

## 🎮 Três Formas de Usar

### 1. Interface Visual (Recomendado para começar)
```bash
# Terminal 1: Inicie a API
python bot_api_webhook.py

# Terminal 2: Abra a interface
# Abra interface.html no navegador
```

### 2. Linha de Comando (Teste rápido)
```bash
python bot_decifrando.py
```

### 3. Bot Discord (para comunidade)
```bash
# Configure o DISCORD_TOKEN em .env
python bot_discord.py
```

---

## 📝 Exemplos Rápidos

### Desembaralhar
```python
from bot_decifrando import BotDecifrando

bot = BotDecifrando()
resultado = bot.desembaralhar_palavra("OTEPMOC", idioma="pt")
print(resultado)  # ['computador']
```

### Matemática
```python
resultado = bot.resolver_matematica("2+2")
print(resultado)  # '4'
```

### Via API
```bash
curl -X POST http://localhost:5000/desembaralha \
  -H "Content-Type: application/json" \
  -d '{"palavra": "OTEPMOC", "idioma": "pt"}'
```

---

## 🔧 Integração com Seu Jogo/Evento

### Python
```python
import requests

# Desembaralhar
response = requests.post('http://localhost:5000/desembaralha',
    json={'palavra': 'OTEPMOC'})
print(response.json())
```

### JavaScript
```javascript
fetch('http://localhost:5000/desembaralha', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({palavra: 'OTEPMOC'})
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## 💡 Próximos Passos

1. ✅ Rode a API: `python bot_api_webhook.py`
2. ✅ Abra: `interface.html`
3. ✅ Teste as funcionalidades
4. ✅ Integre com seu jogo/evento
5. ✅ Leia `README.md` para mais detalhes

---

## ❓ Dúvidas?

- API não conecta? → Rodou `python bot_api_webhook.py`?
- Interface vazia? → Veja se a API está online (status verde)
- Precisa de mais palavras? → Edite `_carregar_palavras_pt()` em `bot_decifrando.py`
- Quer mais idiomas? → Adicione em `_carregar_palavras_*()` com seu dicionário

---

## 🎉 Pronto!

Seu bot está completo e pronto para usar! 🚀

**Próximo passo**: Abra `interface.html` e explore as funcionalidades!

