#!/bin/sh
# Script de demarrage du conteneur.
# 1) Construit la base vectorielle (embeddings des chunks dans ChromaDB).
# 2) Demarre l'API FastAPI.

echo "Construction de la base vectorielle..."
python vectorize.py

echo "Demarrage de l'API..."
# l'API soit joignable depuis l'exterieur du conteneur.
# le port vient de la variable d'environnement PORT (fournie par l'hebergeur,
# ex. Render). en local cette variable n'existe pas, on retombe sur 8000.
uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}

