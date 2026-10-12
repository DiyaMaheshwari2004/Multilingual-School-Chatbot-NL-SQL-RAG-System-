import os
import json
import faiss
import numpy as np
import requests

from datetime import datetime
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi

# =====================================
# LOAD MODELS
# =====================================

print("Loading models...")

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# =====================================
# LOAD PDFS
# =====================================

documents = []

for root, dirs, files in os.walk("school_docs_"):

    for file in files:

        if file.endswith(".pdf"):

            path = os.path.join(root, file)

            try:

                reader = PdfReader(path)

                text = ""

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text

                chunk_size = 500
                overlap = 100

                for i in range(
                    0,
                    len(text),
                    chunk_size - overlap
                ):

                    chunk = text[
                        i:i + chunk_size
                    ].strip()

                    if len(chunk) > 50:
                        documents.append(chunk)

                print(f"Loaded {file}")

            except Exception as e:

                print(
                    f"Error loading {path}"
                )
                print(e)

# Remove duplicate chunks
documents = list(
    dict.fromkeys(documents)
)

MAX_CHUNKS = 500

if len(documents) > MAX_CHUNKS:
    documents = documents[:MAX_CHUNKS]

print(
    "\nUnique chunks:",
    len(documents)
)

# =====================================
# BM25 INDEX
# =====================================

tokenized_docs = [
    doc.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized_docs)

print("BM25 index ready")

# =====================================
# FAISS INDEX
# =====================================

embedding_file = "embeddings.npy"

if os.path.exists(embedding_file):

    print("Loading saved embeddings...")

    embeddings = np.load(embedding_file)

    if len(embeddings) != len(documents):

        print("Document count changed.")
        print("Rebuilding embeddings...")

        embeddings = embed_model.encode(
            documents,
            convert_to_numpy=True,
            batch_size=16,
            show_progress_bar=True
        )

        np.save(
            embedding_file,
            embeddings
        )

        print("Embeddings rebuilt and saved.")

else:

    print("Creating embeddings...")

    embeddings = embed_model.encode(
        documents,
        convert_to_numpy=True,
        batch_size=16,
        show_progress_bar=True
    )

    np.save(
        embedding_file,
        embeddings
    )

    print("Embeddings saved.")

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(embeddings)

print("FAISS index ready")

# =====================================
# USER QUERY
# =====================================

query = input("\nQuestion: ")

# =====================================
# BM25 RETRIEVAL
# =====================================

tokenized_query = query.lower().split()

bm25_scores = bm25.get_scores(
    tokenized_query
)

bm25_top = np.argsort(
    bm25_scores
)[::-1][:5]

# =====================================
# VECTOR RETRIEVAL
# =====================================

query_embedding = embed_model.encode(
    [query],
    convert_to_numpy=True,
    normalize_embeddings=True
)

D, I = index.search(
    query_embedding,
    5
)

# =====================================
# HYBRID RETRIEVAL
# =====================================

rrf_scores = {}

for rank, idx in enumerate(bm25_top):
    rrf_scores[int(idx)] = (
        rrf_scores.get(int(idx), 0)
        + 1 / (60 + rank)
    )

for rank, idx in enumerate(I[0]):
    rrf_scores[int(idx)] = (
        rrf_scores.get(int(idx), 0)
        + 1 / (60 + rank)
    )

candidate_ids = set()

for idx in I[0]:
    candidate_ids.add(int(idx))

for idx in bm25_top:
    candidate_ids.add(int(idx))

candidate_docs = [
    documents[i]
    for i in candidate_ids
]
if not candidate_docs:
    print(
        "\nNo candidate documents found."
    )
    exit()

print("\nRETRIEVED CHUNKS:\n")

for i, doc in enumerate(
    candidate_docs,
    start=1
):

    print(f"\n--- Chunk {i} ---")
    print(doc[:400])

# =====================================
# RERANK
# =====================================

pairs = [
    [query, doc]
    for doc in candidate_docs
]

scores = reranker.predict(
    pairs
)

ranked = sorted(
    zip(scores, candidate_docs),
    key=lambda x: x[0],
    reverse=True
)

# Keep only highly relevant docs
top_docs = []

for score, doc in ranked:

    if score > 2.0:
        top_docs.append(doc)

    if len(top_docs) >= 5:
        break

if len(top_docs) == 0:

    print(
        "\nNo relevant documents found."
    )
    exit()

top_score = float(
    ranked[0][0]
)

# =====================================
# CONFIDENCE
# =====================================

confidence = float(
    1 / (
        1 + np.exp(-top_score)
    )
)

print(
    "\nConfidence:",
    round(confidence, 3)
)

# =====================================
# LOW CONFIDENCE FALLBACK
# =====================================

if confidence < 0.35:

    answer = (
        "I could not find a reliable "
        "answer in the provided documents."
    )

    print("\nANSWER:\n")
    print(answer)

    exit()

# =====================================
# CONTEXT
# =====================================

context = ""

for idx, doc in enumerate(
    top_docs,
    start=1
):

    context += (
        f"[{idx}] {doc}\n\n"
    )

# =====================================
# PROMPT
# =====================================

prompt = f"""
You are a document QA system.

Use ONLY the passages.

If the answer is not found, reply exactly:

I could not find the answer in the provided documents.

PASSAGES:
{context}

QUESTION:
{query}

Return ONLY:

Answer: <answer>

Sources: [1], [2]

Do not explain.
Do not justify.
Do not mention requirements.
Do not add extra text.
"""

# =====================================
# OLLAMA
# =====================================

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "top_docs": 0.1
        }
    },
    timeout=120
)

if response.status_code != 200:

    print(
        "\nOllama Error:"
    )

    print(response.text)

    exit()

data = response.json()

answer = data.get(
    "response",
    "No response generated."
)

# =====================================
# OUTPUT
# =====================================

print("\nANSWER:\n")
print(answer)

# =====================================
# SOURCES
# =====================================

print("\nSOURCES:\n")

for idx, doc in enumerate(
    top_docs,
    start=1
):

    print(
        f"[{idx}] "
        f"{doc[:200]}...\n"
    )

# =====================================
# LOGGING
# =====================================

log = {

    "timestamp": str(datetime.now()),
    "query": query,
    "confidence": confidence,
    "top_score": top_score,

    "retrieved_docs":
        len(candidate_docs),

    "reranked_docs":
        len(top_docs),

    "answer": answer,

    "sources": [
        doc[:300]
        for doc in top_docs
    ]
}

with open(
    "rag_logs.jsonl",
    "a",
    encoding="utf-8"
) as f:

    f.write(
        json.dumps(log)
        + "\n"
    )

print(
    "\nRequest logged to rag_logs.jsonl"
)