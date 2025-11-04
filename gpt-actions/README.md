# GPT Action per Vale's Data API

Questa cartella contiene la specifica OpenAPI per creare una Custom GPT Action che interagisce con l'API su Render.

## File

- `openapi-spec.json`: Specifica OpenAPI 3.1.0 per la GPT Action

## Cosa modificare domani

### 1. URL del server
Nel file `openapi-spec.json`, sostituisci:
```json
"url": "https://YOUR-RENDER-SERVICE.onrender.com"
```
Con il tuo URL reale di Render.

### 2. Percorsi degli endpoint
Modifica i path (`/api/data`) con i percorsi reali della tua API.

### 3. Schema dei dati
Aggiorna lo schema `DataItem` nella sezione `components/schemas` con i campi effettivi della tua API.

Esempio:
```json
"DataItem": {
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "tuoCampo1": { "type": "string" },
    "tuoCampo2": { "type": "number" }
  }
}
```

### 4. Autenticazione (se necessaria)
Se la tua API richiede autenticazione, aggiungi nella sezione `components`:

```json
"securitySchemes": {
  "ApiKeyAuth": {
    "type": "apiKey",
    "in": "header",
    "name": "X-API-Key"
  }
}
```

E nella root del documento:
```json
"security": [
  {
    "ApiKeyAuth": []
  }
]
```

## Come usare questa specifica con ChatGPT

1. Vai su https://chat.openai.com/gpts/editor
2. Crea un nuovo Custom GPT
3. Nella sezione "Actions", clicca "Create new action"
4. Copia e incolla il contenuto di `openapi-spec.json`
5. Configura l'autenticazione se necessaria
6. Salva e testa la GPT Action

## Operazioni disponibili

Una volta configurato, il tuo Custom GPT potrà:

- **getData**: Leggere tutti i dati dall'API
- **getDataById**: Leggere un dato specifico tramite ID
- **createData**: Creare o modificare dati nell'API

## Test dell'API

Prima di configurare la GPT Action, verifica che gli endpoint funzionino:

```bash
# GET - Ottieni tutti i dati
curl https://YOUR-RENDER-SERVICE.onrender.com/api/data

# GET - Ottieni un dato specifico
curl https://YOUR-RENDER-SERVICE.onrender.com/api/data/123

# POST - Crea/modifica dati
curl -X POST https://YOUR-RENDER-SERVICE.onrender.com/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"test","value":"example"}'
```

## Note

- Il template usa OpenAPI 3.1.0, compatibile con ChatGPT Custom Actions
- Gli esempi sono generici: personalizzali in base alla tua struttura dati
- Se hai domande sulla configurazione, consulta la [documentazione ufficiale di OpenAI](https://platform.openai.com/docs/actions)
