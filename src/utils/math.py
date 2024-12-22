import math


def simple_cosine_similarity(vec1, vec2):
    dot   = sum(x * y for x, y in zip(vec1, vec2))
    norm1 = math.sqrt(sum(x * x for x in vec1))
    norm2 = math.sqrt(sum(y * y for y in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)
