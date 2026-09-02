# Semantic retrieval: fetch the chunks closest in meaning to a question.

import chromadb


def get_collection():
    """Reconnect to the already-built persistent vector store."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="faq_assurance")
    return collection


def retrieve(question, k=3):
    """Return the k chunks closest in meaning to the question."""
    collection = get_collection()

    results = collection.query(
        query_texts=[question],
        n_results=k,
    )

    # ChromaDB returns a list per query; we only have one question.
    chunks = results["documents"][0]
    distances = results["distances"][0]

    return chunks, distances


if __name__ == "__main__":
    question = "Mon vehicule a ete accidente, quelles sont les premieres choses a faire ?"
    print(f"Question: {question}\n")

    chunks, distances = retrieve(question)

    print(f"Top {len(chunks)} chunks retrieved:\n")
    for i, (chunk, dist) in enumerate(zip(chunks, distances)):
        print(f"[{i}] (distance {dist:.3f})")
        print(f"    {chunk[:100]}...\n")