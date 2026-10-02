# 🎮 Bot Decifrando

Bot inteligente que **desembaralha palavras** e **resolve questões de matemática** em português e espanhol.

## 🌟 Funcionalidades

✅ **Desembaralha palavras** em português e espanhol
✅ **Resolve expressões matemáticas** complexas
✅ Suporta múltiplas plataformas (Discord, API, Webhook)
✅ Processamento em lote (batch)
✅ Log e estatísticas de uso
✅ Detecção automática de tipo de entrada
🤖 **Groq integrado** (opcional) — desembaralha QUALQUER palavra (não só as do dicionário local) e responde perguntas de quiz soltas, automaticamente
📢 **Resposta passiva no Discord** — o bot fica quieto até perceber uma mensagem de quiz (palavra em MAIÚSCULAS ou expressão matemática) solta no chat, sem precisar digitar comando nenhum

---

## 🤖 Ativando o Groq (resposta automática)

Sem isso configurado, o bot só reconhece as ~70 palavras do dicionário local
e só responde quando alguém digita um comando (`/desembaralha`, `/math`,
`/auto`). Com o Groq configurado:

1. Crie uma conta grátis em [console.groq.com](https://console.groq.com/keys) e gere uma chave de API.
2. Crie um arquivo chamado `.env` (sem nome antes do ponto) com o conteúdo:
   ```
   GROQ_API_KEY=sua_chave_aqui
   ```
3. Onde colocar esse arquivo `.env`:
   - **Rodando com Python direto** (`python app.py`): na mesma pasta do `app.py`.
   - **App de desktop instalado** (o instalador `.exe`): na MESMA PASTA onde o "Bot Decifrando.exe" foi instalado — geralmente `%LOCALAPPDATA%\Programs\bot-decifrando-desktop\`. O jeito mais fácil de achar essa pasta: clica com o botão direito no atalho da área de trabalho → "Abrir local do arquivo".
4. Reinicie o bot (feche e abra de novo). Pronto — agora ele desembaralha qualquer palavra e, no Discord, responde sozinho quando perceber uma mensagem de quiz no chat (sem precisar de `/comando`).

---

## 📦 Instalação

### 1. Clone ou baixe os arquivos:
```bash
git clone seu_repositorio
cd bot_decifrando
```

### 2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo .env:
```bash
cp .env.example .env
# Edite .env com seus dados
```

---

## 🚀 Como Usar

### Opção 1: Teste Básico (sem dependências externas)

```bash
python bot_decifrando.py
```

Isso executa exemplos de desembaralhar palavras e resolver matemática.

---

### Opção 2: Bot Discord

#### Pré-requisitos:
- Token do Discord (obtenha em https://discord.com/developers/applications)
- Arquivo `.env` configurado com `DISCORD_TOKEN`

#### Execução:
```bash
python bot_discord.py
```

#### Comandos Disponíveis:

**Desembaralhar palavra:**
```
/desembaralha OTEPMOC
/desembaralha OTEPMOC --es  # espanhol
```

**Resolver matemática:**
```
/math 2+2
/math (10*5)+20
/math 100/4-5
```

**Modo automático:**
```
/auto desembaralha OTEPMOC
/auto quanto é 25 + 17
```

**Ajuda:**
```
/help
```

---

### Opção 3: API Webhook (Para Integração com Jogo/Evento)

#### Execução:
```bash
python bot_api_webhook.py
```

A API rodará em `http://localhost:5000`

#### Endpoints Disponíveis:

**1. Desembaralhar Palavra:**
```bash
POST http://localhost:5000/desembaralha
Content-Type: application/json

{
  "palavra": "OTEPMOC",
  "idioma": "pt"
}
```

**Resposta:**
```json
{
  "tipo": "palavra_embaralhada",
  "entrada": "OTEPMOC",
  "idioma": "pt",
  "soluções": ["computador"],
  "quantidade": 1,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

**2. Resolver Matemática:**
```bash
POST http://localhost:5000/math
Content-Type: application/json

{
  "expressao": "2+2"
}
```

**Resposta:**
```json
{
  "tipo": "matematica",
  "entrada": "2+2",
  "resultado": "4",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

**3. Modo Automático (Detecta tipo):**
```bash
POST http://localhost:5000/auto
Content-Type: application/json

{
  "texto": "desembaralha OTEPMOC",
  "idioma": "pt"
}
```

**Resposta:**
```json
{
  "tipo": "palavra_embaralhada",
  "entrada": "OTEPMOC",
  "idioma": "pt",
  "resultado": ["computador"],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

**4. Processar em Lote (Batch):**
```bash
POST http://localhost:5000/batch
Content-Type: application/json

{
  "requisicoes": [
    {"tipo": "desembaralha", "palavra": "OTEPMOC"},
    {"tipo": "math", "expressao": "10*5+20"},
    {"tipo": "auto", "texto": "quanto é 2+2"}
  ],
  "idioma": "pt"
}
```

**Resposta:**
```json
{
  "tipo": "batch",
  "total": 3,
  "processadas": 3,
  "resultados": [
    {
      "tipo": "palavra_embaralhada",
      "entrada": "OTEPMOC",
      "soluções": ["computador"],
      "status": "sucesso"
    },
    {
      "tipo": "matematica",
      "entrada": "10*5+20",
      "resultado": "70",
      "status": "sucesso"
    },
    {
      "tipo": "desconhecido",
      "entrada": "quanto é 2+2",
      "resultado": ["4"],
      "status": "sucesso"
    }
  ],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

**5. Verificar Saúde:**
```bash
GET http://localhost:5000/health
```

---

**6. Ver Logs:**
```bash
GET http://localhost:5000/logs?limite=50
```

---

**7. Estatísticas:**
```bash
GET http://localhost:5000/stats
```

---

## 📝 Exemplos de Uso com cURL

### Desembaralhar:
```bash
curl -X POST http://localhost:5000/desembaralha \
  -H "Content-Type: application/json" \
  -d '{"palavra": "OTEPMOC", "idioma": "pt"}'
```

### Matemática:
```bash
curl -X POST http://localhost:5000/math \
  -H "Content-Type: application/json" \
  -d '{"expressao": "(10*5)+20"}'
```

### Batch:
```bash
curl -X POST http://localhost:5000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "requisicoes": [
      {"tipo": "desembaralha", "palavra": "OTEPMOC"},
      {"tipo": "math", "expressao": "2+2"}
    ],
    "idioma": "pt"
  }'
```

---

## 🔧 Integração com Seu Jogo/Evento

### Via API Webhook:

```python
import requests
import json

# Desembaralhar palavra
response = requests.post(
    'http://localhost:5000/desembaralha',
    json={'palavra': 'OTEPMOC', 'idioma': 'pt'}
)
resultado = response.json()
print(resultado['soluções'])

# Resolver matemática
response = requests.post(
    'http://localhost:5000/math',
    json={'expressao': '2+2'}
)
resultado = response.json()
print(f"Resultado: {resultado['resultado']}")
```

### Via JavaScript/Node.js:

```javascript
// Desembaralhar
fetch('http://localhost:5000/desembaralha', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({palavra: 'OTEPMOC', idioma: 'pt'})
})
.then(r => r.json())
.then(data => console.log(data.soluções));

// Matemática
fetch('http://localhost:5000/math', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({expressao: '2+2'})
})
.then(r => r.json())
.then(data => console.log(`Resultado: ${data.resultado}`));
```

---

## 📚 Estrutura de Arquivos

```
bot_decifrando/
├── bot_decifrando.py       # Classe principal do bot
├── bot_discord.py          # Integração com Discord
├── bot_api_webhook.py      # API Flask
├── requirements.txt        # Dependências
├── .env.example           # Variáveis de ambiente
└── README.md              # Este arquivo
```

---

## 🎯 Funcionalidades Futuras

- [ ] Integração com mais idiomas
- [ ] Dicionário expandido
- [ ] Cache de resultados
- [ ] Autenticação de API
- [ ] Dashboard de estatísticas
- [ ] Suporte a Telegram
- [ ] Machine Learning para melhor desembaralho

---

## ⚠️ Limitações Conhecidas

- O dicionário atual é limitado (adicione mais palavras em `_carregar_palavras_pt()` e `_carregar_palavras_es()`)
- Matemática: aceita apenas operações básicas (+, -, *, /, %, parênteses)
- Sem suporte a equações complexas ou cálculo

---

## 📧 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`
2. Verifique se o arquivo `.env` está correto
3. Veja os logs da API: `GET /logs`

---

## 📄 Licença

Este projeto é de código aberto. Use livremente!

---

## 🎉 Pronto!

Seu bot está pronto para desembaralhar palavras e resolver matemática! 🚀

