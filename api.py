# FastAPI service exposing the RAG pipeline (generation + judging).

from fastapi import FastAPI
from pydantic import BaseModel

from generate import generate_answer
from judge import judge_answer

app = FastAPI(title="Insurance RAG Assistant")


# Request body schema. FastAPI validates it automatically and returns
# a 422 if the payload does not match.
class AskRequest(BaseModel):
    question: str
    k: int = 3


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    # Generate the grounded answer, then validate it with the judge.
    answer, chunks = generate_answer(req.question, k=req.k)
    verdict = judge_answer(req.question, answer, chunks)

    # Return the answer, the verdict and the sources. Exposing the sources
    # is part of the contract: traceability matters in an insurance context.
    return {
        "question": req.question,
        "answer": answer,
        "grounded": verdict["grounded"],
        "judge_reason": verdict["reason"],
        "sources": chunks,
    }