from src.utils.math import simple_cosine_similarity


async def naive_knn_search(all_records: dict, query_vector: list, k=5):
    neighbours = []
    for record_id, record in all_records.items():
        embedding = record.get('embedding', [])
        if embedding:
            similarity_score = simple_cosine_similarity(query_vector, embedding)
            neighbours.append((similarity_score, record))

    neighbours.sort(key=lambda x: x[0], reverse=True)
    top_k_slice   = neighbours[:k]
    top_k_records = []
    for similarity_score, record in top_k_slice:
        top_k_records.append(record)
    return top_k_records
