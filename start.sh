#!/bin/sh
# Script de demarrage du conteneur.
# 1) Construit la base vectorielle (embeddings des chunks dans ChromaDB).
# 2) Demarre l'API FastAPI.

echo "Construction de la base vectorielle..."
python vectorize.py

echo "Demarrage de l'API..."
# on lance uvicorn en ecoutant sur 0.0.0.0 (toutes les interfaces),
# indispensable pour que l'API soit accessible depuis l'exterieur du conteneur.
uvicorn api:app --host 0.0.0.0 --port 8000

