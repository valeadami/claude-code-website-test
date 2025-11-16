# 🛍️ Custom GPT Customer Care - Esempio Completo

Esempio pratico di **Custom GPT per assistenza clienti** con:
- ✅ Knowledge Base per FAQ e politiche aziendali
- ✅ API Action per controllare stato ordini in tempo reale
- ✅ Dati mockup realistici (8 ordini di esempio)
- ✅ Gestione conversazioni naturali

## 🎯 Scenario d'Uso

**Azienda:** TechShop Italia (e-commerce elettronica)

**Problema:** Clienti che chiamano/scrivono per sapere lo stato degli ordini

**Soluzione:** Chatbot Custom GPT che:
1. Risponde a domande generiche (spedizioni, resi, garanzie) usando la Knowledge Base
2. Recupera stato ordini in tempo reale tramite API Action
3. Conversa in modo naturale e professionale

---

## 🚀 Quick Start (5 minuti)

### 1. Avvia il server

```bash
# Avvia il server customer care
python customer_care_server.py

# Server disponibile su http://localhost:8000
# Documentazione: http://localhost:8000/docs
```

### 2. Testa il server

```bash
# Opzione A: Menu interattivo
python test_customer_care.py

# Opzione B: Quick tests
python test_customer_care.py quick

# Opzione C: Test manuale
curl http://localhost:8000/order/ORD-2025-01
```

### 3. Crea il Custom GPT

Segui la guida completa: [CUSTOMER_CARE_GPT_SETUP.md](CUSTOMER_CARE_GPT_SETUP.md)

**TL;DR:**
1. Crea nuovo GPT in ChatGPT
2. Carica `customer_care_knowledge_base.md` come Knowledge
3. Configura Action con endpoint `/order/{order_id}`
4. Aggiungi autenticazione Bearer
5. Testa!

---

## 📦 Ordini di Esempio Disponibili

| ID Ordine | Status | Descrizione |
|-----------|--------|-------------|
| **ORD-2025-01** | ✅ Consegnato | Laptop, consegnato al portiere |
| **ORD-2025-02** | 🚚 In transito | Mouse + tastiera, con tracking |
| **ORD-2025-03** | 📦 In preparazione | Monitor, nessun tracking ancora |
| **ORD-2025-04** | ❌ Annullato | Cavi, rimborso completato |
| **ORD-2025-05** | 📤 Spedito | Smartphone + accessori (5 articoli) |
| **ORD-2025-06** | ✅ Consegnato | Notebook alto valore |
| **ORD-2025-07** | ⏳ Attesa pagamento | Webcam + microfono |
| **ORD-2025-08** | 🔄 Reso richiesto | Auricolari, reso autorizzato |

---

## 💬 Esempi di Conversazioni

### Scenario 1: Cliente chiede stato ordine

**Cliente:**
```
Ciao, vorrei sapere dov'è il mio pacco
```

**Bot:**
```
Ciao! Sarò felice di aiutarti a tracciare il tuo ordine.
Per controllare lo stato, ho bisogno del codice ordine
(formato ORD-2025-XX). Lo trovi nell'email di conferma
che hai ricevuto dopo l'acquisto. Puoi fornirmelo?
```

**Cliente:**
```
ORD-2025-02
```

**Bot:**
```
Perfetto! Ho controllato il tuo ordine ORD-2025-02:

🚚 Stato: In transito
📦 Data ordine: 12 gennaio 2025
📍 Indirizzo di consegna: Corso Garibaldi 45, Roma, 00100

Prodotti ordinati:
- Mouse Wireless (x2) - €29.99
- Tastiera Meccanica (x1) - €29.52

Totale: €89.50

📍 Tracking: IT987654321
🔗 Puoi tracciare il pacco qui: https://tracking.example.com/IT987654321

📅 Consegna prevista: 18 gennaio 2025

📝 Note: Il pacco è in consegna, arrivo previsto domani

Il tuo pacco è in viaggio e dovrebbe arrivare domani!
Posso aiutarti con altro?
```

---

### Scenario 2: Cliente chiede info spedizioni (usa KB)

**Cliente:**
```
Quanto costa la spedizione?
```

**Bot:**
```
Ecco i costi di spedizione di TechShop:

📦 Spedizione Standard: €4.90 (2-4 giorni lavorativi)
🆓 Spedizione GRATUITA per ordini superiori a €50
⚡ Spedizione Express: €9.90 (1-2 giorni lavorativi)

I tempi sono indicativi per l'Italia continentale.
Per le isole potrebbero essere necessari 1-2 giorni extra.

Stai pensando di fare un ordine? Posso aiutarti con altro?
```

---

### Scenario 3: Ordine annullato

**Cliente:**
```
Controlla ordine ORD-2025-04
```

**Bot:**
```
Ho controllato il tuo ordine ORD-2025-04:

❌ Stato: Annullato
📦 Data ordine: 15 gennaio 2025

Prodotti ordinati:
- Cavo USB-C (x3) - €15.00

Totale: €45.00

❌ Motivo annullamento: Annullato dal cliente il 2025-01-15
💰 Rimborso: Rimborso completato

📝 Note: Il rimborso è stato processato e verrà accreditato
entro 3-5 giorni lavorativi

Il tuo ordine è stato annullato e il rimborso è già stato
processato. Dovresti vedere l'accredito sul tuo metodo di
pagamento originale entro 3-5 giorni lavorativi.

Se hai altre domande sul rimborso, fammi sapere!
```

---

### Scenario 4: Domanda su reso (usa KB)

**Cliente:**
```
Voglio rendere un prodotto, come faccio?
```

**Bot:**
```
Certo! Ecco come fare un reso con TechShop:

🔄 PROCEDURA RESO:
1. Accedi al tuo account su techshop.it
2. Vai su "I miei ordini"
3. Seleziona l'ordine e clicca "Richiedi reso"
4. Stampa l'etichetta di reso che riceverai via email
5. Spedisci il pacco

📋 CONDIZIONI:
- Hai 30 giorni dalla consegna
- Il prodotto deve essere non utilizzato
- Confezione originale integra
- Tutti gli accessori inclusi

💰 RIMBORSO:
Il rimborso viene processato entro 5-7 giorni lavorativi
dalla ricezione del reso.

Hai già ricevuto il prodotto che vuoi rendere? Se sì,
posso aiutarti ad avviare la procedura.
```

---

## 🛠️ Struttura del Progetto

```
.
├── customer_care_server.py           # API server FastAPI
├── customer_care_knowledge_base.md   # KB per il Custom GPT
├── test_customer_care.py             # Test suite
├── CUSTOMER_CARE_GPT_SETUP.md        # Guida setup Custom GPT
└── CUSTOMER_CARE_README.md           # Questo file
```

---

## 🔧 Personalizzazione

### Modificare gli Ordini Mockup

Apri `customer_care_server.py` e modifica il dizionario `MOCK_ORDERS`:

```python
MOCK_ORDERS = {
    "ORD-2025-09": {
        "order_id": "ORD-2025-09",
        "customer_name": "Il Tuo Nome",
        "status": "delivered",
        # ... altri campi
    }
}
```

### Aggiungere Status Personalizzati

Modifica `ORDER_STATUSES` in `customer_care_server.py`:

```python
ORDER_STATUSES = {
    "custom_status": "Descrizione personalizzata",
    # ...
}
```

### Modificare la Knowledge Base

Modifica `customer_care_knowledge_base.md` per:
- Aggiornare politiche aziendali
- Aggiungere FAQ
- Cambiare informazioni di contatto
- Personalizzare il tono

### Cambiare l'Azienda

Sostituisci "TechShop" con il tuo brand in:
1. `customer_care_knowledge_base.md`
2. Istruzioni del Custom GPT
3. `customer_care_server.py` (descrizioni API)

---

## 📊 API Endpoints

### GET /order/{order_id}

Recupera lo stato di un ordine.

**Request:**
```bash
curl -H "Authorization: Bearer sk-customer-care-secret-2025" \
     http://localhost:8000/order/ORD-2025-01
```

**Response 200:**
```json
{
  "success": true,
  "order_id": "ORD-2025-01",
  "status": "delivered",
  "status_description": "Consegnato",
  "order_date": "2025-01-10",
  "total_amount": 149.99,
  "currency": "EUR",
  "items": [...],
  "shipping_address": "Via Roma 123, Milano, 20100",
  "tracking_number": "IT123456789",
  "tracking_url": "https://tracking.example.com/IT123456789",
  "delivery_date": "2025-01-15",
  "notes": "Consegnato al portiere"
}
```

**Response 404:**
```json
{
  "detail": {
    "success": false,
    "error": "order_not_found",
    "message": "Ordine ORD-2025-99 non trovato..."
  }
}
```

### GET /orders/list

Lista tutti gli ordini (solo per testing).

**Response:**
```json
{
  "success": true,
  "total_orders": 8,
  "orders": [...]
}
```

### GET /health

