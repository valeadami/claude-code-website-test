# 🌐 Guida al Deployment

Guida pratica per deployare l'API server e testare il Custom GPT.

---

## ⚡ Opzione 1: Ngrok (5 minuti - La più veloce)

**Perfetto per:** Test rapidi e sviluppo locale

**Pro:**
- Setup in 2 minuti
- Non serve caricare codice da nessuna parte
- Gratuito

**Contro:**
- L'URL cambia ogni volta che riavvii (versione gratuita)
- Serve lasciare il computer acceso

### Setup Ngrok:

#### 1. Installa Ngrok

**Windows/Mac:**
```bash
# Vai su https://ngrok.com/download
# Scarica e installa per il tuo OS
```

**Linux:**
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

#### 2. Configura Ngrok

```bash
# Vai su https://dashboard.ngrok.com/get-started/your-authtoken
# Copia il tuo token e eseguilo:
ngrok config add-authtoken <YOUR_TOKEN>
```

#### 3. Avvia il Server API

**Terminale 1:**
```bash
python api_server.py
```

#### 4. Avvia Ngrok

**Terminale 2:**
```bash
# Opzione A: Usa lo script
./deploy_ngrok.sh

# Opzione B: Comando manuale
ngrok http 8000
```

#### 5. Copia l'URL

Ngrok ti mostrerà qualcosa tipo:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```

**Copia l'URL HTTPS** (es: `https://abc123.ngrok-free.app`)

#### 6. Testa l'URL

```bash
# Testa che funzioni
curl https://abc123.ngrok-free.app/health
```

#### 7. Usa nel Custom GPT

Quando configuri le Actions nel Custom GPT, usa:
```
https://abc123.ngrok-free.app/openapi.json
```

**Importante:** Ogni volta che riavvii ngrok, l'URL cambia e devi aggiornarlo nel Custom GPT.

---

## 🔥 Opzione 2: Replit (10 minuti - URL permanente gratuito)

**Perfetto per:** Demo e prototipi condivisibili

**Pro:**
- Gratuito
- URL permanente
- Editor online
- Non serve un server

**Contro:**
- Limite di risorse (versione gratuita)
- Il container si spegne dopo inattività

### Setup Replit:

#### 1. Crea account su Replit

