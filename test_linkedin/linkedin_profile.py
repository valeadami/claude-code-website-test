"""
LinkedIn Profile API
Recupera i dati del profilo dell'utente autenticato
"""

import os
import requests
from dotenv import load_dotenv
import json

# Carica variabili d'ambiente
load_dotenv()

# Configurazione
ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

# API Endpoints
PROFILE_URL = 'https://api.linkedin.com/v2/userinfo'


def get_profile_info():
    """
    Recupera le informazioni base del profilo
    Usando l'endpoint userinfo (OpenID Connect)
    """
    if not ACCESS_TOKEN:
        raise Exception("Access token non trovato. Esegui prima linkedin_auth.py")

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(PROFILE_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Errore nell'ottenere il profilo: {response.status_code} - {response.text}")


def get_profile_v2():
    """
    Recupera informazioni usando l'API v2 /me endpoint
    Nota: Questo endpoint è deprecato ma potrebbe ancora funzionare
    """
    if not ACCESS_TOKEN:
        raise Exception("Access token non trovato. Esegui prima linkedin_auth.py")

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Endpoint per ottenere il profilo base
    url = 'https://api.linkedin.com/v2/me'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore con /v2/me: {response.status_code} - {response.text}")
        return None


def display_profile(profile_data):
    """
    Visualizza i dati del profilo in modo leggibile
    """
    print("\n" + "="*60)
    print("DATI PROFILO LINKEDIN")
    print("="*60 + "\n")

    if 'sub' in profile_data:
        # Formato userinfo (OpenID Connect)
        print(f"ID Utente:        {profile_data.get('sub', 'N/A')}")
        print(f"Nome:             {profile_data.get('given_name', 'N/A')}")
        print(f"Cognome:          {profile_data.get('family_name', 'N/A')}")
        print(f"Nome completo:    {profile_data.get('name', 'N/A')}")
        print(f"Email:            {profile_data.get('email', 'N/A')}")
        print(f"Email verificata: {profile_data.get('email_verified', 'N/A')}")
        print(f"Foto profilo:     {profile_data.get('picture', 'N/A')}")
    else:
        # Formato v2/me
        print(f"ID Utente:        {profile_data.get('id', 'N/A')}")

        # Nome localizzato
        localized_name = profile_data.get('localizedFirstName', '')
        localized_lastname = profile_data.get('localizedLastName', '')
        print(f"Nome:             {localized_name} {localized_lastname}")

    print("\n" + "="*60)
    print("DATI RAW (JSON)")
    print("="*60 + "\n")
    print(json.dumps(profile_data, indent=2, ensure_ascii=False))


def main():
    """
    Funzione principale
    """
    print("\n" + "="*60)
    print("LinkedIn Profile API - Test")
    print("="*60 + "\n")

    try:
        # Metodo 1: userinfo endpoint (raccomandato)
        print("Recupero dati profilo tramite /userinfo...")
        profile = get_profile_info()
        display_profile(profile)

        # Metodo 2: v2/me endpoint (opzionale, deprecato)
        print("\n\nTentativo di recuperare dati tramite /v2/me...")
        profile_v2 = get_profile_v2()
        if profile_v2:
            print("\n" + "="*60)
            print("DATI DA /v2/me ENDPOINT")
            print("="*60 + "\n")
            print(json.dumps(profile_v2, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\nERRORE: {str(e)}")
        print("\nAssicurati di:")
        print("1. Aver eseguito linkedin_auth.py per ottenere il token")
        print("2. Il token sia ancora valido (non scaduto)")
        print("3. Avere i permessi corretti (scope: openid, profile, email)")
        return 1

    print("\n✅ Test completato con successo!\n")
    return 0


if __name__ == '__main__':
    exit(main())
