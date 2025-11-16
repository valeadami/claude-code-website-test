"""
API Server per Custom GPT Actions
Espone endpoint per chiamare OpenAI e Claude con thinking
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os
import sys
from pathlib import Path

# Aggiungi la directory root al path per importare core
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.api_client import OpenAIClient, ClaudeClient

app = FastAPI(
    title="AI API for Custom GPT",
    description="API per estendere Custom GPT con chiamate a OpenAI e Claude",
    version="1.0.0"
)

# Configurazione CORS per permettere chiamate da ChatGPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Autenticazione semplice (da configurare nel Custom GPT)
API_KEY = os.getenv("CUSTOM_GPT_API_KEY", "your-secret-api-key-here")


def verify_api_key(authorization: str = Header(None)):
    """Verifica l'API key dalle richieste"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing API Key")

    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return True


# Modelli per le richieste
class AIRequest(BaseModel):
    prompt: str = Field(..., description="Il prompt da inviare all'AI")
    thinking: bool = Field(default=False, description="Abilita il ragionamento esteso")
    max_tokens: Optional[int] = Field(default=None, description="Limite di token nella risposta")
    temperature: Optional[float] = Field(default=1.0, description="Temperatura (0.0-2.0)")


class CompareRequest(BaseModel):
    prompt: str = Field(..., description="Il prompt da inviare a entrambi i modelli")
    thinking: bool = Field(default=False, description="Abilita il ragionamento esteso")


# Modelli per le risposte
class AIResponse(BaseModel):
    response: str
    model: str
    thinking_used: bool


class CompareResponse(BaseModel):
    openai_response: str
    claude_response: str
    openai_model: str
    claude_model: str


# Endpoint API

@app.get("/")
async def root():
    """Endpoint di benvenuto"""
    return {
        "message": "AI API for Custom GPT Actions",
        "version": "1.0.0",
        "endpoints": [
            "/openai/chat",
            "/claude/chat",
            "/compare"
        ]
    }


@app.post("/openai/chat", response_model=AIResponse)
async def openai_chat(
    request: AIRequest,
    authorized: bool = Header(None, include_in_schema=False)
):
    """
    Chiama OpenAI GPT con opzione thinking

    Quando thinking=True, usa automaticamente il modello o1 con reasoning
    """
    try:
        client = OpenAIClient()
        messages = [{"role": "user", "content": request.prompt}]

        model = "o1" if request.thinking else "gpt-4o"

        response = client.chat_completion(
            messages=messages,
            model=model,
            thinking_enabled=request.thinking,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return AIResponse(
            response=response.choices[0].message.content,
            model=model,
            thinking_used=request.thinking
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")


@app.post("/claude/chat", response_model=AIResponse)
async def claude_chat(
    request: AIRequest,
    authorized: bool = Header(None, include_in_schema=False)
):
    """
    Chiama Claude con opzione extended thinking

    Quando thinking=True, Claude userà il ragionamento esteso
    """
    try:
        client = ClaudeClient()
        messages = [{"role": "user", "content": request.prompt}]

        response = client.create_message(
            messages=messages,
            thinking_enabled=request.thinking,
            temperature=request.temperature or 1.0,
            max_tokens=request.max_tokens or 8192
        )

        # Estrai il testo dalla risposta
        full_text = ""
        thinking_text = ""
        for block in response.content:
            if block.type == "text":
                full_text += block.text
            elif block.type == "thinking":
                thinking_text += block.thinking

        # Se c'è thinking, includilo nella risposta
        final_response = full_text
        if thinking_text:
            final_response = f"[RAGIONAMENTO]: {thinking_text}\n\n[RISPOSTA]: {full_text}"

        return AIResponse(
            response=final_response,
            model="claude-sonnet-4-5-20250929",
            thinking_used=request.thinking
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claude Error: {str(e)}")


@app.post("/compare", response_model=CompareResponse)
async def compare_models(
    request: CompareRequest,
    authorized: bool = Header(None, include_in_schema=False)
):
    """
    Confronta le risposte di OpenAI e Claude sullo stesso prompt
    """
    try:
        # Chiama entrambi i modelli in parallelo
        openai_client = OpenAIClient()
        claude_client = ClaudeClient()

        messages = [{"role": "user", "content": request.prompt}]

        # OpenAI
        openai_model = "o1" if request.thinking else "gpt-4o"
        openai_response = openai_client.chat_completion(
            messages=messages,
            model=openai_model,
            thinking_enabled=request.thinking
        )

        # Claude
        claude_response = claude_client.create_message(
            messages=messages,
            thinking_enabled=request.thinking,
            max_tokens=8192
        )

        # Estrai testo da Claude
        claude_text = ""
        for block in claude_response.content:
            if block.type == "text":
                claude_text += block.text

        return CompareResponse(
            openai_response=openai_response.choices[0].message.content,
            claude_response=claude_text,
            openai_model=openai_model,
            claude_model="claude-sonnet-4-5-20250929"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison Error: {str(e)}")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Verifica che il server sia attivo"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
