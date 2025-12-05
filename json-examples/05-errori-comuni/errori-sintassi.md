# Errori Comuni di Sintassi JSON

Questo file mostra gli errori più comuni quando si scrive JSON e come correggerli.

## ❌ ERRORE 1: Virgola finale (Trailing Comma)

### SBAGLIATO:
```json
{
  "nome": "Mario",
  "età": 30,
}
```

### CORRETTO:
```json
{
  "nome": "Mario",
  "età": 30
}
```

**Regola:** NON mettere mai la virgola dopo l'ultimo elemento!

---

## ❌ ERRORE 2: Virgolette singole invece di doppie

### SBAGLIATO:
```json
{
  'nome': 'Mario',
  'età': 30
}
```

### CORRETTO:
```json
{
  "nome": "Mario",
  "età": 30
}
```

**Regola:** Usa SEMPRE virgolette doppie (`"`) per le stringhe e le chiavi!

---

## ❌ ERRORE 3: Chiavi senza virgolette

### SBAGLIATO:
```json
{
  nome: "Mario",
  età: 30
}
```

### CORRETTO:
```json
{
  "nome": "Mario",
  "età": 30
}
```

**Regola:** Le chiavi devono SEMPRE essere tra virgolette doppie!

---

## ❌ ERRORE 4: Commenti nel JSON

### SBAGLIATO:
```json
{
  // Questo è un commento
  "nome": "Mario",
  /* Commento
     multilinea */
  "età": 30
}
```

### CORRETTO:
```json
{
  "_comment": "Puoi usare una chiave speciale per i commenti",
  "nome": "Mario",
  "età": 30
}
```

**Regola:** JSON standard NON supporta commenti! Usa file `.jsonc` o `.json5` se hai bisogno di commenti.

---

## ❌ ERRORE 5: Valori booleani errati

### SBAGLIATO:
```json
{
  "attivo": True,
  "verificato": FALSE,
  "premium": "true"
}
```

### CORRETTO:
```json
{
  "attivo": true,
  "verificato": false,
  "premium": true
}
```

**Regola:** Usa solo `true` o `false` (minuscolo, senza virgolette)!

---

## ❌ ERRORE 6: null errato

### SBAGLIATO:
```json
{
  "valore": Null,
  "altro": NULL,
  "terzo": "null",
  "quarto": None
}
```

### CORRETTO:
```json
{
  "valore": null,
  "altro": null,
  "terzo": null,
  "quarto": null
}
```

**Regola:** Usa solo `null` (minuscolo, senza virgolette)!

---

## ❌ ERRORE 7: Numeri con virgola o separatori

### SBAGLIATO:
```json
{
  "prezzo": "19,99",
  "popolazione": "1.000.000",
  "percentuale": "75,5%"
}
```

### CORRETTO:
```json
{
  "prezzo": 19.99,
  "popolazione": 1000000,
  "percentuale": 75.5
}
```

**Regola:**
- Usa il punto (`.`) come separatore decimale
- NON usare separatori delle migliaia
- NON mettere virgolette intorno ai numeri
- NON includere unità di misura nel numero

---

## ❌ ERRORE 8: Caratteri speciali non escapati

### SBAGLIATO:
```json
{
  "percorso": "C:\Users\Nome",
  "citazione": "Lui disse "ciao"",
  "testo": "Prima riga
Seconda riga"
}
```

### CORRETTO:
```json
{
  "percorso": "C:\\Users\\Nome",
  "citazione": "Lui disse \"ciao\"",
  "testo": "Prima riga\nSeconda riga"
}
```

**Regola:** Usa backslash (`\`) per escapare caratteri speciali:
- `\"` per virgolette
- `\\` per backslash
- `\n` per newline
- `\t` per tab

---

## ❌ ERRORE 9: Chiavi duplicate

### SBAGLIATO:
```json
{
  "id": 1,
  "nome": "Mario",
  "id": 2
}
```

### CORRETTO:
```json
{
  "id": 2,
  "nome": "Mario"
}
```

**Regola:** Ogni chiave deve essere unica in un oggetto!

---

## ❌ ERRORE 10: Valori undefined o funzioni

### SBAGLIATO:
```json
{
  "valore": undefined,
  "funzione": function() { return 42; },
  "data": new Date()
}
```

### CORRETTO:
```json
{
  "valore": null,
  "risultato": 42,
  "data": "2024-12-05T10:30:00Z"
}
```

**Regola:** JSON supporta solo: string, number, boolean, null, object, array!

---

## ✅ Strumenti per Validare JSON

1. **Online:** [jsonlint.com](https://jsonlint.com/)
2. **VS Code:** Estensione "JSON Tools"
3. **Command line:** `jq` tool
4. **Python:**
   ```python
   import json
   json.loads(stringa_json)  # Lancia errore se non valido
   ```
5. **JavaScript:**
   ```javascript
   JSON.parse(stringa_json);  // Lancia errore se non valido
   ```

---

## 📌 Checklist Rapida

Prima di salvare il tuo JSON, verifica:

- [ ] Tutte le stringhe e chiavi usano virgolette doppie (`"`)
- [ ] Nessuna virgola dopo l'ultimo elemento
- [ ] I booleani sono `true` o `false` (minuscolo)
- [ ] null è `null` (minuscolo)
- [ ] I numeri non hanno virgolette
- [ ] Nessun commento nel file
- [ ] Caratteri speciali escapati correttamente
- [ ] Nessuna chiave duplicata
- [ ] Il file è valido su jsonlint.com
