def keyword_match_context(chunks, question, max_chunks=3):
    keywords = [word.strip() for word in question.lower().split() if len(word.strip()) >= 2]
    
    scored_chunks = []
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = sum(1 for kw in keywords if kw in chunk_lower)
        scored_chunks.append((score, i, chunk))
    
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    
    matched = [chunk for score, idx, chunk in scored_chunks if score > 0]
    
    if matched:
        print(f"[QA] Found {len(matched)} chunks matching {len(keywords)} keywords, using top {min(max_chunks, len(matched))}")
        return "\n".join(matched[:max_chunks])
    else:
        print(f"[QA] No keyword matches found, falling back to first {max_chunks} chunks")
        return "\n".join(chunks[:max_chunks])