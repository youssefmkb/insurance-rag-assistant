# Load and chunk the source document.

def load_document(path):
    """Read a text file and return its full content."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def chunk_document(text):
    """Split the document into chunks: one chunk per FAQ section.

    Semantic chunking by section rather than fixed-size, because each
    question-and-answer block is already a self-contained unit of meaning.
    """
    raw_parts = text.split("## ")

    # Keep non-empty parts only, stripped of surrounding whitespace.
    chunks = [part.strip() for part in raw_parts if part.strip()]

    return chunks


if __name__ == "__main__":
    text = load_document("faq_assurance.txt")
    print(f"Document loaded: {len(text)} characters")

    chunks = chunk_document(text)
    print(f"Chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"[Chunk {i}] {chunk[:60]}...")