Health check del server.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-16T...",
  "total_orders": 8
}
```

---

## 🧪 Testing

### Test Interattivo

```bash
python test_customer_care.py
```

Menu con opzioni:
1. Quick Tests (essenziali)
2. Full Test Suite (completa)
3. Test singolo ordine
4. Lista tutti gli ordini
5. Health Check

### Quick Tests

```bash
python test_customer_care.py quick
```

Testa:
- Health check
- Root endpoint
- Alcuni ordini esempio
- Ordine non trovato
- Lista ordini

### Full Test Suite

```bash
python test_customer_care.py full
```

Testa tutti gli 8 ordini mockup.

### Test Singolo Ordine

```bash
python test_customer_care.py ORD-2025-05
```

---

## 🚀 Deployment

### Per Testing (Ngrok)

```bash
# Terminale 1
python customer_care_server.py

# Terminale 2
ngrok http 8000
```

Usa l'URL HTTPS di ngrok per configurare il Custom GPT.

### Per Produzione

Vedi [DEPLOYMENT.md](DEPLOYMENT.md) per:
- Replit (gratuito)
- Railway ($5/mese)
- Render (gratuito con limitazioni)

---

## 💡 Casi d'Uso Avanzati

### 1. Integrazione Database Reale

Sostituisci `MOCK_ORDERS` con query a un database:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@app.get("/order/{order_id}")
async def get_order_status(order_id: str):
    # Query al database
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404)
    return order
```

### 2. Autenticazione Cliente

Aggiungi OAuth per identificare il cliente:

```python
@app.get("/order/{order_id}")
async def get_order_status(
    order_id: str,
    current_user: User = Depends(get_current_user)
):
    # Verifica che l'ordine appartenga al cliente
    order = get_order(order_id)
    if order.customer_id != current_user.id:
        raise HTTPException(status_code=403)
    return order
```

### 3. Webhook per Aggiornamenti

Ricevi notifiche dal corriere e aggiorna lo stato:

```python
@app.post("/webhook/tracking")
async def tracking_webhook(data: TrackingUpdate):
    # Aggiorna stato ordine
    update_order_status(data.order_id, data.status)
    # Notifica cliente via email
    send_notification(data.order_id)
```

### 4. Analytics

Traccia le domande più frequenti:

```python
from collections import Counter

queries = Counter()

@app.middleware("http")
async def log_queries(request, call_next):
    if "/order/" in request.url.path:
        queries[request.url.path] += 1
    return await call_next(request)
```

---

## 📈 Metriche di Successo

Con un Custom GPT per customer care puoi:

- ✅ **Ridurre carico supporto** del 60-80% (domande ripetitive)
- ✅ **Risposta 24/7** senza costi aggiuntivi
- ✅ **Tempo di risposta < 5 secondi** (vs minuti/ore via email)
- ✅ **Scalabilità infinita** (gestisce migliaia di richieste simultanee)
- ✅ **Consistenza** nelle risposte (sempre le stesse policy)

---

## 🎓 Lezioni Apprese

### Best Practices

1. **Knowledge Base dettagliata:**
   - Più info dai, meno il GPT inventa
   - Usa esempi concreti
   - Aggiorna regolarmente

2. **Istruzioni chiare:**
   - Definisci il tono di voce
   - Specifica quando usare le Actions
   - Dai esempi di risposte buone/cattive

3. **Gestione errori:**
   - Messaggi amichevoli anche per errori
   - Suggerisci azioni alternative
   - Escalation a umani quando necessario

4. **Testing:**
   - Testa tutti i possibili scenari
   - Includi casi edge
   - Simula clienti frustrati

---

## 🆘 FAQ

**Q: Il GPT può modificare/annullare ordini?**
A: No, per sicurezza solo recupera informazioni. Per modifiche, indirizza al supporto umano.

**Q: Come proteggere i dati dei clienti?**
A: Implementa autenticazione OAuth, filtra ordini per cliente, usa HTTPS, non loggare dati sensibili.

**Q: Cosa succede se l'API è down?**
A: Il GPT dirà che c'è un problema tecnico e indirizzerà al supporto email/telefono.

**Q: Posso usarlo in produzione?**
A: Sì, ma assicurati di:
- Database reale (non mockup)
- Autenticazione robusta
- Logging e monitoring
- Escalation a umani

---

## 📚 Risorse

- **Setup Guide:** [CUSTOMER_CARE_GPT_SETUP.md](CUSTOMER_CARE_GPT_SETUP.md)
- **Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **API Docs:** http://localhost:8000/docs (quando server attivo)

---

## 🎉 Conclusione

Hai ora un esempio completo e funzionante di Custom GPT per customer care!

Puoi usarlo come base per:
- E-commerce
- SaaS customer support
- Help desk aziendale
- FAQ automatizzate
- Ticketing system

**Prossimi step:**
1. Personalizza con i tuoi dati
2. Deploya in produzione
3. Monitora le conversazioni
4. Itera e migliora

Buon chatbot! 🤖🛍️
