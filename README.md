# 🤖 Custom GPT Actions - OpenAI & Claude API

Progetto completo per creare **Custom GPT con Actions** che chiamano sia OpenAI che Claude, con supporto per thinking e confronto tra modelli.

## 🎯 Cosa puoi fare

✅ Usare le API di OpenAI e Claude da Python (con thinking e streaming)
✅ Esporre un'API REST con FastAPI
✅ **Creare un Custom GPT in ChatGPT che usa le tue API**
✅ Confrontare le risposte di OpenAI e Claude
✅ Fare deploy su server gratuiti (Ngrok, Replit, Railway, Render)

## 🚀 Quick Start

### 1. Setup locale (5 minuti)

```bash
# Clona il repository
git clone https://github.com/valeadami/claude-code-website-test.git
cd claude-code-website-test

# Installa dipendenze
pip install -r requirements.txt

# Configura le API keys
cp .env.example .env
# Modifica .env e inserisci le tue chiavi API
```

### 2. Testa il client Python

```bash
python core/api_client.py
```

### 3. Prova un esempio

**Esempio 1: Customer Care Bot** (chatbot assistenza clienti)
```bash
python examples/customer_care/server.py
# Test: python examples/customer_care/test.py
```

**Esempio 2: OpenAI vs Claude** (confronto modelli)
```bash
python examples/openai_claude/server.py
# Test: python examples/openai_claude/test.py
```

### 4. Crea il Custom GPT

📖 **Guida rapida:** [docs/QUICKSTART.md](docs/QUICKSTART.md)
📖 **Guida completa:** [docs/CUSTOM_GPT_SETUP.md](docs/CUSTOM_GPT_SETUP.md)
📖 **Opzioni di deployment:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📚 Documentazione

### Guide Generali

| Documento | Descrizione |
|-----------|-------------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Setup rapido in 5-10 minuti |
| [docs/PYTHON_README.md](docs/PYTHON_README.md) | Uso del client Python per OpenAI e Claude |
| [docs/CUSTOM_GPT_SETUP.md](docs/CUSTOM_GPT_SETUP.md) | Guida completa per Custom GPT Actions |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Come fare il deploy (Ngrok, Replit, Railway, Render) |

### 🎯 Esempi Pratici

#### 🛍️ Customer Care Bot

Un chatbot completo per assistenza clienti con Knowledge Base e API per stato ordini.

| File | Descrizione |
|------|-------------|
| [examples/customer_care/README.md](examples/customer_care/README.md) | Overview e guida |
| [examples/customer_care/SETUP.md](examples/customer_care/SETUP.md) | Setup Custom GPT step-by-step |
| `examples/customer_care/server.py` | Server API con 8 ordini mockup |
| `examples/customer_care/knowledge_base.md` | KB con FAQ e politiche |
| `examples/customer_care/test.py` | Test suite interattiva |

**Quick Start:**
```bash
python examples/customer_care/server.py
python examples/customer_care/test.py
```

#### 🤖 OpenAI vs Claude

Confronta le risposte di OpenAI e Claude sullo stesso prompt.

| File | Descrizione |
|------|-------------|
| [examples/openai_claude/README.md](examples/openai_claude/README.md) | Overview e guida |
| `examples/openai_claude/server.py` | Server API multi-model |
| `examples/openai_claude/test.py` | Test suite |

**Quick Start:**
```bash
python examples/openai_claude/server.py
python examples/openai_claude/test.py
```

---

## 🌟 Funzionalità

### Client Python
- ✅ OpenAI GPT-4o, GPT-4o-mini, o1, o1-mini
- ✅ Claude Sonnet 4.5, Opus 4, Haiku 4
- ✅ Supporto thinking/reasoning esteso
- ✅ Streaming delle risposte
- ✅ Conversazioni multi-turno

