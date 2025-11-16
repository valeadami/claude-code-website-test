# 🤖 OpenAI & Claude Comparison API

Custom GPT Action che permette di chiamare sia OpenAI che Claude e confrontare le risposte.

## 🎯 Funzionalità

- ✅ **Chiamata a OpenAI** con supporto thinking (modello o1)
- ✅ **Chiamata a Claude** con extended thinking
- ✅ **Confronto diretto** tra le risposte dei due modelli
- ✅ Autenticazione Bearer token
- ✅ Documentazione Swagger automatica

## 🚀 Quick Start

### 1. Configura le API keys

Dalla root del progetto:

```bash
cp .env.example .env
# Modifica .env e inserisci:
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
# - CUSTOM_GPT_API_KEY
```

### 2. Avvia il server

```bash
# Dalla root del progetto
python examples/openai_claude/server.py

# Oppure dalla cartella dell'esempio
cd examples/openai_claude
python server.py
```

Il server sarà disponibile su `http://localhost:8000`

### 3. Testa il server

```bash
# Dalla root del progetto
python examples/openai_claude/test.py

# Test manuale
curl -X POST http://localhost:8000/openai/chat \
  -H "Authorization: Bearer your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ciao!", "thinking": false}'
```

### 4. Visualizza la documentazione

Apri nel browser:
```
http://localhost:8000/docs
```

## 📡 Endpoint Disponibili

### POST /openai/chat

Chiama OpenAI GPT (usa o1 se thinking=true).

**Request:**
```json
{
  "prompt": "Spiega cos'è FastAPI",
  "thinking": false,
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response:**
```json
{
  "response": "FastAPI è un framework...",
  "model": "gpt-4o",
  "thinking_used": false
}
```

### POST /claude/chat

Chiama Claude (con extended thinking opzionale).

**Request:**
```json
{
  "prompt": "Spiega cos'è FastAPI",
  "thinking": true,
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response:**
```json
{
  "response": "[RAGIONAMENTO]: ... [RISPOSTA]: FastAPI è...",
  "model": "claude-sonnet-4-5-20250929",
  "thinking_used": true
}
```

### POST /compare

Confronta le risposte di entrambi i modelli.

**Request:**
```json
{
  "prompt": "Cosa sono le API REST?",
  "thinking": false
}
```

**Response:**
```json
{
  "openai_response": "Le API REST sono...",
  "claude_response": "Le API REST rappresentano...",
  "openai_model": "gpt-4o",
  "claude_model": "claude-sonnet-4-5-20250929"
}
```

## 🤖 Creare il Custom GPT

### 1. Deploy del server

Vedi [docs/DEPLOYMENT.md](../../docs/DEPLOYMENT.md) per:
- Ngrok (test rapidi)
- Replit (gratuito permanente)
- Railway / Render (produzione)

### 2. Genera schema OpenAPI

```bash
# Dalla root del progetto
python scripts/generate_openapi_schema.py
```

Questo crea `openapi_schema.json` da usare nel Custom GPT.

### 3. Configura il Custom GPT

Vedi la guida completa: [docs/CUSTOM_GPT_SETUP.md](../../docs/CUSTOM_GPT_SETUP.md)

**Breve:**
1. Vai su ChatGPT → "My GPTs" → "Create a GPT"
2. Configura nome e istruzioni
3. Aggiungi Action con lo schema OpenAPI
4. Configura autenticazione Bearer
5. Testa!

## 💬 Esempi di Prompt per il Custom GPT

Dopo aver configurato il Custom GPT, puoi usare prompt come:

```
Usa OpenAI per spiegarmi il machine learning
```

```
Usa Claude con thinking per risolvere questo problema matematico:
Se ho 100€ e spendo il 30%, poi guadagno il 20% di quello che resta,
quanto ho alla fine?
```

```
Confronta come OpenAI e Claude spiegano cosa sono i Large Language Models
```

## 📝 Istruzioni Esempio per il Custom GPT

```
Tu hai accesso a tre azioni:
1. /openai/chat - Chiama OpenAI GPT (con opzione thinking per o1)
2. /claude/chat - Chiama Claude (con opzione extended thinking)
3. /compare - Confronta entrambi i modelli

Quando usare thinking=true:
- Problemi matematici complessi
- Ragionamento logico multi-step
- Analisi profonde

Workflow:
- Per domande semplici: usa un modello senza thinking
- Per problemi complessi: usa thinking
- Per confronti: usa /compare

Sii chiaro con l'utente su quale modello stai usando e perché.
```

## 🔧 Personalizzazione

### Cambiare i modelli

In `server.py`, modifica:

```python
# Per OpenAI
model = "gpt-4o-mini" if not request.thinking else "o1-mini"

# Per Claude
model="claude-haiku-4-20250514"  # Modello più economico
```

### Aggiungere endpoint

Esempio per aggiungere un endpoint di traduzione:

```python
@app.post("/translate")
async def translate(text: str, target_lang: str):
    client = OpenAIClient()
    prompt = f"Traduci in {target_lang}: {text}"
    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}]
    )
    return {"translation": response.choices[0].message.content}
```

## 📚 Risorse

- **Setup generale:** [docs/QUICKSTART.md](../../docs/QUICKSTART.md)
- **Client Python:** [docs/PYTHON_README.md](../../docs/PYTHON_README.md)
- **Deployment:** [docs/DEPLOYMENT.md](../../docs/DEPLOYMENT.md)
- **Custom GPT setup:** [docs/CUSTOM_GPT_SETUP.md](../../docs/CUSTOM_GPT_SETUP.md)

## 🆘 Troubleshooting

**Server non parte:**
```bash
# Verifica dipendenze
pip install -r requirements.txt
```

**Import Error: No module named 'core':**
```bash
# Esegui dalla root del progetto, non dalla cartella examples
cd /path/to/claude-code-website-test
python examples/openai_claude/server.py
```

**401 Unauthorized:**
- Verifica che CUSTOM_GPT_API_KEY nel .env sia uguale a quella nel Custom GPT

**OpenAI/Claude Error:**
- Verifica che le API keys siano valide
- Controlla di avere crediti

---

**Happy coding!** 🚀
