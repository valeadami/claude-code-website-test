"""
LinkedIn OAuth 2.0 Authentication
Gestisce il flusso di autenticazione per ottenere l'access token
"""

import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, redirect
from urllib.parse import urlencode

# Carica variabili d'ambiente
load_dotenv()

app = Flask(__name__)

# Configurazione
CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:5000/callback')

# Scope richiesti
SCOPES = [
    'openid',
    'profile',
    'email',
    'w_member_social'  # Per pubblicare post
]

# LinkedIn OAuth URLs
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'


def get_authorization_url():
    """
    Genera l'URL per avviare il flusso OAuth 2.0
    """
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'state': 'random_state_string'  # In produzione, usa un valore random sicuro
    }

    url = f"{AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    return url


def exchange_code_for_token(authorization_code):
    """
    Scambia il codice di autorizzazione con un access token
    """
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data
    else:
        raise Exception(f"Errore nell'ottenere il token: {response.text}")


@app.route('/')
def index():
    """
    Homepage con link per iniziare l'autenticazione
    """
    auth_url = get_authorization_url()

    html = f"""
    <html>
        <head>
            <title>LinkedIn API Test - Autenticazione</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                }}
                .button {{
                    background-color: #0077B5;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin-top: 20px;
                }}
                .button:hover {{
                    background-color: #005885;
                }}
            </style>
        </head>
        <body>
            <h1>LinkedIn API Test - Autenticazione</h1>
            <p>Clicca il pulsante qui sotto per autenticarti con LinkedIn:</p>
            <a href="{auth_url}" class="button">Accedi con LinkedIn</a>

            <h2>Cosa succede?</h2>
            <ul>
                <li>Verrai reindirizzato alla pagina di login di LinkedIn</li>
                <li>Dopo l'accesso, LinkedIn ti chiederà di autorizzare l'app</li>
                <li>Verrai reindirizzato a questa app con il token di accesso</li>
            </ul>

            <h2>Scope richiesti:</h2>
            <ul>
                <li><strong>openid, profile, email:</strong> Dati base del profilo</li>
                <li><strong>w_member_social:</strong> Pubblicare post</li>
            </ul>
        </body>
    </html>
    """
    return html


@app.route('/callback')
def callback():
    """
    Callback URL dove LinkedIn reindirizza dopo l'autenticazione
    """
    # Ottieni il codice di autorizzazione
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return f"""
        <html>
            <body>
                <h1>Errore nell'autenticazione</h1>
                <p>Errore: {error}</p>
                <p>Descrizione: {request.args.get('error_description', 'N/A')}</p>
            </body>
        </html>
        """

    if not code:
        return "Errore: Nessun codice di autorizzazione ricevuto"

    try:
        # Scambia il codice per un token
        token_data = exchange_code_for_token(code)
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in')

        # Salva il token in un file .env
        env_path = os.path.join(os.path.dirname(__file__), '.env')

        # Leggi il contenuto esistente del file .env se esiste
        env_content = {}
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_content[key] = value

        # Aggiorna il token
        env_content['LINKEDIN_ACCESS_TOKEN'] = access_token

        # Scrivi il file .env aggiornato
        with open(env_path, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")

        html = f"""
        <html>
            <head>
                <title>Autenticazione riuscita!</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 50px auto;
                        padding: 20px;
                    }}
                    .success {{
                        background-color: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                    }}
                    .token {{
                        background-color: #f8f9fa;
                        border: 1px solid #dee2e6;
                        padding: 10px;
                        border-radius: 3px;
                        font-family: monospace;
                        word-break: break-all;
                        margin: 10px 0;
                    }}
                </style>
            </head>
            <body>
                <h1>Autenticazione riuscita!</h1>

                <div class="success">
                    Il token di accesso è stato salvato nel file .env
                </div>

                <h2>Dettagli token:</h2>
                <p><strong>Access Token:</strong></p>
                <div class="token">{access_token[:50]}...</div>

                <p><strong>Scade tra:</strong> {expires_in} secondi ({expires_in // 3600} ore)</p>

                <h2>Prossimi passi:</h2>
                <ol>
                    <li>Il token è stato salvato in <code>.env</code></li>
                    <li>Ora puoi eseguire <code>linkedin_profile.py</code> per ottenere i dati del profilo</li>
                    <li>Oppure <code>linkedin_posts.py</code> per pubblicare un post</li>
                </ol>

                <p><a href="/">Torna alla home</a></p>
            </body>
        </html>
        """

        return html

    except Exception as e:
        return f"""
        <html>
            <body>
                <h1>Errore</h1>
                <p>Si è verificato un errore durante lo scambio del token:</p>
                <pre>{str(e)}</pre>
            </body>
        </html>
        """


if __name__ == '__main__':
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERRORE: Configura LINKEDIN_CLIENT_ID e LINKEDIN_CLIENT_SECRET nel file .env")
        print("Copia .env.example in .env e inserisci le tue credenziali")
        exit(1)

    print("\n" + "="*60)
    print("LinkedIn OAuth 2.0 Authentication Server")
    print("="*60)
    print(f"\nApri il browser e vai a: http://localhost:5000")
    print("\nPremi CTRL+C per fermare il server\n")

    app.run(debug=True, port=5000)
