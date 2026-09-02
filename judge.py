# LLM-as-judge: Sonnet checks whether Haiku's answer is grounded in the sources.

import json
from dotenv import load_dotenv
from anthropic import Anthropic

from generate import generate_answer

load_dotenv()
client = Anthropic()


def judge_answer(question, answer, chunks):
    """Have Sonnet judge whether the answer is fully supported by the chunks."""

    context = "\n\n".join(chunks)

    judge_prompt = f"""Tu es un evaluateur qualite. On te donne un CONTEXTE source,
une QUESTION, et une REPONSE generee par un autre modele.

Ta tache : verifier si la REPONSE est ENTIEREMENT fondee sur le CONTEXTE.
- Si chaque affirmation de la reponse provient du contexte : grounded = true.
- Si la reponse ajoute des informations absentes du contexte ou le contredit : grounded = false.

Reponds UNIQUEMENT avec un objet JSON, sans texte autour, au format exact :
{{"grounded": true/false, "reason": "courte justification"}}

CONTEXTE :
{context}

QUESTION : {question}

REPONSE A EVALUER : {answer}

JSON :"""

    # Sonnet does the validation: more capable model, used only where
    # judgment adds value (cost-versus-quality allocation).
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=200,
        messages=[{"role": "user", "content": judge_prompt}],
    )

    raw = response.content[0].text.strip()

    # LLMs often wrap JSON in Markdown fences (```json ... ```).
    # Strip them before parsing, otherwise json.loads() fails.
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):]
        raw = raw.strip()

    # Safety net: if the judge's output is not valid JSON, return a cautious verdict.
    try:
        verdict = json.loads(raw)
    except json.JSONDecodeError:
        verdict = {"grounded": False, "reason": f"Unparseable judge output: {raw}"}

    return verdict


if __name__ == "__main__":
    question = "Combien de temps j'ai pour declarer un vol de voiture ?"
    print(f"Question: {question}\n")

    answer, chunks = generate_answer(question)
    print("--- Generated answer (Haiku) ---")
    print(answer)

    print("\n--- Judge verdict (Sonnet) ---")
    verdict = judge_answer(question, answer, chunks)
    print(f"Grounded: {verdict['grounded']}")
    print(f"Reason  : {verdict['reason']}")

    # Anti-hallucination test: feed the judge a deliberately false answer
    # to confirm it gets rejected. A judge that always says yes is worthless.
    print("\n" + "=" * 55)
    print("ANTI-HALLUCINATION TEST (deliberately false answer)")
    print("=" * 55 + "\n")

    fake_answer = "En cas de vol, vous avez 30 jours pour declarer le sinistre."
    print(f"Fabricated answer: {fake_answer}\n")

    fake_verdict = judge_answer(question, fake_answer, chunks)
    print("--- Judge verdict (Sonnet) ---")
    print(f"Grounded: {fake_verdict['grounded']}")
    print(f"Reason  : {fake_verdict['reason']}")