#!/bin/bash
# Script per deploy rapido con Ngrok

echo "🚀 Deploy con Ngrok"
echo "==================="
echo ""

# Controlla se ngrok è installato
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok non è installato"
    echo ""
    echo "Installa ngrok:"
    echo "1. Vai su https://ngrok.com/"
    echo "2. Crea un account gratuito"
    echo "3. Scarica ngrok per il tuo sistema"
    echo "4. Installa ed esegui: ngrok config add-authtoken <YOUR_TOKEN>"
    echo ""
    echo "Oppure su Linux/Mac:"
    echo "  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null"
    echo "  echo \"deb https://ngrok-agent.s3.amazonaws.com buster main\" | sudo tee /etc/apt/sources.list.d/ngrok.list"
    echo "  sudo apt update && sudo apt install ngrok"
    echo ""
    exit 1
fi

echo "✅ Ngrok trovato"
echo ""
echo "📝 Istruzioni:"
echo "1. Avvia il server API in un terminale:"
echo "   python api_server.py"
echo ""
echo "2. Avvia ngrok (questo script o manualmente):"
echo "   ngrok http 8000"
echo ""
echo "3. Copia l'URL HTTPS che ngrok ti dà"
echo "4. Usa quell'URL per configurare il Custom GPT"
echo ""
read -p "Premi INVIO per avviare ngrok su porta 8000..."

ngrok http 8000
