# 🚀 Quick Start - Custom GPT Actions

Guida rapida per iniziare subito con il Custom GPT.

## ⚡ Setup in 5 minuti

### 1. Installa dipendenze
```bash
pip install -r requirements.txt
```

### 2. Configura le API keys
```bash
cp .env.example .env
# Modifica .env e inserisci:
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
# - CUSTOM_GPT_API_KEY (creane una tu, es: sk-custom-abc123)
```

### 3. Testa il client Python
```bash
python api_client.py
```

### 4. Avvia l'API server
```bash
python api_server.py
# Server disponibile su http://localhost:8000
# Documentazione: http://localhost:8000/docs
```

### 5. Testa il server
```bash
# In un altro terminale
python test_api_server.py
```

---

## 🌐 Deploy e Custom GPT (10 minuti)

### Opzione A: Deploy con Ngrok (più veloce)

```bash
# Terminale 1: Avvia il server
python api_server.py

# Terminale 2: Avvia ngrok
ngrok http 8000
# Copia l'URL HTTPS che ti dà (es: https://abc123.ngrok-free.app)
```

### Opzione B: Deploy su Replit (gratuito)

1. Vai su [replit.com](https://replit.com)
2. Crea nuovo Repl Python
3. Carica tutti i file
4. Aggiungi le env vars in "Secrets"
5. Run `python api_server.py`
6. Copia l'URL del Repl

---

## 🤖 Crea il Custom GPT

1. Vai su [ChatGPT](https://chat.openai.com)
2. Profilo → "My GPTs" → "Create a GPT"
3. **Nome:** AI Multi-Model Assistant
4. **Descrizione:**
   ```
   Assistente AI con accesso a OpenAI e Claude.
   Può usare thinking per ragionamento complesso.
   ```

5. **Instructions:**
   ```
   Hai accesso a:
   - /openai/chat (con thinking per o1)
   - /claude/chat (con thinking esteso)
   - /compare (confronta entrambi)

   Usa thinking=true per problemi complessi.
   ```

6. Tab **Configure** → **Actions** → **Create new action**

7. **Schema:** Importa da URL
   ```
   https://[TUO-URL]/openapi.json
   ```
   oppure genera e copia il JSON:
   ```bash
   python generate_openapi_schema.py
   # Copia il contenuto di openapi_schema.json
   ```

8. **Authentication:** API Key
   - Auth Type: Bearer
   - API Key: [La tua CUSTOM_GPT_API_KEY dal .env]

9. **Save** e testa!

---

## 🧪 Test il Custom GPT

Prova questi prompt:

```
Usa OpenAI per spiegarmi le API REST in 2 frasi
```

```
Usa Claude con thinking per risolvere:
Se ho 100€ e spendo il 30%, poi guadagno il 20% di quello che resta,
quanto ho alla fine?
```

```
Confronta come OpenAI e Claude spiegano cos'è un webhook
```

---

## 📚 Documentazione Completa

- **Setup dettagliato:** [CUSTOM_GPT_SETUP.md](CUSTOM_GPT_SETUP.md)
- **Uso del client Python:** [PYTHON_README.md](PYTHON_README.md)

---

## 🆘 Problemi Comuni

**Server non parte:**
```bash
# Verifica dipendenze
pip install -r requirements.txt
```

**401 Unauthorized:**
- La CUSTOM_GPT_API_KEY nel .env deve essere uguale a quella nel Custom GPT

**OpenAI/Claude Error:**
- Verifica che le API keys siano valide
- Controlla di avere crediti

**Custom GPT non vede le Actions:**
- Verifica che l'URL sia HTTPS (non HTTP)
- Ricarica lo schema OpenAPI

---

## ✅ Checklist

- [ ] Installato dipendenze
- [ ] Configurato .env con tutte le keys
- [ ] Testato client Python
- [ ] Avviato server API
- [ ] Testato server con test_api_server.py
- [ ] Deployato server su URL pubblico
- [ ] Generato schema OpenAPI
- [ ] Creato Custom GPT
- [ ] Importato schema Actions
- [ ] Configurato autenticazione
- [ ] Testato Custom GPT

Fatto! 🎉
