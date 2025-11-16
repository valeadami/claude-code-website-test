"""
Script di test per verificare gli endpoint dell'API server
"""

import requests
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Configurazione
BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("CUSTOM_GPT_API_KEY", "your-secret-api-key-here")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def test_health():
    """Test endpoint health check"""
    print("\n🔍 Test: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_root():
    """Test endpoint root"""
    print("\n🔍 Test: Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_openai_chat():
    """Test endpoint OpenAI chat"""
    print("\n🔍 Test: OpenAI Chat")
    data = {
        "prompt": "Spiega cos'è FastAPI in 1 frase",
        "thinking": False,
        "temperature": 0.7
    }
    response = requests.post(
        f"{BASE_URL}/openai/chat",
        json=data,
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Model: {result['model']}")
        print(f"Response: {result['response'][:100]}...")
        return True
    else:
        print(f"Error: {response.text}")
        return False


def test_claude_chat():
    """Test endpoint Claude chat"""
    print("\n🔍 Test: Claude Chat")
    data = {
        "prompt": "Spiega cos'è FastAPI in 1 frase",
        "thinking": False,
        "temperature": 0.7
    }
    response = requests.post(
        f"{BASE_URL}/claude/chat",
        json=data,
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Model: {result['model']}")
        print(f"Response: {result['response'][:100]}...")
        return True
    else:
        print(f"Error: {response.text}")
        return False


def test_compare():
    """Test endpoint compare"""
    print("\n🔍 Test: Compare Models")
    data = {
        "prompt": "Cosa sono le API?",
        "thinking": False
    }
    response = requests.post(
        f"{BASE_URL}/compare",
        json=data,
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"OpenAI Model: {result['openai_model']}")
        print(f"OpenAI: {result['openai_response'][:80]}...")
        print(f"\nClaude Model: {result['claude_model']}")
        print(f"Claude: {result['claude_response'][:80]}...")
        return True
    else:
        print(f"Error: {response.text}")
        return False


def test_unauthorized():
    """Test che l'autenticazione funzioni"""
    print("\n🔍 Test: Unauthorized Access")
    data = {"prompt": "test", "thinking": False}
    # Prova senza header di autorizzazione
    response = requests.post(
        f"{BASE_URL}/openai/chat",
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 401:
        print("✅ Autenticazione funziona correttamente (richiesta rifiutata)")
        return True
    else:
        print("❌ Problema con l'autenticazione")
        return False


def main():
    """Esegue tutti i test"""
    print("=" * 60)
    print("🧪 Test API Server per Custom GPT Actions")
    print("=" * 60)
    print(f"\n📍 URL: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:20]}...")

    results = {
        "Health Check": test_health(),
        "Root Endpoint": test_root(),
        "Unauthorized Access": test_unauthorized(),
    }

    # Test che richiedono le API keys (potrebbero fallire se non configurate)
    print("\n" + "=" * 60)
    print("⚠️  I seguenti test richiedono chiavi API valide")
    print("=" * 60)

    try:
        results["OpenAI Chat"] = test_openai_chat()
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        results["OpenAI Chat"] = False

    try:
        results["Claude Chat"] = test_claude_chat()
    except Exception as e:
        print(f"❌ Claude test failed: {e}")
        results["Claude Chat"] = False

    try:
        results["Compare Models"] = test_compare()
    except Exception as e:
        print(f"❌ Compare test failed: {e}")
        results["Compare Models"] = False

    # Riepilogo
    print("\n" + "=" * 60)
    print("📊 Riepilogo Test")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} test passati")

    if passed == total:
        print("\n🎉 Tutti i test sono passati! Il server è pronto.")
    else:
        print("\n⚠️  Alcuni test sono falliti. Controlla la configurazione.")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Errore: Non riesco a connettermi al server")
        print("Assicurati che il server sia in esecuzione:")
        print("  python api_server.py")
