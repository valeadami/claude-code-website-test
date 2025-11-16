"""
Script per generare lo schema OpenAPI da usare nel Custom GPT
"""

import json
from api_server import app

# Genera lo schema OpenAPI
schema = app.openapi()

# Modifica lo schema per renderlo compatibile con Custom GPT
# Rimuovi l'endpoint di autorizzazione dal schema (lo configureremo manualmente)
if "components" in schema:
    if "securitySchemes" not in schema["components"]:
        schema["components"]["securitySchemes"] = {}

    # Aggiungi lo schema di sicurezza Bearer
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "API Key"
    }

# Aggiungi la sicurezza a tutti gli endpoint (tranne root e health)
for path, methods in schema["paths"].items():
    if path not in ["/", "/health"]:
        for method in methods:
            if method != "parameters":
                if "security" not in schema["paths"][path][method]:
                    schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

# Salva lo schema in un file
with open("openapi_schema.json", "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

print("✅ Schema OpenAPI generato con successo!")
print("📄 File salvato: openapi_schema.json")
print("\n🔗 Usa questo file per configurare le Actions nel tuo Custom GPT")
print("\n📖 Leggi CUSTOM_GPT_SETUP.md per le istruzioni complete")
