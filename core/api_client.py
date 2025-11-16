"""
Client per interagire con le API di OpenAI e Claude (Anthropic)
Supporta parametri di pensiero (thinking) e streaming
"""

import os
from typing import Optional, Dict, Any, Iterator
from openai import OpenAI
from anthropic import Anthropic


class OpenAIClient:
    """Client per le API di OpenAI con supporto per thinking e streaming"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inizializza il client OpenAI

        Args:
            api_key: Chiave API OpenAI (se None, usa la variabile d'ambiente OPENAI_API_KEY)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        thinking_enabled: bool = False,
        **kwargs
    ) -> Any:
        """
        Esegue una chat completion con OpenAI

        Args:
            messages: Lista di messaggi nel formato [{"role": "user", "content": "..."}]
            model: Modello da usare (es: gpt-4o, gpt-4o-mini, o1, o1-mini)
            temperature: Temperatura per la generazione (0.0 - 2.0)
            max_tokens: Numero massimo di token da generare
            stream: Se True, abilita lo streaming della risposta
            thinking_enabled: Se True, usa modelli con capacità di ragionamento esteso
            **kwargs: Altri parametri da passare all'API

        Returns:
            Risposta dell'API (oggetto ChatCompletion o Stream)
        """
        # Se thinking_enabled è True, usa i modelli della serie o1
        if thinking_enabled:
            if model.startswith("gpt"):
                model = "o1"  # Passa al modello o1 che supporta il reasoning
            # I modelli o1 hanno parametri predefiniti ottimizzati
            # Rimuovi temperature se si usa o1
            if model.startswith("o1"):
                kwargs.pop("temperature", None)
                temperature = None

        params = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }

        # Aggiungi parametri opzionali solo se specificati
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**params)

        if stream:
            return self._handle_stream(response)
        else:
            return response

    def _handle_stream(self, stream: Iterator) -> Iterator[str]:
        """
        Gestisce lo streaming della risposta

        Args:
            stream: Stream iterator dalla API

        Yields:
            Chunk di testo della risposta
        """
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


class ClaudeClient:
    """Client per le API di Claude (Anthropic) con supporto per thinking e streaming"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inizializza il client Claude

        Args:
            api_key: Chiave API Anthropic (se None, usa la variabile d'ambiente ANTHROPIC_API_KEY)
        """
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    def create_message(
        self,
        messages: list[Dict[str, str]],
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 8192,
        temperature: float = 1.0,
        stream: bool = False,
        thinking_enabled: bool = False,
        thinking_budget: Optional[int] = None,
        **kwargs
    ) -> Any:
        """
        Crea un messaggio con Claude

        Args:
            messages: Lista di messaggi nel formato [{"role": "user", "content": "..."}]
            model: Modello da usare (es: claude-sonnet-4-5-20250929, claude-opus-4-20250514)
            max_tokens: Numero massimo di token da generare
            temperature: Temperatura per la generazione (0.0 - 1.0)
            stream: Se True, abilita lo streaming della risposta
            thinking_enabled: Se True, abilita il pensiero esteso (extended thinking)
            thinking_budget: Budget di token per il pensiero (opzionale)
            **kwargs: Altri parametri da passare all'API

        Returns:
            Risposta dell'API (oggetto Message o Stream)
        """
        params = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }

        # Abilita il pensiero esteso se richiesto
        if thinking_enabled:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget or 10000
            }

        response = self.client.messages.create(**params)

        if stream:
            return self._handle_stream(response)
        else:
            return response

    def _handle_stream(self, stream: Iterator) -> Iterator[str]:
        """
        Gestisce lo streaming della risposta

        Args:
            stream: Stream iterator dalla API

        Yields:
            Chunk di testo della risposta
        """
        for event in stream:
            if event.type == "content_block_delta":
                if hasattr(event.delta, "text"):
                    yield event.delta.text


# Funzioni di utilità per esempi rapidi

def quick_openai_chat(prompt: str, thinking: bool = False, stream: bool = False) -> str:
    """
    Funzione rapida per una chat con OpenAI

    Args:
        prompt: Il prompt da inviare
        thinking: Se True, usa un modello con reasoning
        stream: Se True, abilita lo streaming

    Returns:
        La risposta del modello (o stampa lo stream)
    """
    client = OpenAIClient()
    messages = [{"role": "user", "content": prompt}]

    response = client.chat_completion(
        messages=messages,
        thinking_enabled=thinking,
        stream=stream
    )

    if stream:
        print("OpenAI (streaming):")
        full_response = ""
        for chunk in response:
            print(chunk, end="", flush=True)
            full_response += chunk
        print("\n")
        return full_response
    else:
        return response.choices[0].message.content


def quick_claude_chat(prompt: str, thinking: bool = False, stream: bool = False) -> str:
    """
    Funzione rapida per una chat con Claude

    Args:
        prompt: Il prompt da inviare
        thinking: Se True, abilita il pensiero esteso
        stream: Se True, abilita lo streaming

    Returns:
        La risposta del modello (o stampa lo stream)
    """
    client = ClaudeClient()
    messages = [{"role": "user", "content": prompt}]

    response = client.create_message(
        messages=messages,
        thinking_enabled=thinking,
        stream=stream
    )

    if stream:
        print("Claude (streaming):")
        full_response = ""
        for chunk in response:
            print(chunk, end="", flush=True)
            full_response += chunk
        print("\n")
        return full_response
    else:
        # Gestisci i diversi tipi di contenuto (testo e pensiero)
        full_text = ""
        for block in response.content:
            if block.type == "text":
                full_text += block.text
            elif block.type == "thinking":
                print(f"\n[Pensiero di Claude]: {block.thinking}\n")
        return full_text


# Esempio di utilizzo
if __name__ == "__main__":
    # Assicurati di avere le chiavi API configurate nelle variabili d'ambiente
    # o passa le chiavi direttamente ai costruttori

    print("=== Test OpenAI ===")
    try:
        response = quick_openai_chat("Spiega cos'è il machine learning in 2 frasi")
        print(f"OpenAI: {response}\n")
    except Exception as e:
        print(f"Errore OpenAI: {e}\n")

    print("=== Test Claude ===")
    try:
        response = quick_claude_chat("Spiega cos'è il machine learning in 2 frasi")
        print(f"Claude: {response}\n")
    except Exception as e:
        print(f"Errore Claude: {e}\n")

    print("=== Test con Thinking (Claude) ===")
    try:
        response = quick_claude_chat(
            "Risolvi questo problema: se ho 3 mele e ne compro il doppio, poi ne regalo la metà, quante me ne restano?",
            thinking=True
        )
        print(f"Claude (con thinking): {response}\n")
    except Exception as e:
        print(f"Errore Claude thinking: {e}\n")
