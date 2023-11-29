from CandidateGeneration import query_wikidata
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def link_entity(context, named_entity):
    candidates = query_wikidata(named_entity)

    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    context_embedding = model.encode(context)

    combined_scores = []
    for candidate in candidates:
        candidate_embedding = model.encode(
            f'title: {candidate["Label"]}, description: {candidate["Description"]}'
        )

        entity_similarity = cosine_similarity(
            [context_embedding], [candidate_embedding]
        )[0][0]

        combined_score = entity_similarity
        combined_scores.append(combined_score)

    most_relevant_index = np.argmax(combined_scores)

    return candidates[most_relevant_index]
