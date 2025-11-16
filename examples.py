"""
Esempi avanzati di utilizzo delle API OpenAI e Claude
"""

from api_client import OpenAIClient, ClaudeClient
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()


def esempio_conversazione_multi_turno():
    """Esempio di conversazione con più scambi (chat history)"""
    print("\n=== CONVERSAZIONE MULTI-TURNO ===\n")

    client = ClaudeClient()

    # Storia della conversazione
    messages = [
        {"role": "user", "content": "Ciao! Mi chiamo Marco e studio informatica."},
    ]

    response = client.create_message(messages)
    assistant_msg = response.content[0].text
    print(f"Claude: {assistant_msg}\n")

    # Aggiungi la risposta dell'assistente alla storia
    messages.append({"role": "assistant", "content": assistant_msg})

    # Secondo messaggio
    messages.append({"role": "user", "content": "Qual è il mio nome e cosa studio?"})

    response = client.create_message(messages)
    assistant_msg = response.content[0].text
    print(f"Claude: {assistant_msg}\n")


def esempio_confronto_modelli():
    """Confronta la stessa domanda su diversi modelli"""
    print("\n=== CONFRONTO MODELLI ===\n")

    prompt = "Spiega il concetto di ricorsione in programmazione con un esempio in Python"

    # OpenAI GPT-4o
    print("--- GPT-4o ---")
    openai_client = OpenAIClient()
    response = openai_client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o-mini"  # Usa mini per velocità
    )
    print(response.choices[0].message.content[:300] + "...\n")

    # Claude Sonnet
    print("--- Claude Sonnet ---")
    claude_client = ClaudeClient()
    response = claude_client.create_message(
        messages=[{"role": "user", "content": prompt}],
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024
    )
    print(response.content[0].text[:300] + "...\n")


def esempio_thinking_complesso():
    """Usa il thinking per un problema che richiede ragionamento"""
    print("\n=== THINKING SU PROBLEMA COMPLESSO ===\n")

    problema = """
    Maria ha 3 anni più di Giovanni. Fra 5 anni, l'età di Maria sarà il doppio
    dell'età che Giovanni aveva 3 anni fa. Quanti anni hanno adesso?
    """

    # Claude con extended thinking
    client = ClaudeClient()
    response = client.create_message(
        messages=[{"role": "user", "content": problema}],
        thinking_enabled=True,
        thinking_budget=8000
    )

    for block in response.content:
        if block.type == "thinking":
            print(f"[PENSIERO DI CLAUDE]:\n{block.thinking}\n")
        elif block.type == "text":
            print(f"[RISPOSTA FINALE]:\n{block.text}\n")


def esempio_streaming_comparato():
    """Mostra lo streaming side-by-side (in sequenza)"""
    print("\n=== STREAMING COMPARATO ===\n")

    prompt = "Scrivi una breve storia di 3 frasi su un robot che impara a dipingere"

    # OpenAI streaming
    print("--- OpenAI (streaming) ---")
    openai_client = OpenAIClient()
    response = openai_client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in response:
        print(chunk, end="", flush=True)
    print("\n")

    # Claude streaming
    print("--- Claude (streaming) ---")
    claude_client = ClaudeClient()
    response = claude_client.create_message(
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in response:
        print(chunk, end="", flush=True)
    print("\n")


def esempio_parametri_temperatura():
    """Mostra l'effetto della temperatura sulla creatività"""
    print("\n=== EFFETTO TEMPERATURA ===\n")

    prompt = "Completa questa frase: Il gatto salì sul..."

    client = OpenAIClient()

    # Temperatura bassa (più deterministico)
    print("--- Temperatura 0.0 (deterministico) ---")
    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    print(response.choices[0].message.content + "\n")

    # Temperatura alta (più creativo)
    print("--- Temperatura 1.5 (creativo) ---")
    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=1.5
    )
    print(response.choices[0].message.content + "\n")


def esempio_system_prompt():
    """Usa un system prompt per modificare il comportamento"""
    print("\n=== SYSTEM PROMPT ===\n")

    # Con Claude, i system prompt si passano come parametro separato
    claude_client = ClaudeClient()

    response = claude_client.create_message(
        messages=[
            {"role": "user", "content": "Spiegami cosa sono i database"}
        ],
        system="Sei un professore universitario che spiega concetti complessi in modo semplice usando analogie con la cucina.",
        max_tokens=2048
    )

    print(response.content[0].text + "\n")


def esempio_max_tokens():
    """Mostra come limitare la lunghezza della risposta"""
    print("\n=== CONTROLLO LUNGHEZZA (max_tokens) ===\n")

    prompt = "Raccontami la storia dell'informatica"

    client = ClaudeClient()

    # Risposta breve
    print("--- Max 100 tokens ---")
    response = client.create_message(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    print(response.content[0].text + "\n")

    # Risposta lunga
    print("--- Max 500 tokens ---")
    response = client.create_message(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    print(response.content[0].text + "\n")


def esempio_error_handling():
    """Mostra come gestire gli errori"""
    print("\n=== GESTIONE ERRORI ===\n")

    from anthropic import APIError, RateLimitError, APIConnectionError

    client = ClaudeClient()

    try:
        # Questo potrebbe fallire se le API keys non sono configurate
        response = client.create_message(
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=100
        )
        print("✓ Richiesta completata con successo\n")

    except RateLimitError as e:
        print(f"✗ Rate limit raggiunto: {e}\n")
        print("Suggerimento: Aspetta qualche secondo e riprova\n")

    except APIConnectionError as e:
        print(f"✗ Errore di connessione: {e}\n")
        print("Suggerimento: Controlla la tua connessione internet\n")

    except APIError as e:
        print(f"✗ Errore API: {e}\n")
        print("Suggerimento: Controlla le tue API keys nel file .env\n")

    except Exception as e:
        print(f"✗ Errore generico: {e}\n")


# Menu principale
def main():
    """Esegue tutti gli esempi"""
    print("=" * 60)
    print("ESEMPI DI UTILIZZO API OPENAI E CLAUDE")
    print("=" * 60)

    esempi = {
        "1": ("Conversazione multi-turno", esempio_conversazione_multi_turno),
        "2": ("Confronto modelli", esempio_confronto_modelli),
        "3": ("Thinking su problema complesso", esempio_thinking_complesso),
        "4": ("Streaming comparato", esempio_streaming_comparato),
        "5": ("Effetto temperatura", esempio_parametri_temperatura),
        "6": ("System prompt", esempio_system_prompt),
        "7": ("Controllo lunghezza (max_tokens)", esempio_max_tokens),
        "8": ("Gestione errori", esempio_error_handling),
        "9": ("Esegui tutti gli esempi", None),
    }

    print("\nScegli un esempio da eseguire:")
    for key, (descrizione, _) in esempi.items():
        print(f"{key}. {descrizione}")

    scelta = input("\nInserisci il numero (o 'q' per uscire): ").strip()

    if scelta.lower() == 'q':
        print("Arrivederci!")
        return

    if scelta == "9":
        # Esegui tutti
        for key, (descrizione, funzione) in esempi.items():
            if funzione:
                try:
                    funzione()
                except Exception as e:
                    print(f"Errore nell'esempio '{descrizione}': {e}\n")
    elif scelta in esempi and esempi[scelta][1]:
        try:
            esempi[scelta][1]()
        except Exception as e:
            print(f"Errore: {e}\n")
    else:
        print("Scelta non valida!")


if __name__ == "__main__":
    main()
