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
python api_client.py
```

### 3. Avvia l'API server

```bash
python api_server.py
# Server disponibile su http://localhost:8000
# Documentazione: http://localhost:8000/docs
```

### 4. Crea il Custom GPT

📖 **Guida rapida:** [QUICKSTART.md](QUICKSTART.md)
📖 **Guida completa:** [CUSTOM_GPT_SETUP.md](CUSTOM_GPT_SETUP.md)
📖 **Opzioni di deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)

## 📚 Documentazione

| Documento | Descrizione |
|-----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Setup rapido in 5-10 minuti |
| [PYTHON_README.md](PYTHON_README.md) | Uso del client Python per OpenAI e Claude |
| [CUSTOM_GPT_SETUP.md](CUSTOM_GPT_SETUP.md) | Guida completa per Custom GPT Actions |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Come fare il deploy (Ngrok, Replit, Railway, Render) |

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

## 🎮 Esempi d'uso

### Client Python

```python
from api_client import OpenAIClient, ClaudeClient

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

## 🌐 Deployment

Il progetto include configurazioni pronte per:

- **Ngrok** (test rapidi, 2 minuti)
- **Replit** (gratuito, URL permanente)
- **Railway** ($5/mese, produzione)
- **Render** (gratuito, con limitazioni)

Vedi [DEPLOYMENT.md](DEPLOYMENT.md) per le guide dettagliate.

## 📋 Requisiti

- Python 3.8+
- Account OpenAI con API key
- Account Anthropic con API key
- (Opzionale) Account ChatGPT Plus per Custom GPT

## 🔧 Struttura Progetto

```
.
├── api_client.py              # Client Python per OpenAI/Claude
├── api_server.py              # Server FastAPI con endpoint REST
├── examples.py                # Esempi d'uso del client
├── test_api_server.py         # Test suite per l'API
├── generate_openapi_schema.py # Genera schema per Custom GPT
├── requirements.txt           # Dipendenze Python
├── .env.example              # Template variabili d'ambiente
├── QUICKSTART.md             # Guida rapida
├── PYTHON_README.md          # Documentazione client Python
├── CUSTOM_GPT_SETUP.md       # Guida Custom GPT completa
└── DEPLOYMENT.md             # Guide deployment
```

## 🆘 Supporto

Problemi comuni e soluzioni in [CUSTOM_GPT_SETUP.md](CUSTOM_GPT_SETUP.md#troubleshooting)

## 📄 Licenza

MIT License - Vedi [LICENSE](LICENSE)

## 🌟 Contributi

Pull request benvenute! Per modifiche importanti, apri prima un issue.

---

**Happy coding!** 🚀
