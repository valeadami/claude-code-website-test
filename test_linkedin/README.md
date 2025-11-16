# LinkedIn API Test

Progetto per testare le API di LinkedIn con Python. Permette di autenticarsi, recuperare dati del profilo e pubblicare post.

## Funzionalità

- **Autenticazione OAuth 2.0**: Login sicuro tramite LinkedIn
- **Recupero profilo**: Ottieni dati base del tuo profilo (nome, email, foto)
- **Pubblicazione post**: Crea post testuali o con link sul tuo profilo

## Limitazioni delle API LinkedIn

**IMPORTANTE**: Le API di LinkedIn sono molto limitate:

- ❌ **NON puoi** leggere i post esistenti (né tuoi né di altri)
- ❌ **NON puoi** accedere ai profili di altri utenti
- ❌ **NON puoi** cercare utenti o aziende
- ✅ **PUOI** autenticarti e ottenere dati base del tuo profilo
- ✅ **PUOI** pubblicare nuovi post

## Requisiti

- Python 3.7+
- Account LinkedIn
- App LinkedIn registrata (vedi Setup)

## Setup

### 1. Crea un'app LinkedIn

1. Vai a [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Clicca su "Create app"
3. Compila i dati richiesti:
   - **App name**: LinkedIn API Test (o un nome a tua scelta)
   - **LinkedIn Page**: Seleziona o crea una pagina LinkedIn
   - **App logo**: Carica un'immagine (puoi usare una qualsiasi)
   - **Legal agreement**: Accetta i termini

4. Dopo la creazione, vai sulla tab **"Auth"**:
   - Copia il **Client ID**
   - Copia il **Client Secret**
   - In **"Redirect URLs"** aggiungi: `http://localhost:5000/callback`

5. Vai sulla tab **"Products"** e richiedi:
   - **"Sign In with LinkedIn using OpenID Connect"** (approvazione immediata)
   - **"Share on LinkedIn"** (approvazione immediata)

### 2. Configura il progetto

```bash
# Vai nella cartella del progetto
cd test_linkedin

# Installa le dipendenze
pip install -r requirements.txt

# Copia il file .env.example in .env
cp .env.example .env

# Modifica il file .env e inserisci le tue credenziali
# LINKEDIN_CLIENT_ID=il_tuo_client_id
# LINKEDIN_CLIENT_SECRET=il_tuo_client_secret
```

### 3. Modifica il file .env

Apri il file `.env` e inserisci i valori ottenuti dal Developer Portal:

```env
LINKEDIN_CLIENT_ID=il_tuo_client_id_qui
LINKEDIN_CLIENT_SECRET=il_tuo_client_secret_qui
LINKEDIN_REDIRECT_URI=http://localhost:5000/callback
```

## Utilizzo

### Step 1: Autenticazione

Esegui prima lo script di autenticazione per ottenere l'access token:

```bash
python linkedin_auth.py
```

1. Il server si avvierà su `http://localhost:5000`
2. Apri il browser e vai a quell'indirizzo
3. Clicca su "Accedi con LinkedIn"
4. Autorizza l'applicazione
5. Verrai reindirizzato alla pagina di successo
6. Il token verrà salvato automaticamente nel file `.env`

**Nota**: Il token scade dopo alcune ore. Se ottieni errori di autenticazione, riesegui questo script.

### Step 2: Recupera i dati del profilo

```bash
python linkedin_profile.py
```

Questo script recupera e visualizza:
- ID utente
- Nome e cognome
- Email
- Foto profilo

**Output esempio:**
```
==============================================================
DATI PROFILO LINKEDIN
==============================================================

ID Utente:        ABC123XYZ
Nome:             Mario
Cognome:          Rossi
Nome completo:    Mario Rossi
Email:            mario.rossi@example.com
Email verificata: True
Foto profilo:     https://media.licdn.com/...
```

### Step 3: Pubblica un post

```bash
python linkedin_posts.py
```

Questo script offre un menu interattivo:

1. **Post di solo testo**: Scrivi un messaggio testuale
2. **Post con link**: Condividi un link con testo
3. **Test**: Pubblica un post di prova (visibile solo ai tuoi collegamenti)

**Esempio post di testo:**
```
Scegli il tipo di post da pubblicare:

1. Post di solo testo
2. Post con link
3. Test (post di prova)
0. Esci

Scelta: 1

--- Post di solo testo ---
Inserisci il testo del post: Ciao LinkedIn! Questo è un test delle API

Visibilità:
1. PUBLIC (pubblico)
2. CONNECTIONS (solo collegamenti)
Scelta: 2

📤 Pubblicazione in corso...

✅ Post pubblicato con successo!
```

## Struttura del progetto

```
test_linkedin/
├── README.md                 # Questa guida
├── requirements.txt          # Dipendenze Python
├── .env.example             # Template configurazione
├── .env                     # Configurazione (da creare)
├── linkedin_auth.py         # OAuth 2.0 authentication
├── linkedin_profile.py      # Recupero dati profilo
└── linkedin_posts.py        # Pubblicazione post
```

## Scope OAuth utilizzati

- `openid`: Autenticazione base
- `profile`: Accesso a nome e foto profilo
- `email`: Accesso all'indirizzo email
- `w_member_social`: Permesso di scrivere post

## Troubleshooting

### Errore: "Access token non trovato"
- Esegui prima `linkedin_auth.py` per ottenere il token
- Verifica che il file `.env` contenga `LINKEDIN_ACCESS_TOKEN`

### Errore: "401 Unauthorized"
- Il token potrebbe essere scaduto, riesegui `linkedin_auth.py`
- Verifica che gli scope siano corretti nell'app LinkedIn

### Errore: "redirect_uri_mismatch"
- Verifica che l'URL di redirect in `.env` corrisponda a quello configurato nell'app LinkedIn
- Deve essere esattamente: `http://localhost:5000/callback`

### Errore nella pubblicazione post
- Verifica di avere il prodotto "Share on LinkedIn" abilitato nell'app
- Controlla di avere lo scope `w_member_social`

## Limitazioni e Note

1. **Token expiration**: L'access token scade (solitamente dopo 60 giorni). Dovrai rieseguire l'autenticazione.

2. **Rate limiting**: LinkedIn limita il numero di richieste API. Se fai troppe richieste potresti essere temporaneamente bloccato.

3. **Dati limitati**: Puoi accedere solo ai tuoi dati base. Non è possibile:
   - Leggere post esistenti
   - Accedere a profili di altri utenti
   - Cercare profili o aziende
   - Ottenere statistiche dettagliate

4. **Prodotti LinkedIn**: Alcune funzionalità richiedono l'approvazione di prodotti specifici (es. Marketing Developer Platform).

## Risorse utili

- [LinkedIn API Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
- [OAuth 2.0 Guide](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [Share API Documentation](https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)

## Licenza

Questo progetto è solo per scopi educativi e di test.
