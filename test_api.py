# test_api.py
# Verifie que la cle API est bien chargee et que Claude repond.

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()   # lit le fichier .env et remplit os.environ

# Anthropic() lit automatiquement ANTHROPIC_API_KEY depuis os.environ.
client = Anthropic()

# Un petit appel de test sur Haiku (rapide, quelques centimes max).
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=50,
    messages=[{"role": "user", "content": "Reponds juste : OK, cle valide."}],
)

# La reponse est dans response.content[0].text
print(response.content[0].text)