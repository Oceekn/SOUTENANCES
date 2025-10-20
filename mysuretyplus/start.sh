#!/bin/bash

echo "========================================"
echo "    APPLICATION NANA - DEMARRAGE"
echo "========================================"
echo ""

# Vérifier si Python est installé
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERREUR: Python n'est pas installé"
    echo "Veuillez installer Python 3.7+"
    exit 1
fi

echo "✓ Python détecté: $($PYTHON_CMD --version)"

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "ERREUR: Node.js n'est pas installé"
    echo "Veuillez installer Node.js 14+"
    exit 1
fi

echo "✓ Node.js détecté: $(node --version)"
echo ""

# Démarrer le backend Django
echo "[1/3] Démarrage du backend Django..."
cd backend

if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel Python..."
    $PYTHON_CMD -m venv venv
fi

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo "Installation des dépendances Python..."
pip install -r requirements.txt

echo "Démarrage du serveur Django..."
$PYTHON_CMD manage.py runserver > django.log 2>&1 &
DJANGO_PID=$!

# Attendre un peu pour que Django démarre
echo "Attente du démarrage de Django..."
sleep 5

# Démarrer le frontend React
echo "[2/3] Démarrage du frontend React..."
cd ../frontend

echo "Installation des dépendances Node.js..."
npm install

echo "Démarrage du serveur React..."
npm start > react.log 2>&1 &
REACT_PID=$!

# Attendre un peu pour que React démarre
echo "Attente du démarrage de React..."
sleep 5

echo "[3/3] Ouverture du navigateur..."
sleep 3

# Ouvrir le navigateur (Linux)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
else
    echo "Ouvrez manuellement: http://localhost:3000"
fi

echo ""
echo "========================================"
echo "    APPLICATION DEMARRÉE AVEC SUCCÈS!"
echo "========================================"
echo ""
echo "Backend Django: http://localhost:8000"
echo "Frontend React: http://localhost:3000"
echo ""
echo "Logs Django: backend/django.log"
echo "Logs React: frontend/react.log"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application..."

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "Arrêt de l'application..."
    kill $DJANGO_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    echo "Application arrêtée."
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre indéfiniment
wait





