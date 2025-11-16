# 🛍️ Setup Custom GPT - Customer Care Bot

Guida completa per creare un **Custom GPT di assistenza clienti** con:
- ✅ Knowledge Base per domande generiche
- ✅ Action per controllare lo stato ordini
- ✅ Risposte personalizzate e professionali

---

## 🎯 Cosa farà il Custom GPT

Il tuo chatbot potrà:

1. **Rispondere a domande generiche:**
   - Politiche di spedizione, resi, garanzie
   - FAQ su ordini, pagamenti, prodotti
   - Informazioni aziendali

2. **Controllare lo stato ordini in tempo reale:**
   - Quando il cliente fornisce un ID ordine (es: ORD-2025-01)
   - Il GPT chiama automaticamente l'API
   - Restituisce stato, tracking, note, etc.

3. **Gestire conversazioni naturali:**
   - "Dov'è il mio pacco?"
   - "Voglio fare un reso"
   - "Quanto costa la spedizione?"

---

## 🚀 Parte 1: Avviare l'API Server

### 1. Testa il server localmente

```bash
# Avvia il server customer care
python customer_care_server.py

# Server disponibile su http://localhost:8000
# Documentazione: http://localhost:8000/docs
```

### 2. Testa manualmente un ordine

```bash
# Testa recupero ordine
curl http://localhost:8000/order/ORD-2025-01

# Lista tutti gli ordini (solo per testing)
curl http://localhost:8000/orders/list

# Health check
curl http://localhost:8000/health
```

### 3. Deploya il server

**Per testing rapido:** Usa Ngrok

```bash
# Terminale 1: Server
python customer_care_server.py

# Terminale 2: Ngrok
ngrok http 8000

# Copia l'URL HTTPS che ti dà ngrok
```

**Per deployment permanente:** Vedi [DEPLOYMENT.md](DEPLOYMENT.md) per Replit, Railway, Render.

---

## 🤖 Parte 2: Creare il Custom GPT

### 1. Vai su ChatGPT

