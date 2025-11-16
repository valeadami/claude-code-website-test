# Setup Custom GPT con Actions

Guida completa per creare un Custom GPT che usa le API di OpenAI e Claude tramite le tue Actions.

## 📋 Prerequisiti

1. Account ChatGPT Plus o Enterprise (necessario per creare Custom GPT)
2. Un server pubblicamente accessibile per le API (vedi sezione Deployment)
3. Chiavi API di OpenAI e Anthropic configurate

## 🚀 Parte 1: Setup Locale

### 1. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2. Configura le variabili d'ambiente

Crea un file `.env` dalla copia di `.env.example`:

```bash
cp .env.example .env
```

Modifica `.env` e inserisci:
- `OPENAI_API_KEY`: La tua chiave OpenAI
- `ANTHROPIC_API_KEY`: La tua chiave Anthropic
- `CUSTOM_GPT_API_KEY`: Una chiave segreta che creerai (es: `sk-custom-abc123xyz789`)

**Importante:** La `CUSTOM_GPT_API_KEY` è una chiave che **tu crei** per proteggere le tue API. Deve essere una stringa casuale e sicura.

### 3. Genera lo schema OpenAPI

```bash
python generate_openapi_schema.py
```

Questo crea il file `openapi_schema.json` che userai per configurare il Custom GPT.

### 4. Testa il server localmente

```bash
python api_server.py
```

Il server parte su `http://localhost:8000`

Apri il browser su:
- **Documentazione interattiva:** http://localhost:8000/docs
- **Schema OpenAPI:** http://localhost:8000/openapi.json

### 5. Testa gli endpoint

```bash
# Health check
curl http://localhost:8000/health

# Chiamata a OpenAI (con autenticazione)
curl -X POST http://localhost:8000/openai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -d '{"prompt": "Spiega cos'\''è FastAPI in 2 frasi", "thinking": false}'
```

---

## 🌐 Parte 2: Deployment (Rendere le API Pubbliche)

Le Custom GPT Actions possono chiamare **solo API pubblicamente accessibili via HTTPS**.

### Opzioni di Deployment:

#### **Opzione A: Ngrok (per test rapidi)**

Ngrok crea un tunnel HTTPS verso il tuo localhost.

```bash
# Installa ngrok
# Vai su https://ngrok.com e crea un account gratuito

# Avvia il server API
python api_server.py

# In un altro terminale, avvia ngrok
ngrok http 8000
```

Ngrok ti darà un URL tipo: `https://abc123.ngrok-free.app`

**Pro:** Veloce per testare
**Contro:** L'URL cambia ogni volta (versione gratuita)

---

#### **Opzione B: Replit (hosting gratuito)**

