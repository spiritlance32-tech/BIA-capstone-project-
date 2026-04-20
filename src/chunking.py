def chunk_text(text, size=800, overlap=100):
    """
    Splits text into meaningful overlaps. 
    Smaller chunks (500 chars) are better for TinyLlama.
    """
    # Simple recursive-style split if you don't want to install langchain
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for p in paragraphs:
        if len(current_chunk) + len(p) < size:
            current_chunk += p + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks
