"""
API Server per Customer Care Custom GPT
Gestisce richieste di stato ordini per un chatbot di assistenza clienti
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, timedelta
import os

app = FastAPI(
    title="Customer Care API",
    description="API per Custom GPT di assistenza clienti - Stato ordini",
    version="1.0.0"
)

# Configurazione CORS per permettere chiamate da ChatGPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Autenticazione semplice
API_KEY = os.getenv("CUSTOM_GPT_API_KEY", "sk-customer-care-secret-2025")


def verify_api_key(authorization: str = Header(None)):
    """Verifica l'API key dalle richieste"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing API Key")

    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return True


# Database mockup degli ordini
MOCK_ORDERS = {
    "ORD-2025-01": {
        "order_id": "ORD-2025-01",
        "customer_name": "Mario Rossi",
        "customer_email": "mario.rossi@email.com",
        "order_date": "2025-01-10",
        "status": "delivered",
        "status_description": "Consegnato",
        "total_amount": 149.99,
        "currency": "EUR",
        "items": [
            {"name": "Laptop HP", "quantity": 1, "price": 149.99}
        ],
        "shipping_address": "Via Roma 123, Milano, 20100",
        "tracking_number": "IT123456789",
        "tracking_url": "https://tracking.example.com/IT123456789",
        "delivery_date": "2025-01-15",
        "notes": "Consegnato al portiere"
    },
    "ORD-2025-02": {
        "order_id": "ORD-2025-02",
        "customer_name": "Laura Bianchi",
        "customer_email": "laura.bianchi@email.com",
        "order_date": "2025-01-12",
        "status": "in_transit",
        "status_description": "In transito",
        "total_amount": 89.50,
        "currency": "EUR",
        "items": [
            {"name": "Mouse Wireless", "quantity": 2, "price": 29.99},
            {"name": "Tastiera Meccanica", "quantity": 1, "price": 29.52}
        ],
        "shipping_address": "Corso Garibaldi 45, Roma, 00100",
        "tracking_number": "IT987654321",
        "tracking_url": "https://tracking.example.com/IT987654321",
        "estimated_delivery": "2025-01-18",
        "notes": "Il pacco è in consegna, arrivo previsto domani"
    },
    "ORD-2025-03": {
        "order_id": "ORD-2025-03",
        "customer_name": "Giuseppe Verdi",
        "customer_email": "g.verdi@email.com",
        "order_date": "2025-01-14",
        "status": "processing",
        "status_description": "In preparazione",
        "total_amount": 299.00,
        "currency": "EUR",
        "items": [
            {"name": "Monitor 27\"", "quantity": 1, "price": 299.00}
        ],
        "shipping_address": "Piazza San Marco 1, Venezia, 30100",
        "tracking_number": None,
        "tracking_url": None,
        "estimated_delivery": "2025-01-20",
        "notes": "L'ordine è in preparazione nel nostro magazzino"
    },
    "ORD-2025-04": {
        "order_id": "ORD-2025-04",
        "customer_name": "Anna Ferrari",
        "customer_email": "anna.ferrari@email.com",
        "order_date": "2025-01-15",
        "status": "cancelled",
        "status_description": "Annullato",
        "total_amount": 45.00,
        "currency": "EUR",
        "items": [
            {"name": "Cavo USB-C", "quantity": 3, "price": 15.00}
        ],
        "shipping_address": "Via Dante 78, Torino, 10100",
        "tracking_number": None,
        "tracking_url": None,
        "cancellation_reason": "Annullato dal cliente il 2025-01-15",
        "refund_status": "Rimborso completato",
        "notes": "Il rimborso è stato processato e verrà accreditato entro 3-5 giorni lavorativi"
    },
    "ORD-2025-05": {
        "order_id": "ORD-2025-05",
        "customer_name": "Paolo Neri",
        "customer_email": "paolo.neri@email.com",
        "order_date": "2025-01-16",
        "status": "shipped",
        "status_description": "Spedito",
        "total_amount": 599.99,
        "currency": "EUR",
        "items": [
            {"name": "Smartphone XYZ", "quantity": 1, "price": 499.99},
            {"name": "Cover protettiva", "quantity": 1, "price": 19.99},
            {"name": "Pellicola vetro", "quantity": 1, "price": 9.99},
            {"name": "Caricabatterie rapido", "quantity": 1, "price": 29.99},
            {"name": "Cuffie Bluetooth", "quantity": 1, "price": 39.99}
        ],
        "shipping_address": "Viale Europa 234, Napoli, 80100",
        "tracking_number": "IT555666777",
        "tracking_url": "https://tracking.example.com/IT555666777",
        "estimated_delivery": "2025-01-19",
        "notes": "Pacco affidato al corriere BRT"
    },
    "ORD-2025-06": {
        "order_id": "ORD-2025-06",
        "customer_name": "Chiara Greco",
        "customer_email": "chiara.greco@email.com",
        "order_date": "2025-01-08",
        "status": "delivered",
        "status_description": "Consegnato",
        "total_amount": 1299.00,
        "currency": "EUR",
        "items": [
            {"name": "Notebook Pro 15\"", "quantity": 1, "price": 1299.00}
        ],
        "shipping_address": "Via Mazzini 56, Bologna, 40100",
        "tracking_number": "IT111222333",
        "tracking_url": "https://tracking.example.com/IT111222333",
        "delivery_date": "2025-01-12",
        "notes": "Consegnato e firmato dal destinatario"
    },
    "ORD-2025-07": {
        "order_id": "ORD-2025-07",
        "customer_name": "Stefano Lombardi",
        "customer_email": "s.lombardi@email.com",
        "order_date": "2025-01-17",
        "status": "pending_payment",
        "status_description": "In attesa di pagamento",
        "total_amount": 199.99,
        "currency": "EUR",
        "items": [
            {"name": "Webcam HD", "quantity": 1, "price": 79.99},
            {"name": "Microfono USB", "quantity": 1, "price": 119.99}
        ],
        "shipping_address": "Corso Italia 89, Firenze, 50100",
        "tracking_number": None,
        "tracking_url": None,
        "payment_link": "https://payments.example.com/pay/ORD-2025-07",
        "notes": "In attesa del completamento del pagamento. Link di pagamento inviato via email."
    },
    "ORD-2025-08": {
        "order_id": "ORD-2025-08",
        "customer_name": "Francesca Ricci",
        "customer_email": "francesca.ricci@email.com",
        "order_date": "2025-01-13",
        "status": "return_requested",
        "status_description": "Reso richiesto",
        "total_amount": 79.99,
        "currency": "EUR",
        "items": [
            {"name": "Auricolari wireless", "quantity": 1, "price": 79.99}
        ],
        "shipping_address": "Via Verdi 12, Palermo, 90100",
        "tracking_number": "IT444555666",
        "tracking_url": "https://tracking.example.com/IT444555666",
        "delivery_date": "2025-01-16",
        "return_reason": "Prodotto non conforme",
        "return_tracking": "IT999888777",
        "notes": "Reso autorizzato. Etichetta di reso inviata via email. Rimborso verrà processato dopo ispezione del prodotto."
    }
}

