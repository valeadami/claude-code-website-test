# Progetto API Python - OpenAI & Claude

Progetto per imparare e sperimentare con le API di OpenAI e Claude (Anthropic), con supporto per parametri di pensiero (thinking) e streaming.

## Setup Iniziale

### 1. Installazione Dipendenze

```bash
pip install -r requirements.txt
```

### 2. Configurazione Chiavi API

Copia il file `.env.example` in `.env`:

```bash
cp .env.example .env
```

Poi modifica `.env` e inserisci le tue chiavi API:
- **OpenAI**: Ottieni la chiave da [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic**: Ottieni la chiave da [Anthropic Console](https://console.anthropic.com/settings/keys)

### 3. Configurazione Visual Studio Code

Installa l'estensione Python per VS Code se non l'hai già:
1. Apri VS Code
2. Vai su Extensions (Ctrl+Shift+X)
3. Cerca "Python" e installa l'estensione ufficiale di Microsoft

## Utilizzo

### Esempi Base

```python
from api_client import OpenAIClient, ClaudeClient

# Inizializza i client (usano automaticamente le variabili d'ambiente)
openai_client = OpenAIClient()
claude_client = ClaudeClient()

# Chat semplice con OpenAI
messages = [{"role": "user", "content": "Ciao! Come funzionano le reti neurali?"}]
response = openai_client.chat_completion(messages)
print(response.choices[0].message.content)

# Chat semplice con Claude
messages = [{"role": "user", "content": "Ciao! Come funzionano le reti neurali?"}]
response = claude_client.create_message(messages)
print(response.content[0].text)
```

### Esempi con Thinking (Ragionamento Esteso)

#### OpenAI con modello o1 (reasoning)

```python
from api_client import OpenAIClient

client = OpenAIClient()
messages = [
    {
        "role": "user",
        "content": "Risolvi: Un treno parte da Milano alle 10:00 e viaggia a 120 km/h. Un altro treno parte da Roma (600 km di distanza) alle 10:30 e viaggia a 100 km/h verso Milano. A che ora si incontrano?"
    }
]

# Usa thinking_enabled=True per usare il modello o1
response = client.chat_completion(
    messages=messages,
    thinking_enabled=True
)

print(response.choices[0].message.content)
```

#### Claude con Extended Thinking

```python
from api_client import ClaudeClient

client = ClaudeClient()
messages = [
    {
        "role": "user",
        "content": "Analizza questo problema logico: 3 interruttori controllano 3 lampadine in un'altra stanza. Puoi azionare gli interruttori quanto vuoi, ma puoi entrare nella stanza solo una volta. Come fai a capire quale interruttore controlla quale lampadina?"
    }
]

response = client.create_message(
    messages=messages,
    thinking_enabled=True,
    thinking_budget=5000  # Budget di token per il pensiero
)

# Claude restituisce sia il pensiero che la risposta
for block in response.content:
    if block.type == "thinking":
        print(f"[PENSIERO]: {block.thinking}\n")
    elif block.type == "text":
        print(f"[RISPOSTA]: {block.text}\n")
```

### Esempi con Streaming

#### Streaming con OpenAI

```python
from api_client import OpenAIClient

client = OpenAIClient()
messages = [{"role": "user", "content": "Raccontami una breve storia"}]

response = client.chat_completion(
    messages=messages,
    stream=True
)

# Stampa chunk per chunk
for chunk in response:
    print(chunk, end="", flush=True)
```

#### Streaming con Claude

```python
from api_client import ClaudeClient

client = ClaudeClient()
messages = [{"role": "user", "content": "Raccontami una breve storia"}]

response = client.create_message(
    messages=messages,
    stream=True
)

# Stampa chunk per chunk
for chunk in response:
    print(chunk, end="", flush=True)
```

### Funzioni Rapide (Quick Functions)

Per test veloci, puoi usare le funzioni di utilità:

```python
from api_client import quick_openai_chat, quick_claude_chat

# Test rapido OpenAI
response = quick_openai_chat("Cosa sono i Large Language Models?")
print(response)

# Test rapido Claude con thinking
response = quick_claude_chat(
    "Spiega la differenza tra supervised e unsupervised learning",
    thinking=True
)
print(response)

# Test con streaming
quick_claude_chat("Scrivi una poesia breve", stream=True)
```

## Eseguire il File di Test

Il file `api_client.py` include esempi di utilizzo nel blocco `if __name__ == "__main__"`:

```bash
python api_client.py
```

## Parametri Principali

### OpenAI

- `model`: Modello da usare (es: `gpt-4o`, `gpt-4o-mini`, `o1`, `o1-mini`)
- `temperature`: Controllo della creatività (0.0 = deterministico, 2.0 = molto creativo)
- `max_tokens`: Limite di token nella risposta
- `stream`: Abilita streaming
- `thinking_enabled`: Passa automaticamente ai modelli o1 con reasoning

### Claude

- `model`: Modello da usare (es: `claude-sonnet-4-5-20250929`, `claude-opus-4-20250514`)
- `temperature`: Controllo della creatività (0.0 - 1.0)
- `max_tokens`: Limite di token nella risposta (richiesto)
- `stream`: Abilita streaming
- `thinking_enabled`: Abilita extended thinking
- `thinking_budget`: Budget di token per il pensiero (default: 10000)

## Modelli Disponibili (Marzo 2025)

### OpenAI
- **GPT-4o**: Modello più capace, multimodale
- **GPT-4o-mini**: Versione più veloce ed economica
- **o1**: Modello con reasoning avanzato
- **o1-mini**: Versione più economica con reasoning

### Anthropic (Claude)
- **claude-sonnet-4-5-20250929**: Ultimo modello Sonnet, bilanciato
- **claude-opus-4-20250514**: Modello più potente
- **claude-haiku-4-20250514**: Modello più veloce ed economico

## Tips per VS Code

1. Usa il Python debugger integrato (F5) per debug interattivo
2. Installa l'estensione "Python Docstring Generator" per documentazione rapida
3. Usa Pylance per type checking e autocompletamento
4. Configura un virtual environment per isolare le dipendenze

## Prossimi Passi

1. Sperimenta con diversi modelli e parametri
2. Prova conversazioni multi-turno (aggiungi messaggi alla lista)
3. Esplora le funzionalità di vision (GPT-4o supporta immagini)
4. Implementa tool/function calling per estendere le capacità dei modelli
5. Crea applicazioni più complesse combinando le API

## Risorse Utili

- [Documentazione OpenAI API](https://platform.openai.com/docs)
- [Documentazione Anthropic API](https://docs.anthropic.com)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Anthropic Claude Prompt Library](https://docs.anthropic.com/claude/prompt-library)
