# Import de l'application Flask
import sys
import os

# Ajouter le dossier parent au path pour trouver app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Export pour Vercel
app = app
