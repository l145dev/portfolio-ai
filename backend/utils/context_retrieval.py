from data.portfolio import portfolio
from utils.clean_query import clean_query

# semantic retrieval with ChromaDB
def query_chroma(chroma_client, query: str):
    collection = chroma_client.get_or_create_collection("aryan_portfolio")
    results = collection.query(query_texts=[query], n_results=5)
    return results["documents"][0] if results.get("documents") else []

# keyword retrieval with BM25
def sort_index_by_score(scored_chunks: list) -> list:
    # item is (index, score)
    # sort based on score
    if len(scored_chunks) <= 1:
        return scored_chunks

    lower = []
    higher = []
    partition = scored_chunks[0][1]

    for i in range(1, len(scored_chunks)):
        if scored_chunks[i][1] > partition:
            higher.append(scored_chunks[i])
        else:
            lower.append(scored_chunks[i])

    return sort_index_by_score(lower) + [(scored_chunks[0][0], partition)] + sort_index_by_score(higher)

def query_bm25(BM25Okapi, groq_client, query: str, top_k = 5):
    # extract chunks
    corpus = []

    for item in portfolio:
        chunk = item['document'].lower().split()
        corpus.append(chunk)

    # initialize bm25
    bm25 = BM25Okapi(corpus)

    # user query handling
    query_items = clean_query(groq_client, query=query).lower().split(" ")

    # scoring
    scores = bm25.get_scores(query_items)  # returns a list of scores, same order as corpus

    # score sorting desc
    index_score = []

    # attach indices to scores to match with portfolio_chroma indexes after sorting
    for i in range(len(scores)):
        index_score.append((i, scores[i]))

    # sort tuples array index_score desc
    sorted_index_scores = sort_index_by_score(index_score)[::-1]

    # get top k index_scores
    index_scores_top_k = sorted_index_scores[0:min(len(sorted_index_scores), top_k)]

    # top k chunks
    top_chunks = []

    for i, chunk in index_scores_top_k:
        top_chunks.append(portfolio[i]['document'])

    return top_chunks