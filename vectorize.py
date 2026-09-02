# Build the ChromaDB vector store from the document chunks.

import chromadb

from ingest import load_document, chunk_document


def build_vector_store(chunks):
    """Create a persistent ChromaDB store and add the chunks to it."""

    # Persistent client: the store is written to disk so we index once
    # and reuse it across runs instead of re-embedding every time.
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="faq_assurance")

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # add() embeds each document locally and stores vector + text + id.
    collection.add(documents=chunks, ids=ids)

    return collection


if __name__ == "__main__":
    text = load_document("faq_assurance.txt")
    chunks = chunk_document(text)

    collection = build_vector_store(chunks)

    print(f"Vector store built: {collection.count()} chunks stored")
    print("Persisted to ./chroma_db")