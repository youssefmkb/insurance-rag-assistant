# RAG generation: produce an answer grounded in the retrieved chunks.

from dotenv import load_dotenv
from anthropic import Anthropic

from retrieve import retrieve

load_dotenv()
client = Anthropic()


def build_prompt(question, chunks):
    """Assemble the prompt: instruction + retrieved context + question."""

    context = "\n\n".join(chunks)

    prompt = f"""Tu es un assistant assurance auto. Reponds a la question de l'utilisateur
en te basant UNIQUEMENT sur le contexte ci-dessous.
Si la reponse ne se trouve pas dans le contexte, dis clairement que tu ne sais pas.
Ne fais pas appel a des connaissances exterieures.

CONTEXTE :
{context}

QUESTION : {question}

REPONSE :"""

    return prompt


def generate_answer(question, k=3):
    """Full RAG pipeline: retrieve, build prompt, generate."""

    chunks, distances = retrieve(question, k=k)
    prompt = build_prompt(question, chunks)

    # Haiku handles generation: fast and economical for high volume.
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.content[0].text
    return answer, chunks


if __name__ == "__main__":
    question = "Combien de temps j'ai pour declarer un vol de voiture ?"
    print(f"Question: {question}\n")

    answer, chunks = generate_answer(question)

    print("--- Generated answer ---")
    print(answer)