# Status disponibili con descrizioni
ORDER_STATUSES = {
    "pending_payment": "In attesa di pagamento",
    "processing": "In preparazione",
    "shipped": "Spedito",
    "in_transit": "In transito",
    "out_for_delivery": "In consegna",
    "delivered": "Consegnato",
    "cancelled": "Annullato",
    "return_requested": "Reso richiesto",
    "returned": "Reso completato"
}


# Modelli Pydantic
class OrderStatusResponse(BaseModel):
    """Risposta con lo stato di un ordine"""
    success: bool
    order_id: str
    status: str
    status_description: str
    order_date: str
    total_amount: float
    currency: str
    items: list
    shipping_address: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    estimated_delivery: Optional[str] = None
    delivery_date: Optional[str] = None
    notes: Optional[str] = None
    # Campi opzionali per situazioni speciali
    cancellation_reason: Optional[str] = None
    refund_status: Optional[str] = None
    return_reason: Optional[str] = None
    return_tracking: Optional[str] = None
    payment_link: Optional[str] = None


class ErrorResponse(BaseModel):
    """Risposta in caso di errore"""
    success: bool = False
    error: str
    message: str


# Endpoint API

@app.get("/")
async def root():
    """Endpoint di benvenuto"""
    return {
        "service": "Customer Care API",
        "version": "1.0.0",
        "description": "API per gestire richieste di stato ordini",
        "endpoints": {
            "order_status": "/order/{order_id}",
            "list_orders": "/orders/list"
        }
    }


@app.get("/order/{order_id}", response_model=OrderStatusResponse)
async def get_order_status(
    order_id: str,
    authorized: bool = Header(None, include_in_schema=False)
):
    """
    Recupera lo stato di un ordine dato il suo ID

    L'order_id deve essere nel formato ORD-2025-XX

    Restituisce:
    - Informazioni complete sull'ordine
    - Stato corrente
    - Tracking (se disponibile)
    - Data di consegna stimata o effettiva
    - Note aggiuntive
    """
    # Normalizza l'ID (uppercase e rimuovi spazi)
    order_id = order_id.strip().upper()

    # Cerca l'ordine nel database mockup
    if order_id not in MOCK_ORDERS:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "order_not_found",
                "message": f"Ordine {order_id} non trovato. Verifica che l'ID sia corretto."
            }
        )

    order = MOCK_ORDERS[order_id]

    return OrderStatusResponse(
        success=True,
        **order
    )


@app.get("/orders/list")
async def list_orders(
    authorized: bool = Header(None, include_in_schema=False)
):
    """
    Lista tutti gli ordini disponibili (solo per testing)

    NOTA: In produzione questo endpoint non dovrebbe esistere
    o dovrebbe essere filtrato per cliente
    """
    return {
        "success": True,
        "total_orders": len(MOCK_ORDERS),
        "orders": [
            {
                "order_id": order["order_id"],
                "status": order["status"],
                "status_description": order["status_description"],
                "order_date": order["order_date"],
                "total_amount": order["total_amount"]
            }
            for order in MOCK_ORDERS.values()
        ]
    }


@app.get("/health")
async def health_check():
    """Verifica che il server sia attivo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_orders": len(MOCK_ORDERS)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
