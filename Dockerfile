# Construit une image portable du RAG expose en API FastAPI.

# Image de base : Python 3.12 version "slim" (legere, sans outils superflus).
FROM python:3.12-slim

# Dossier de travail a l'interieur du conteneur.
WORKDIR /app

# --- Optimisation du cache de build ---
# On copie d'ABORD requirements.txt seul, puis on installe.
# Ainsi, tant que les dependances ne changent pas, Docker reutilise
# cette couche en cache et ne reinstalle pas a chaque modif de code.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensuite seulement, on copie tout le reste du code du projet.
COPY . .

# Documente le port sur lequel l'API ecoute (uvicorn tourne sur 8000).
EXPOSE 8000

# Copie le script de demarrage et le rend executable.
COPY start.sh .
RUN chmod +x start.sh

# Au demarrage : on lance le script (construit la base PUIS demarre l'API).
CMD ["./start.sh"]