1. Apri [ChatGPT](https://chat.openai.com)
2. Profilo → **"My GPTs"** → **"Create a GPT"**

---

### 2. Tab "Create" - Configurazione Base

#### **Nome:**
```
TechShop Customer Care
```

#### **Descrizione:**
```
Assistente virtuale per il supporto clienti di TechShop Italia.
Risponde a domande su ordini, spedizioni, resi e politiche aziendali.
Può controllare lo stato degli ordini in tempo reale.
```

#### **Istruzioni (Instructions):**

```
# Ruolo
Sei l'assistente virtuale di TechShop Italia, un e-commerce di elettronica e accessori tech.
Il tuo obiettivo è fornire un'assistenza clienti eccellente, professionale e cordiale.

# Tono di Voce
- Cordiale e professionale
- Empatico con i problemi del cliente
- Chiaro e conciso
- Usa un italiano naturale
- Dai del "tu" al cliente (come è standard nel customer care italiano)

# Capacità

## 1. Domande Generiche
Per domande su:
- Spedizioni, costi, tempi di consegna
- Resi e rimborsi
- Politiche aziendali
- FAQ generiche
- Garanzie
- Pagamenti
- Problemi comuni

Usa le informazioni nella Knowledge Base per rispondere.

## 2. Stato Ordini
Quando un cliente chiede informazioni su un ordine:

1. **Richiedi l'ID ordine** se non lo ha fornito
   - Formato: ORD-2025-XX
   - Spiega dove trovarlo ("nella email di conferma")

2. **Usa l'Action** per recuperare lo stato
   - Chiama GET /order/{order_id}

3. **Presenta le informazioni in modo chiaro:**
   - Stato corrente
   - Data ordine
   - Tracking (se disponibile)
   - Data di consegna prevista/effettiva
   - Eventuali note importanti

4. **Fornisci azioni successive:**
   - Link di tracking se disponibile
   - Suggerimenti in base allo stato
   - Istruzioni per eventuali problemi

## 3. Gestione Situazioni Speciali

### Ordine non trovato
Se l'API restituisce errore 404:
- Chiedi al cliente di verificare l'ID
- Suggerisci di controllare l'email di conferma
- Offri alternative (contattare il supporto diretto)

### Ordine in ritardo
Se la data stimata è passata:
- Mostra empatia
- Spiega possibili cause (maltempo, festività, ecc.)
- Suggerisci di contattare il corriere con il tracking
- Offri apertura di segnalazione se ritardo > 5 giorni

### Ordine annullato
- Spiega il motivo (se presente)
- Informa sullo stato del rimborso
- Indica i tempi di accredito

### Reso richiesto
- Conferma lo stato del reso
- Spiega i prossimi step
- Informa sui tempi di rimborso

## 4. Escalation

Quando NON puoi aiutare direttamente:
- Problemi tecnici complessi → tech@techshop.it
- Reclami o situazioni delicate → support@techshop.it
- Richieste di modifica ordine urgenti → Chat live o telefono

## 5. Workflow Tipico

**Cliente:** "Dov'è il mio pacco?"
**Tu:**
1. Saluta e rassicura
2. Chiedi l'ID ordine
3. Recupera lo stato via Action
4. Presenta info + tracking
5. Offri assistenza aggiuntiva

**Cliente:** "Quanto costa la spedizione?"
**Tu:**
1. Consulta KB
2. Spiega costi standard e gratuita sopra €50
3. Menziona opzione express
4. Chiedi se serve altro

# Limitazioni

- NON puoi modificare ordini
- NON puoi processare rimborsi
- NON puoi cambiare indirizzi di spedizione
- NON puoi accedere a informazioni di altri clienti

Per queste operazioni, indirizza al team di supporto.

# Esempi di Risposta

## Buono ✅
"Ciao! Capisco la tua preoccupazione. Per controllare lo stato del tuo ordine,
ho bisogno del codice ordine (formato ORD-2025-XX). Lo trovi nell'email di
conferma che hai ricevuto. Puoi fornirmelo?"

## Da evitare ❌
"Errore: ordine non trovato."

# Note Importanti

- Se qualcosa non è nella KB, ammetti di non sapere e indirizza al supporto
- Mai inventare informazioni
- Mantieni sempre tono positivo anche per cattive notizie
- Privacy: non chiedere mai dati sensibili (password, carta di credito, ecc.)
```

---

### 3. Tab "Configure" - Knowledge Base

1. Scorri fino a **"Knowledge"**
2. Clicca **"Upload files"**
3. Carica il file `customer_care_knowledge_base.md`

Questo darà al GPT tutte le informazioni su politiche, FAQ, ecc.

---

### 4. Tab "Configure" - Actions

1. Scorri fino a **"Actions"**
2. Clicca **"Create new action"**

#### Opzione A: Import da URL

Se hai deployato il server:
```
https://your-url.com/openapi.json
```

#### Opzione B: Schema Manuale

Copia e incolla questo schema OpenAPI:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Customer Care API",
    "description": "API per recuperare stato ordini",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://your-url-here.com"
    }
  ],
  "paths": {
    "/order/{order_id}": {
      "get": {
        "summary": "Recupera lo stato di un ordine",
        "description": "Restituisce informazioni complete su un ordine dato il suo ID",
        "operationId": "getOrderStatus",
        "parameters": [
          {
            "name": "order_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            },
            "description": "ID dell'ordine nel formato ORD-2025-XX"
          }
        ],
        "responses": {
          "200": {
            "description": "Ordine trovato",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "success": {"type": "boolean"},
                    "order_id": {"type": "string"},
                    "status": {"type": "string"},
                    "status_description": {"type": "string"},
                    "order_date": {"type": "string"},
                    "total_amount": {"type": "number"},
                    "currency": {"type": "string"},
                    "items": {"type": "array"},
                    "shipping_address": {"type": "string"},
                    "tracking_number": {"type": "string"},
                    "tracking_url": {"type": "string"},
                    "estimated_delivery": {"type": "string"},
                    "delivery_date": {"type": "string"},
                    "notes": {"type": "string"}
                  }
                }
              }
            }
          },
          "404": {
            "description": "Ordine non trovato"
          }
        },
        "security": [
          {
            "BearerAuth": []
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "API Key"
      }
    }
  }
}
```

**Importante:** Sostituisci `"url": "https://your-url-here.com"` con il tuo URL reale!

---

### 5. Configura Autenticazione

Nella sezione **"Authentication"**:

1. **Auth Type:** API Key
2. **Auth Type:** Bearer
3. **API Key:** `sk-customer-care-secret-2025` (o la tua CUSTOM_GPT_API_KEY dal .env)
4. **Custom Header Name:** `Authorization`

Clicca **"Save"**

---

### 6. Privacy e Pubblicazione

Scegli:
- **Only me** - Solo tu puoi usarlo
- **Anyone with a link** - Condivisibile tramite link
- **Public** - Visibile nello store GPT

Clicca **"Save"** in alto a destra.

---

## 🧪 Parte 3: Testare il Custom GPT

### Test 1: Domanda Generica (usa KB)

```
Quanto costa la spedizione?
```

**Risposta attesa:**
Il GPT dovrebbe spiegare:
- €4.90 standard
- Gratuita sopra €50
- €9.90 express

---

### Test 2: Stato Ordine - Consegnato

```
Vorrei sapere dov'è il mio ordine ORD-2025-01
```

**Risposta attesa:**
```
Ciao! Ho controllato il tuo ordine ORD-2025-01:

