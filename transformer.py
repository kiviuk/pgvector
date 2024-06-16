#!/usr/bin/env python3

import torch
from sentence_transformers import SentenceTransformer, util

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
    )
    model = SentenceTransformer("all-MiniLM-L6-v2")

model.max_seq_length = 256

# Corpus with example sentences
corpus = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]
corpus_embeddings = model.encode(corpus, normalize_embeddings=True)

# ./transformer.py
# A cheetah is running behind its prey. (Score: 0.3135)
# A man is riding a white horse on an enclosed ground. (Score: 0.2358)
# A man is riding a horse. (Score: 0.2224)
# Two men pushed carts through the woods. (Score: 0.0692)
# The girl is carrying a baby. (Score: 0.0351)
query = "Who is having lunch ?"
query_embedding = model.encode(query, normalize_embeddings=True)

# Since the embeddings are normalized, we can use dot_score to find the highest 5 scores
dot_scores = util.dot_score(query_embedding, corpus_embeddings)[0]
top_results = torch.topk(dot_scores, k=5)

for score, idx in zip(top_results[0], top_results[1]):
    print(corpus[idx], "(Score: {:.4f})".format(score))
