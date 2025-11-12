# process chunks w/ deduplication and reranking
def process_chunks(cohere_client, query: str, chunks: list) -> list:
    chunks = deduplicate_chunks(chunks)
    chunks = rerank_chunks(cohere_client, query, chunks)
    return chunks

# deduplication
def deduplicate_chunks(chunks: list) -> list:
    deduped_chunks = set()

    for result in chunks:
        if result not in deduped_chunks:
            deduped_chunks.add(result)

    return list(deduped_chunks)

# reranking
def rerank_chunks(cohere_client, query, chunks: list) -> list:
    response = cohere_client.rerank(
        model="rerank-v3.5",
        query=query,
        documents=chunks,
        top_n=4,
    )

    context_chunks = []

    if hasattr(response, "results") and isinstance(response.results, list):
        results = response.results

        for result in results:
            context_chunks.append(chunks[result.index])
    else:
        context_chunks = chunks

    return context_chunks