✅ Stato: Consegnato
📦 Data consegna: 15 gennaio 2025
📍 Indirizzo: Via Roma 123, Milano, 20100
📝 Note: Consegnato al portiere

Prodotti ordinati:
- Laptop HP (1x) - €149.99

Totale: €149.99

Il tuo ordine è stato consegnato con successo! Se hai problemi con il prodotto
ricevuto, fammi sapere e ti aiuto con il reso o la garanzia.

Posso aiutarti con altro?
```

---

### Test 3: Stato Ordine - In Transito

```
Controlla l'ordine ORD-2025-02
```

**Risposta attesa:**
Info su stato "In transito" + link tracking + data prevista consegna

---

### Test 4: Ordine Non Trovato

```
Ordine ORD-2025-99
```

**Risposta attesa:**
Messaggio cortese che l'ordine non è stato trovato, suggerimenti per verificare l'ID

---

### Test 5: Conversazione Naturale

```
Salve, ho ordinato uno smartphone ma non so quando arriva
```

**Risposta attesa:**
Il GPT dovrebbe:
1. Salutare
2. Chiedere l'ID ordine
3. (Dopo che lo fornisci) Recuperare lo stato
4. Dare info tracking e consegna

---

### Test 6: Domanda su Reso

```
Come faccio a fare un reso?
```

**Risposta attesa:**
Spiegazione procedura reso dalla KB:
- 30 giorni di tempo
- Procedura online
- Condizioni
- Tempi rimborso

---

### Test 7: Ordine Annullato

```
Controlla ORD-2025-04
```

**Risposta attesa:**
Info su annullamento + stato rimborso

---

## 📊 Ordini di Test Disponibili

| ID Ordine | Status | Note |
|-----------|--------|------|
| ORD-2025-01 | Consegnato | Tutto ok |
| ORD-2025-02 | In transito | Con tracking |
| ORD-2025-03 | In preparazione | Nessun tracking ancora |
| ORD-2025-04 | Annullato | Con rimborso |
| ORD-2025-05 | Spedito | 5 articoli |
| ORD-2025-06 | Consegnato | Alto valore |
| ORD-2025-07 | In attesa pagamento | Con link pagamento |
| ORD-2025-08 | Reso richiesto | Con tracking reso |

---

## 🎨 Personalizzazione

### Logo/Avatar
Carica un logo aziendale nella sezione "Profile Picture"

### Nome Display
Usa un nome professionale tipo "TechShop Assistant"

### Conversazione di Esempio
Nella sezione "Conversation starters", aggiungi:
- "Quanto costa la spedizione?"
- "Dov'è il mio ordine?"
- "Come faccio un reso?"
- "Voglio parlare con un operatore"

---

## 🔧 Troubleshooting

### Il GPT non trova l'ordine
- Verifica che il server API sia online
- Controlla che l'URL nell'Action sia corretto
- Verifica l'autenticazione Bearer

### Il GPT inventa informazioni
- Aggiungi alla KB più dettagli
- Rinforza nelle istruzioni di non inventare
- Usa frasi tipo "Se non trovo l'info, ammetto di non sapere"

### Risposte troppo formali/informali
- Modifica il tono nelle Instructions
- Aggiungi esempi di risposte desiderate

### Il GPT non usa l'Action
- Verifica che lo schema OpenAPI sia valido
- Controlla che il server risponda
- Rinforza nelle istruzioni quando usare l'Action

---

## 🚀 Prossimi Step

### Miglioramenti Possibili

1. **Database Reale:**
   - Connetti a un vero database ordini
   - Filtra per email cliente

2. **Più Actions:**
   - Richiedere reso
   - Modificare indirizzo
   - Scaricare fattura

3. **Integrazione CRM:**
   - Salvare conversazioni
   - Analytics sulle domande più frequenti
   - Ticket automatici per escalation

4. **Multilingua:**
   - Supporto inglese, francese, etc.
   - KB tradotta

5. **Autenticazione Cliente:**
   - OAuth per identificare il cliente
   - Mostrare solo i suoi ordini

---

## 📚 Risorse

- **API Documentation:** http://localhost:8000/docs (quando il server è attivo)
- **Knowledge Base:** [customer_care_knowledge_base.md](customer_care_knowledge_base.md)
- **Deploy Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Il tuo chatbot customer care è pronto!** 🎉

Ora hai un assistente AI che risponde 24/7, usa la knowledge base per domande
generiche e chiama le API per dati in tempo reale. Perfetto per scalare il
supporto clienti!
