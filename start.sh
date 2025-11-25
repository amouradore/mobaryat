#!/bin/bash

echo "========================================"
echo "  Mobaryat - Application de Streaming"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python3 n'est pas installé"
    echo "Installez Python3 avec: sudo apt install python3 python3-pip"
    exit 1
fi

echo "[OK] Python est installé"
echo ""

# Vérifier si les dépendances sont installées
echo "Vérification des dépendances..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installation des dépendances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Échec de l'installation des dépendances"
        exit 1
    fi
else
    echo "[OK] Dépendances installées"
fi

echo ""
echo "Création des dossiers nécessaires..."
mkdir -p cache templates static/css static/js static/logos scrapers

echo "[OK] Dossiers créés"
echo ""
echo "========================================"
echo "  Démarrage de l'application..."
echo "========================================"
echo ""
echo "L'application sera accessible sur:"
echo "  http://localhost:5000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer l'application
python3 app.py
