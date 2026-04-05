def split_into_passages(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = start + chunk_size
        chunks.append(cleaned[start:end])
        start += max(chunk_size - overlap, 1)
    return chunks
