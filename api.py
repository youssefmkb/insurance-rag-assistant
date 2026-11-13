# FastAPI service exposing the RAG pipeline (generation + judging).

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from generate import generate_answer
from judge import judge_answer

app = FastAPI(title="Insurance RAG Assistant")

STATIC_DIR = Path(__file__).parent / "static"


# Request body schema. FastAPI validates it automatically and returns
# a 422 if the payload does not match. The bounds keep a public demo
# from sending huge prompts or retrieving the whole corpus.
class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    k: int = Field(default=3, ge=1, le=5)


@app.get("/", include_in_schema=False)
def home():
    # Single-page web UI: lets anyone try the pipeline without using the API docs.
    return FileResponse(STATIC_DIR / "index.html")


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
