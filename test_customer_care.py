"""
Test suite per il Customer Care API server
"""

import requests
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Configurazione
BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("CUSTOM_GPT_API_KEY", "sk-customer-care-secret-2025")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def print_section(title):
    """Stampa una sezione separata"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_health():
    """Test health check endpoint"""
    print_section("Test: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Server: {data['status']}")
        print(f"   Ordini totali: {data['total_orders']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False


def test_root():
    """Test root endpoint"""
    print_section("Test: Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Service: {data['service']}")
        print(f"   Version: {data['version']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False


def test_order_found(order_id):
    """Test recupero ordine esistente"""
    print_section(f"Test: Ordine Trovato - {order_id}")
    try:
        response = requests.get(
            f"{BASE_URL}/order/{order_id}",
            headers=HEADERS
        )
        print(f"✅ Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n   📦 DETTAGLI ORDINE:")
            print(f"   ID: {data['order_id']}")
            print(f"   Status: {data['status']} ({data['status_description']})")
            print(f"   Data ordine: {data['order_date']}")
            print(f"   Totale: €{data['total_amount']}")
            print(f"   Indirizzo: {data['shipping_address']}")

            if data.get('tracking_number'):
                print(f"   📍 Tracking: {data['tracking_number']}")
                print(f"   🔗 URL: {data['tracking_url']}")

            if data.get('delivery_date'):
                print(f"   ✅ Consegnato il: {data['delivery_date']}")
            elif data.get('estimated_delivery'):
                print(f"   📅 Consegna prevista: {data['estimated_delivery']}")

            print(f"\n   Articoli:")
            for item in data['items']:
                print(f"   - {item['name']} (x{item['quantity']}) - €{item['price']}")

            if data.get('notes'):
                print(f"\n   📝 Note: {data['notes']}")

            if data.get('cancellation_reason'):
                print(f"\n   ❌ Motivo annullamento: {data['cancellation_reason']}")
                print(f"   💰 Rimborso: {data.get('refund_status', 'N/A')}")

            if data.get('return_reason'):
                print(f"\n   🔄 Reso richiesto: {data['return_reason']}")
                print(f"   📦 Tracking reso: {data.get('return_tracking', 'N/A')}")

            return True
        else:
            print(f"❌ Errore {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Errore: {e}")
        return False


def test_order_not_found():
    """Test ordine non esistente"""
    print_section("Test: Ordine Non Trovato")
    try:
        response = requests.get(
            f"{BASE_URL}/order/ORD-2025-99",
            headers=HEADERS
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 404:
            print("✅ Correttamente restituito 404 per ordine inesistente")
            data = response.json()
            print(f"   Messaggio: {data['detail']['message']}")
            return True
        else:
            print(f"❌ Atteso 404, ricevuto {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Errore: {e}")
        return False


def test_list_orders():
    """Test lista ordini"""
    print_section("Test: Lista Ordini")
    try:
        response = requests.get(
            f"{BASE_URL}/orders/list",
            headers=HEADERS
        )
        print(f"✅ Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n   Ordini totali: {data['total_orders']}")
            print(f"\n   📋 LISTA ORDINI:")
            print(f"   {'ID':<15} {'Status':<20} {'Data':<12} {'Totale':>10}")
            print(f"   {'-'*15} {'-'*20} {'-'*12} {'-'*10}")

            for order in data['orders']:
                print(f"   {order['order_id']:<15} "
                      f"{order['status_description']:<20} "
                      f"{order['order_date']:<12} "
                      f"€{order['total_amount']:>9.2f}")

            return True
        else:
            print(f"❌ Errore {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Errore: {e}")
        return False


def test_all_orders():
    """Test tutti gli ordini mockup"""
    print_section("Test: Tutti gli Ordini Mockup")

    order_ids = [
        "ORD-2025-01",  # Consegnato
        "ORD-2025-02",  # In transito
        "ORD-2025-03",  # In preparazione
        "ORD-2025-04",  # Annullato
        "ORD-2025-05",  # Spedito
        "ORD-2025-06",  # Consegnato
        "ORD-2025-07",  # In attesa pagamento
        "ORD-2025-08",  # Reso richiesto
    ]

    results = {}
    for order_id in order_ids:
        results[order_id] = test_order_found(order_id)

    return all(results.values())


def run_quick_tests():
    """Esegue test rapidi essenziali"""
    print("\n" + "🚀" * 35)
    print("  QUICK TESTS - Customer Care API")
    print("🚀" * 35)

    results = {
        "Health Check": test_health(),
        "Root Endpoint": test_root(),
        "Ordine Consegnato": test_order_found("ORD-2025-01"),
        "Ordine In Transito": test_order_found("ORD-2025-02"),
        "Ordine Annullato": test_order_found("ORD-2025-04"),
        "Ordine Non Trovato": test_order_not_found(),
        "Lista Ordini": test_list_orders(),
    }

    print_section("RIEPILOGO QUICK TESTS")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} test passati")

    if passed == total:
        print("\n🎉 Tutti i test sono passati! Il server è pronto per il Custom GPT.")
    else:
        print("\n⚠️  Alcuni test sono falliti. Controlla la configurazione.")

    return all(results.values())


def run_full_tests():
    """Esegue suite completa di test"""
    print("\n" + "🧪" * 35)
    print("  FULL TEST SUITE - Customer Care API")
    print("🧪" * 35)

    results = {
        "Health Check": test_health(),
        "Root Endpoint": test_root(),
        "Lista Ordini": test_list_orders(),
        "Ordine Non Trovato": test_order_not_found(),
    }

    # Test tutti gli ordini
    all_orders_ok = test_all_orders()
    results["Tutti gli Ordini"] = all_orders_ok

    print_section("RIEPILOGO FULL TESTS")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} test passati")

    if passed == total:
        print("\n🎉 Suite completa passata! Pronto per produzione.")
    else:
        print("\n⚠️  Alcuni test sono falliti.")

    return all(results.values())


def interactive_menu():
    """Menu interattivo per testing"""
    while True:
        print("\n" + "=" * 70)
        print("  CUSTOMER CARE API - TEST MENU")
        print("=" * 70)
        print("\n  1. Quick Tests (essenziali)")
        print("  2. Full Test Suite (completa)")
        print("  3. Test singolo ordine")
        print("  4. Lista tutti gli ordini")
        print("  5. Health Check")
        print("  0. Esci")
        print()

        choice = input("Seleziona opzione: ").strip()

        if choice == "1":
            run_quick_tests()
        elif choice == "2":
            run_full_tests()
        elif choice == "3":
            order_id = input("Inserisci ID ordine (es: ORD-2025-01): ").strip()
            test_order_found(order_id)
        elif choice == "4":
            test_list_orders()
        elif choice == "5":
            test_health()
        elif choice == "0":
            print("\n👋 Ciao!")
            break
        else:
            print("\n❌ Opzione non valida")

        input("\nPremi INVIO per continuare...")


if __name__ == "__main__":
    import sys

    print("\n" + "🛍️" * 35)
    print("  CUSTOMER CARE API TEST SUITE")
    print("🛍️" * 35)
    print(f"\nURL: {BASE_URL}")

    # Controlla connessione al server
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except:
        print("\n❌ ERRORE: Server non raggiungibile!")
        print("\nAssicurati che il server sia in esecuzione:")
        print("  python customer_care_server.py")
        print()
        sys.exit(1)

    # Se passati argomenti, esegui test specifici
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            run_quick_tests()
        elif sys.argv[1] == "full":
            run_full_tests()
        elif sys.argv[1].startswith("ORD-"):
            test_order_found(sys.argv[1])
        else:
            print(f"\nArgomento non riconosciuto: {sys.argv[1]}")
            print("\nUso:")
            print("  python test_customer_care.py         # Menu interattivo")
            print("  python test_customer_care.py quick   # Quick tests")
            print("  python test_customer_care.py full    # Full suite")
            print("  python test_customer_care.py ORD-2025-01  # Test ordine specifico")
    else:
        # Menu interattivo
        interactive_menu()