### API Server REST
- ✅ `POST /openai/chat` - Chiama OpenAI
- ✅ `POST /claude/chat` - Chiama Claude
- ✅ `POST /compare` - Confronta entrambi
- ✅ Autenticazione Bearer token
- ✅ Documentazione Swagger automatica

### Custom GPT Actions
- ✅ Schema OpenAPI auto-generato
- ✅ Configurazione completa per ChatGPT
- ✅ Esempi di prompt e workflow
- ✅ Guide per deployment cloud

---

## 🎮 Esempi d'uso

### Client Python

```python
from core.api_client import OpenAIClient, ClaudeClient

# OpenAI
client = OpenAIClient()
response = client.chat_completion(
    messages=[{"role": "user", "content": "Spiega le API REST"}],
    thinking_enabled=True  # Usa o1 per reasoning
)

# Claude
client = ClaudeClient()
response = client.create_message(
    messages=[{"role": "user", "content": "Spiega le API REST"}],
    thinking_enabled=True  # Extended thinking
)
```

### API REST

```bash
# Chiamata a OpenAI
curl -X POST http://localhost:8000/openai/chat \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ciao!", "thinking": false}'

# Confronto modelli
curl -X POST http://localhost:8000/compare \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Cosa sono le API?", "thinking": false}'
```

### Custom GPT

Dopo il setup, puoi usare prompt come:

```
Usa Claude con thinking per risolvere questo problema matematico complesso
```

```
Confronta come OpenAI e Claude spiegano il machine learning
```

---

## 🌐 Deployment

Il progetto include configurazioni pronte per:

- **Ngrok** (test rapidi, 2 minuti)
- **Replit** (gratuito, URL permanente)
- **Railway** ($5/mese, produzione)
- **Render** (gratuito, con limitazioni)

Vedi [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) per le guide dettagliate.

---

## 📋 Requisiti

- Python 3.8+
- Account OpenAI con API key
- Account Anthropic con API key
- (Opzionale) Account ChatGPT Plus per Custom GPT

---

## 🔧 Struttura Progetto

```
.
├── examples/                    # Esempi Custom GPT
│   ├── customer_care/          # 🛍️ Chatbot assistenza clienti
│   │   ├── server.py           # API server
│   │   ├── knowledge_base.md   # KB con FAQ e politiche
│   │   ├── test.py             # Test suite
│   │   ├── README.md           # Guida esempio
│   │   └── SETUP.md            # Setup Custom GPT
│   │
│   └── openai_claude/          # 🤖 Confronto OpenAI vs Claude
│       ├── server.py           # API server multi-model
│       ├── test.py             # Test suite
│       └── README.md           # Guida esempio
│
├── docs/                        # 📚 Documentazione
│   ├── QUICKSTART.md           # Setup rapido
│   ├── DEPLOYMENT.md           # Guide deployment
│   ├── CUSTOM_GPT_SETUP.md     # Setup Custom GPT generale
│   └── PYTHON_README.md        # Uso client Python
│
├── core/                        # 🔧 Codice condiviso
│   ├── __init__.py
│   ├── api_client.py           # Client OpenAI/Claude
│   └── examples.py             # Esempi d'uso
│
├── scripts/                     # 🛠️ Utility
│   ├── generate_openapi_schema.py
│   └── deploy_ngrok.sh
│
├── deploy/                      # ☁️ Configurazioni deployment
│   ├── .replit
│   ├── replit.nix
│   ├── railway.json
│   ├── render.yaml
│   └── Procfile
│
├── .env.example                 # Template env vars
├── requirements.txt             # Dipendenze Python
├── .gitignore
└── README.md
```

---

## 🆘 Supporto

Problemi comuni e soluzioni in [docs/CUSTOM_GPT_SETUP.md](docs/CUSTOM_GPT_SETUP.md#troubleshooting)

---

## 📄 Licenza

MIT License - Vedi [LICENSE](LICENSE)

---

## 🌟 Contributi

Pull request benvenute! Per modifiche importanti, apri prima un issue.

---

**Happy coding!** 🚀
