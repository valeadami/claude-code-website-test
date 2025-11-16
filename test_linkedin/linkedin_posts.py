"""
LinkedIn Posts API
Pubblica post sul profilo LinkedIn dell'utente autenticato
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
POSTS_URL = 'https://api.linkedin.com/v2/ugcPosts'


def get_user_id():
    """
    Recupera l'ID dell'utente necessario per pubblicare post
    """
    if not ACCESS_TOKEN:
        raise Exception("Access token non trovato. Esegui prima linkedin_auth.py")

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(PROFILE_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get('sub')  # ID utente
    else:
        raise Exception(f"Errore nell'ottenere l'ID utente: {response.status_code} - {response.text}")


def create_text_post(text, visibility='PUBLIC'):
    """
    Crea un post di solo testo su LinkedIn

    Args:
        text (str): Il testo del post
        visibility (str): Visibilità del post - 'PUBLIC' o 'CONNECTIONS'

    Returns:
        dict: Risposta dell'API con i dettagli del post creato
    """
    if not ACCESS_TOKEN:
        raise Exception("Access token non trovato. Esegui prima linkedin_auth.py")

    # Ottieni l'ID utente
    user_id = get_user_id()
    author_urn = f"urn:li:person:{user_id}"

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Costruisci il payload del post
    post_data = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        }
    }

    response = requests.post(POSTS_URL, headers=headers, json=post_data)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Errore nella pubblicazione del post: {response.status_code} - {response.text}")


def create_post_with_link(text, link_url, link_title=None, link_description=None, visibility='PUBLIC'):
    """
    Crea un post con un link condiviso

    Args:
        text (str): Il testo del post
        link_url (str): URL del link da condividere
        link_title (str): Titolo del link (opzionale)
        link_description (str): Descrizione del link (opzionale)
        visibility (str): Visibilità del post - 'PUBLIC' o 'CONNECTIONS'

    Returns:
        dict: Risposta dell'API con i dettagli del post creato
    """
    if not ACCESS_TOKEN:
        raise Exception("Access token non trovato. Esegui prima linkedin_auth.py")

    # Ottieni l'ID utente
    user_id = get_user_id()
    author_urn = f"urn:li:person:{user_id}"

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Costruisci il payload del post con link
    media_content = {
        "status": "READY",
        "originalUrl": link_url
    }

    if link_title:
        media_content["title"] = {"text": link_title}

    if link_description:
        media_content["description"] = {"text": link_description}

    post_data = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "ARTICLE",
                "media": [media_content]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        }
    }

    response = requests.post(POSTS_URL, headers=headers, json=post_data)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Errore nella pubblicazione del post: {response.status_code} - {response.text}")


def main():
    """
    Funzione principale - menu interattivo
    """
    print("\n" + "="*60)
    print("LinkedIn Posts API - Pubblicazione Post")
    print("="*60 + "\n")

    if not ACCESS_TOKEN:
        print("❌ ERRORE: Access token non trovato!")
        print("Esegui prima linkedin_auth.py per ottenere il token\n")
        return 1

    print("Scegli il tipo di post da pubblicare:\n")
    print("1. Post di solo testo")
    print("2. Post con link")
    print("3. Test (post di prova)")
    print("0. Esci\n")

    choice = input("Scelta: ")

    try:
        if choice == '1':
            print("\n--- Post di solo testo ---")
            text = input("Inserisci il testo del post: ")

            print("\nVisibilità:")
            print("1. PUBLIC (pubblico)")
            print("2. CONNECTIONS (solo collegamenti)")
            vis_choice = input("Scelta: ")
            visibility = 'PUBLIC' if vis_choice == '1' else 'CONNECTIONS'

            print("\n📤 Pubblicazione in corso...")
            result = create_text_post(text, visibility)

            print("\n✅ Post pubblicato con successo!")
            print(f"ID Post: {result.get('id', 'N/A')}")
            print(f"\nDettagli:")
            print(json.dumps(result, indent=2))

        elif choice == '2':
            print("\n--- Post con link ---")
            text = input("Inserisci il testo del post: ")
            link_url = input("Inserisci l'URL del link: ")
            link_title = input("Titolo del link (opzionale, premi invio per saltare): ") or None
            link_description = input("Descrizione del link (opzionale, premi invio per saltare): ") or None

            print("\nVisibilità:")
            print("1. PUBLIC (pubblico)")
            print("2. CONNECTIONS (solo collegamenti)")
            vis_choice = input("Scelta: ")
            visibility = 'PUBLIC' if vis_choice == '1' else 'CONNECTIONS'

            print("\n📤 Pubblicazione in corso...")
            result = create_post_with_link(text, link_url, link_title, link_description, visibility)

            print("\n✅ Post pubblicato con successo!")
            print(f"ID Post: {result.get('id', 'N/A')}")
            print(f"\nDettagli:")
            print(json.dumps(result, indent=2))

        elif choice == '3':
            print("\n--- Test Post ---")
            test_text = "🤖 Test post pubblicato tramite LinkedIn API - Questa è una prova!"

            print("📤 Pubblicazione post di test...")
            result = create_text_post(test_text, 'CONNECTIONS')

            print("\n✅ Post di test pubblicato con successo!")
            print(f"ID Post: {result.get('id', 'N/A')}")
            print("\n⚠️  Nota: Il post è visibile solo ai tuoi collegamenti (CONNECTIONS)")
            print("    Puoi eliminarlo manualmente da LinkedIn se necessario")

        elif choice == '0':
            print("Uscita...")
            return 0

        else:
            print("❌ Scelta non valida")
            return 1

    except Exception as e:
        print(f"\n❌ ERRORE: {str(e)}")
        print("\nAssicurati di:")
        print("1. Aver eseguito linkedin_auth.py per ottenere il token")
        print("2. Il token sia ancora valido (non scaduto)")
        print("3. Avere lo scope 'w_member_social' abilitato")
        return 1

    print("\n✅ Operazione completata!\n")
    return 0


if __name__ == '__main__':
    exit(main())