1. Vai su [Replit](https://replit.com)
2. Crea un nuovo Repl Python
3. Carica tutti i file del progetto
4. Aggiungi le variabili d'ambiente in "Secrets"
5. Esegui `python api_server.py`

Replit ti darà un URL permanente tipo: `https://yourproject.username.repl.co`

---

#### **Opzione C: Railway / Render (hosting cloud)**

Servizi cloud gratuiti con deployment automatico da GitHub.

**Railway:**
1. Collega il tuo repository GitHub
2. Aggiungi le variabili d'ambiente
3. Railway fa il deploy automatico

**Render:**
1. Crea un nuovo Web Service
2. Connetti il repo GitHub
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

---

#### **Opzione D: AWS / GCP / Azure (produzione)**

Per applicazioni in produzione, usa un cloud provider enterprise.

---

## 🤖 Parte 3: Creare il Custom GPT

### 1. Vai su ChatGPT

Apri [ChatGPT](https://chat.openai.com) e clicca su:
- Il tuo profilo (in alto a destra)
- **"My GPTs"**
- **"Create a GPT"**

### 2. Configura il GPT (tab "Create")

**Nome:** AI Assistant with Multi-Model Support

**Descrizione:**
```
Un assistente AI che può usare sia OpenAI che Claude per risolvere problemi complessi.
Può abilitare il ragionamento esteso (thinking) e confrontare le risposte di diversi modelli.
```

**Istruzioni (Instructions):**
```
Tu sei un assistente AI avanzato con accesso a multiple API AI.

Hai accesso a queste azioni:
1. /openai/chat - Chiama OpenAI GPT (con opzione thinking per reasoning complesso)
2. /claude/chat - Chiama Claude (con opzione thinking per ragionamento esteso)
3. /compare - Confronta le risposte di entrambi i modelli

Quando usare thinking=true:
- Problemi matematici complessi
- Ragionamento logico multi-step
- Analisi che richiedono riflessione profonda
- Domande che beneficiano di "pensare ad alta voce"

Workflow suggerito:
1. Per domande semplici, usa un modello senza thinking
2. Per problemi complessi, prova con thinking abilitato
3. Per confronti, usa l'endpoint /compare

Sii chiaro con l'utente su quale modello stai usando e perché.
```

### 3. Configura le Actions (tab "Configure")

1. Clicca su **"Create new action"**
2. Clicca su **"Import from URL"** OPPURE **"Paste JSON"**

#### Opzione A: Import from URL
Se hai deployato il server, inserisci:
```
https://your-domain.com/openapi.json
```

#### Opzione B: Paste JSON
Apri il file `openapi_schema.json` e copia tutto il contenuto.

### 4. Configura l'Autenticazione

Dopo aver importato lo schema:

1. Nella sezione **"Authentication"**, seleziona **"API Key"**
2. Configura:
   - **Auth Type:** Bearer
   - **API Key:** La tua `CUSTOM_GPT_API_KEY` (quella che hai messo nel `.env`)
   - **Custom Header Name:** `Authorization`
3. Clicca **"Save"**

### 5. Configura la Privacy

Scegli chi può usare il tuo GPT:
- **Only me:** Solo tu
- **Anyone with a link:** Chiunque abbia il link
- **Public:** Visibile nel GPT Store

### 6. Salva e Testa

Clicca **"Save"** in alto a destra.

---

## 🧪 Parte 4: Testare il Custom GPT

Prova questi prompt nel tuo Custom GPT:

### Test 1: Chiamata semplice a OpenAI
```
Usa OpenAI per spiegarmi cos'è il machine learning in 3 frasi
```

### Test 2: Chiamata con thinking
```
Usa Claude con thinking abilitato per risolvere questo problema:
Se un treno parte alle 10:00 a 120 km/h e un altro alle 10:30 a 100 km/h
da città distanti 600 km, quando si incontrano?
```

### Test 3: Confronto modelli
```
Confronta come OpenAI e Claude spiegano la differenza tra AI e Machine Learning
```

---

## 🔧 Troubleshooting

### Errore: "Action failed to execute"
- Verifica che il server sia online e pubblicamente accessibile
- Controlla i log del server per errori
- Verifica che l'API Key sia corretta

### Errore: "Unauthorized" (401)
- La `CUSTOM_GPT_API_KEY` nel `.env` deve coincidere con quella nel Custom GPT
- Verifica che l'autenticazione sia configurata come "Bearer" nel GPT

### Errore: "OpenAI Error" o "Claude Error"
- Verifica che `OPENAI_API_KEY` e `ANTHROPIC_API_KEY` siano valide
- Controlla di avere crediti sufficienti negli account

### Il Custom GPT non vede le Actions
- Ricarica lo schema OpenAPI
- Verifica che l'URL del server sia HTTPS (non HTTP)
- Controlla che il server risponda a `/openapi.json`

---

## 📊 Monitoraggio e Logging

Per vedere cosa sta succedendo, il server FastAPI logga tutte le richieste.

Quando il Custom GPT chiama le tue API vedrai nei log:
```
INFO:     127.0.0.1:12345 - "POST /openai/chat HTTP/1.1" 200 OK
```

---

## 💡 Prossimi Passi

Una volta che il Custom GPT funziona, puoi:

1. **Aggiungere più endpoint:**
   - Ricerca web
   - Analisi di immagini
   - Generazione di codice
   - Accesso a database

2. **Migliorare l'autenticazione:**
   - OAuth 2.0
   - Rate limiting
   - User tracking

3. **Aggiungere cache:**
   - Redis per risposte frequenti
   - Ridurre costi API

4. **Monitoraggio avanzato:**
   - Sentry per errori
   - Logging strutturato
   - Metriche di utilizzo

---

## 📚 Risorse Utili

- [Custom GPT Documentation](https://help.openai.com/en/articles/8554397-creating-a-gpt)
- [OpenAPI Specification](https://swagger.io/specification/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ngrok Setup](https://ngrok.com/docs/getting-started/)

---

## 🎯 Riepilogo

1. ✅ Configura le chiavi API nel `.env`
2. ✅ Genera lo schema OpenAPI con `generate_openapi_schema.py`
3. ✅ Deploya il server su un URL pubblico HTTPS
4. ✅ Crea il Custom GPT in ChatGPT
5. ✅ Importa lo schema OpenAPI nelle Actions
6. ✅ Configura l'autenticazione Bearer con la tua API key
7. ✅ Testa il GPT con vari prompt

Buon divertimento con il tuo Custom GPT! 🚀
