# Guida Completa a JSON

## Cos'è JSON?

**JSON** (JavaScript Object Notation) è un formato leggero per lo scambio di dati. È facile da leggere e scrivere per gli umani, e facile da parsare e generare per le macchine.

## Caratteristiche Principali

- **Formato testuale**: è un semplice testo
- **Leggibile**: facile da comprendere
- **Indipendente dal linguaggio**: supportato da quasi tutti i linguaggi di programmazione
- **Strutturato**: organizza i dati in modo gerarchico

## Regole Base

1. I dati sono in coppie **nome/valore**
2. I dati sono separati da **virgole**
3. Le **graffe `{}`** contengono oggetti
4. Le **parentesi quadre `[]`** contengono array
5. Le **chiavi** devono essere stringhe tra virgolette doppie
6. **NO virgola finale** dopo l'ultimo elemento

## Tipi di Dati Supportati

1. **String** (stringa): `"testo"`
2. **Number** (numero): `42` o `3.14`
3. **Boolean** (booleano): `true` o `false`
4. **null**: `null`
5. **Object** (oggetto): `{}`
6. **Array** (array): `[]`

## Struttura dei File di Esempio

### 📁 `01-tipi-base/`
Esempi dei tipi di dati fondamentali

### 📁 `02-oggetti-array/`
Come creare oggetti e array

### 📁 `03-strutture-annidate/`
Strutture complesse con annidamenti

### 📁 `04-casi-reali/`
Esempi pratici di API e applicazioni reali

### 📁 `05-errori-comuni/`
Errori frequenti e come evitarli

## Come Usare Questi Esempi

1. Inizia dai file nella cartella `01-tipi-base`
2. Procedi in ordine numerico
3. Ogni file contiene esempi con commenti esplicativi
4. Prova a modificare gli esempi per sperimentare
5. Valida i tuoi JSON su [jsonlint.com](https://jsonlint.com/)

## Validazione JSON

Per verificare che il tuo JSON sia corretto:
- **Online**: [jsonlint.com](https://jsonlint.com/)
- **Python**: `json.loads(stringa_json)`
- **JavaScript**: `JSON.parse(stringa_json)`
- **VS Code**: estensione "JSON Tools"

## Risorse Utili

- [Specifiche ufficiali JSON](https://www.json.org/)
- [MDN Web Docs - JSON](https://developer.mozilla.org/it/docs/Web/JavaScript/Reference/Global_Objects/JSON)
- [JSON Schema](https://json-schema.org/) - per validare strutture JSON

---

🚀 **Inizia il tuo ripasso da `01-tipi-base/`!**
