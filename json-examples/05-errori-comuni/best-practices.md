# Best Practices per JSON

Linee guida e consigli per scrivere JSON di qualità.

## 🎯 Principi Fondamentali

### 1. Consistenza
Mantieni uno stile coerente in tutto il documento JSON.

**Buono:**
```json
{
  "primo_nome": "Mario",
  "secondo_nome": "Giuseppe",
  "cognome": "Rossi"
}
```

**Da evitare (stili misti):**
```json
{
  "primoNome": "Mario",
  "secondo_nome": "Giuseppe",
  "LastName": "Rossi"
}
```

### 2. Nomenclatura delle Chiavi

**Raccomandazioni:**
- Usa `snake_case` per le chiavi: `first_name`, `user_id`
- Oppure `camelCase`: `firstName`, `userId`
- SCEGLI UNO STILE e usalo ovunque
- Evita caratteri speciali nelle chiavi
- Usa nomi descrittivi e chiari

**Buono:**
```json
{
  "user_id": 123,
  "first_name": "Mario",
  "email_verified": true,
  "created_at": "2024-01-15"
}
```

**Da evitare:**
```json
{
  "uid": 123,
  "fn": "Mario",
  "emlvrfd": true,
  "dt": "2024-01-15"
}
```

---

## 📝 Strutturazione dei Dati

### 3. Usa Array per Liste Omogenee

**Buono:**
```json
{
  "utenti": [
    {"id": 1, "nome": "Mario"},
    {"id": 2, "nome": "Laura"}
  ]
}
```

**Da evitare:**
```json
{
  "utente_1": {"id": 1, "nome": "Mario"},
  "utente_2": {"id": 2, "nome": "Laura"}
}
```

### 4. Raggruppa Dati Correlati

**Buono:**
```json
{
  "utente": {
    "personale": {
      "nome": "Mario",
      "cognome": "Rossi"
    },
    "contatti": {
      "email": "mario@esempio.it",
      "telefono": "+39 123456789"
    }
  }
}
```

**Da evitare (flat senza organizzazione):**
```json
{
  "nome": "Mario",
  "cognome": "Rossi",
  "email": "mario@esempio.it",
  "telefono": "+39 123456789"
}
```

### 5. Limita la Profondità di Annidamento

**Raccomandazione:** Max 3-4 livelli di profondità

**Accettabile:**
```json
{
  "azienda": {
    "dipartimento": {
      "team": {
        "membri": []
      }
    }
  }
}
```

**Troppo annidato (difficile da gestire):**
```json
{
  "livello1": {
    "livello2": {
      "livello3": {
        "livello4": {
          "livello5": {
            "livello6": {}
          }
        }
      }
    }
  }
}
```

---

## 🔢 Gestione dei Valori

### 6. Usa null per Valori Assenti

**Buono:**
```json
{
  "nome": "Mario",
  "secondo_nome": null,
  "cognome": "Rossi"
}
```

**Da evitare:**
```json
{
  "nome": "Mario",
  "secondo_nome": "",
  "cognome": "Rossi"
}
```

**Quando usare cosa:**
- `null`: valore non presente o non applicabile
- `""`: stringa intenzionalmente vuota
- `0`: numero zero (diverso da null!)
- `false`: booleano falso (diverso da null!)

### 7. Formato Date e Orari

**Raccomandato:** Usa ISO 8601

```json
{
  "data_creazione": "2024-12-05T10:30:00Z",
  "data_nascita": "1990-01-15",
  "ora_evento": "14:30:00"
}
```

**Alternative accettabili:**
```json
{
  "timestamp": 1733397000,
  "data_formattata": "05/12/2024"
}
```

### 8. Unità di Misura

Specifica sempre le unità se non ovvie.

**Buono:**
```json
{
  "durata_secondi": 3600,
  "peso_kg": 75.5,
  "temperatura_celsius": 22,
  "prezzo": {
    "valore": 19.99,
    "valuta": "EUR"
  }
}
```

**Ambiguo:**
```json
{
  "durata": 3600,
  "peso": 75.5,
  "temperatura": 22
}
```

---

## 🎨 Formattazione

### 9. Indentazione

**Raccomandato:** 2 spazi per livello

```json
{
  "utente": {
    "nome": "Mario",
    "dettagli": {
      "età": 30,
      "città": "Milano"
    }
  }
}
```

### 10. Usa Pretty Print per Leggibilità

**Sviluppo (leggibile):**
```json
{
  "id": 1,
  "nome": "Mario",
  "attivo": true
}
```

**Produzione (compatto):**
```json
{"id":1,"nome":"Mario","attivo":true}
```

---

## 🔐 Sicurezza

### 11. NON Includere Dati Sensibili

**MAI includere:**
- Password
- Token di autenticazione
- Chiavi API
- Dati di carte di credito
- Informazioni personali sensibili

**Sbagliato:**
```json
{
  "username": "mario",
  "password": "password123",
  "api_key": "sk_live_1234567890"
}
```

**Corretto:**
```json
{
  "username": "mario",
  "password_hash": "$2b$10$...",
  "api_key_hint": "sk_***7890"
}
```

---

## 📊 API Response Best Practices

### 12. Struttura Response Consistente

**Raccomandato:**
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "user": {
      "id": 1,
      "name": "Mario"
    }
  },
  "meta": {
    "timestamp": "2024-12-05T10:30:00Z",
    "request_id": "abc123"
  }
}
```

### 13. Gestione Errori

**Buono:**
```json
{
  "status": "error",
  "code": 400,
  "error": {
    "message": "Email non valida",
    "type": "ValidationError",
    "field": "email",
    "details": "Il formato dell'email non è corretto"
  }
}
```

### 14. Paginazione

**Raccomandato:**
```json
{
  "data": [...],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "per_page": 20,
    "total_items": 200,
    "has_next": true,
    "has_previous": false
  }
}
```

---

## 🚀 Performance

### 15. Minimizza la Dimensione

- Rimuovi campi non necessari
- Usa nomi di chiavi brevi ma chiari
- Considera la compressione (gzip)
- Per produzione, usa formato minificato

### 16. Usa Tipi Appropriati

**Efficiente:**
```json
{
  "id": 123,
  "attivo": true,
  "prezzo": 19.99
}
```

**Inefficiente:**
```json
{
  "id": "123",
  "attivo": "true",
  "prezzo": "19.99"
}
```

---

## ✅ Checklist Finale

Prima di pubblicare il tuo JSON:

- [ ] Validato con tool online (jsonlint.com)
- [ ] Nomenclatura consistente
- [ ] Struttura logica e organizzata
- [ ] Profondità di annidamento ragionevole (max 3-4 livelli)
- [ ] Date in formato ISO 8601
- [ ] Unità di misura specificate quando necessario
- [ ] Nessun dato sensibile
- [ ] Formattazione consistente
- [ ] Documentato (se è uno schema/API)
- [ ] Testato con il codice che lo userà

---

## 📚 Risorse Utili

- [JSON Schema](https://json-schema.org/) - Per validare la struttura
- [JSON API](https://jsonapi.org/) - Specifiche per API REST
- [OpenAPI](https://www.openapis.org/) - Per documentare API
- [JSONLint](https://jsonlint.com/) - Validator online
- [jq](https://stedolan.github.io/jq/) - Tool command-line per JSON