Vai su [replit.com](https://replit.com) e registrati (gratuito)

#### 2. Crea un nuovo Repl

1. Clicca **"+ Create Repl"**
2. Seleziona **"Python"** come template
3. Nome: `custom-gpt-api` (o quello che vuoi)
4. Clicca **"Create Repl"**

#### 3. Carica i file

**Opzione A - Via Git (consigliata):**

Nel terminale di Replit:
```bash
git clone https://github.com/valeadami/claude-code-website-test.git .
```

**Opzione B - Upload manuale:**

Carica questi file dal tuo progetto:
- `api_server.py`
- `api_client.py`
- `requirements.txt`
- `.replit` (già creato)
- `replit.nix` (già creato)

#### 4. Configura le Variabili d'Ambiente

Nella sidebar sinistra di Replit:
1. Clicca sull'icona 🔒 **"Secrets"**
2. Aggiungi tre secrets:
   - Key: `OPENAI_API_KEY`, Value: `sk-proj-...`
   - Key: `ANTHROPIC_API_KEY`, Value: `sk-ant-...`
   - Key: `CUSTOM_GPT_API_KEY`, Value: `sk-custom-...` (creane una tu)

#### 5. Esegui il Server

Clicca il pulsante verde **"Run"** in alto.

Il server partirà e Replit ti mostrerà l'URL tipo:
```
https://custom-gpt-api.yourname.repl.co
```

#### 6. Testa l'URL

Apri nel browser:
```
https://custom-gpt-api.yourname.repl.co/docs
```

Dovresti vedere la documentazione FastAPI.

#### 7. Usa nel Custom GPT

Quando configuri le Actions, usa:
```
https://custom-gpt-api.yourname.repl.co/openapi.json
```

**Nota:** L'URL rimane lo stesso per sempre!

---

## 🚂 Opzione 3: Railway (15 minuti - Hosting professionale)

**Perfetto per:** Produzione leggera, sempre online

**Pro:**
- $5 di credito gratuito al mese
- Deploy automatico da GitHub
- Always-on (non si spegne)
- Molto affidabile

**Contro:**
- Richiede carta di credito (non viene addebitato se resti sotto $5)

### Setup Railway:

#### 1. Push su GitHub

Assicurati che il tuo codice sia su GitHub:
```bash
# Se non l'hai già fatto
git add .
git commit -m "Ready for deployment"
git push
```

#### 2. Crea account Railway

1. Vai su [railway.app](https://railway.app)
2. Clicca **"Login"** e usa GitHub
3. Collega la carta (non verrà addebitato nulla sotto $5/mese)

#### 3. Crea nuovo Progetto

1. Clicca **"New Project"**
2. Seleziona **"Deploy from GitHub repo"**
3. Autorizza Railway ad accedere a GitHub
4. Seleziona il repository `claude-code-website-test`

#### 4. Configura le Variabili d'Ambiente

1. Clicca sul servizio appena creato
2. Vai su **"Variables"**
3. Aggiungi:
   ```
   OPENAI_API_KEY=sk-proj-...
   ANTHROPIC_API_KEY=sk-ant-...
   CUSTOM_GPT_API_KEY=sk-custom-...
   PORT=8000
   ```

#### 5. Configura il Deploy

Railway rileverà automaticamente che è un progetto Python.

Se non parte automaticamente, vai su **"Settings"** e imposta:
- **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

#### 6. Deploy

Railway farà il deploy automaticamente. Aspetta qualche minuto.

#### 7. Ottieni l'URL

1. Vai su **"Settings"** del servizio
2. Nella sezione **"Domains"**, clicca **"Generate Domain"**
3. Railway ti darà un URL tipo: `https://yourapp.railway.app`

#### 8. Testa

```bash
curl https://yourapp.railway.app/health
```

#### 9. Usa nel Custom GPT

```
https://yourapp.railway.app/openapi.json
```

**Nota:** Ogni push su GitHub farà un re-deploy automatico!

---

## 🎨 Opzione 4: Render (15 minuti - Gratuito permanente)

**Perfetto per:** Progetti personali gratuiti

**Pro:**
- Piano gratuito permanente
- Deploy da GitHub
- SSL automatico

**Contro:**
- Si spegne dopo 15 minuti di inattività (si riavvia al primo accesso)
- Avvio lento (cold start)

### Setup Render:

#### 1. Crea account Render

Vai su [render.com](https://render.com) e registrati con GitHub

#### 2. Crea nuovo Web Service

1. Dashboard → **"New +"** → **"Web Service"**
2. Connetti il repository GitHub
3. Seleziona `claude-code-website-test`

#### 3. Configura il Service

- **Name:** `custom-gpt-api`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

#### 4. Seleziona il piano

Scegli **"Free"** (gratuito)

#### 5. Aggiungi Environment Variables

Nella sezione **"Environment"**, aggiungi:
```
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
CUSTOM_GPT_API_KEY=sk-custom-...
```

#### 6. Deploy

Clicca **"Create Web Service"**

Render farà il build e deploy (5-10 minuti la prima volta).

#### 7. Ottieni l'URL

Render ti darà un URL tipo:
```
https://custom-gpt-api.onrender.com
```

#### 8. Usa nel Custom GPT

```
https://custom-gpt-api.onrender.com/openapi.json
```

**Nota:** Il servizio gratuito si spegne dopo 15 minuti di inattività. Il primo accesso dopo il risveglio sarà lento (30 secondi).

---

## 📊 Confronto Opzioni

| Opzione | Velocità Setup | Costo | URL Permanente | Always-On | Adatto per |
|---------|---------------|-------|----------------|-----------|------------|
| **Ngrok** | ⚡⚡⚡ 2 min | Gratis | ❌ | ❌ | Test rapidi |
| **Replit** | ⚡⚡ 10 min | Gratis | ✅ | ⚠️ | Demo/Prototipi |
| **Railway** | ⚡ 15 min | $5/mese | ✅ | ✅ | Produzione |
| **Render** | ⚡ 15 min | Gratis | ✅ | ⚠️ | Progetti personali |

---

## 🧪 Dopo il Deploy - Testing

Indipendentemente dall'opzione scelta, testa sempre:

### 1. Health Check
```bash
curl https://your-url.com/health
```

Dovrebbe rispondere:
```json
{"status": "healthy"}
```

### 2. Documentazione API
Apri nel browser:
```
https://your-url.com/docs
```

Dovresti vedere l'interfaccia Swagger.

### 3. Test Endpoint (con autenticazione)
```bash
curl -X POST https://your-url.com/openai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-api-key" \
  -d '{
    "prompt": "Ciao! Come stai?",
    "thinking": false
  }'
```

### 4. Schema OpenAPI
```bash
curl https://your-url.com/openapi.json
```

Deve restituire un JSON valido.

---

## 🔧 Troubleshooting

### Errore "Internal Server Error"
- Controlla i log del servizio
- Verifica che le environment variables siano configurate
- Controlla che requirements.txt sia installato correttamente

### Errore "Unauthorized" nel Custom GPT
- Verifica che la `CUSTOM_GPT_API_KEY` sia la stessa nel server e nel GPT
- Controlla che l'autenticazione nel GPT sia "Bearer"

### Il Custom GPT non vede gli endpoint
- Verifica che l'URL finisca con `/openapi.json`
- L'URL deve essere HTTPS (non HTTP)
- Prova a ricaricare lo schema nel Custom GPT

### Performance lente
- Render Free: normale (cold start)
- Replit Free: normale dopo inattività
- Considera Railway se serve sempre-on

---

## 💡 Raccomandazione

**Per iniziare subito:** Usa **Ngrok** (2 minuti)

**Per condividere il GPT:** Usa **Replit** o **Render** (URL permanente gratuito)

**Per uso serio:** Usa **Railway** ($5/mese, sempre online)

---

## 📚 Prossimi Passi

Dopo il deploy:
1. ✅ Testa tutti gli endpoint
2. ✅ Genera lo schema OpenAPI: `python generate_openapi_schema.py`
3. ✅ Configura il Custom GPT (vedi [CUSTOM_GPT_SETUP.md](CUSTOM_GPT_SETUP.md))
4. ✅ Testa il Custom GPT
5. 🚀 Divertiti!
