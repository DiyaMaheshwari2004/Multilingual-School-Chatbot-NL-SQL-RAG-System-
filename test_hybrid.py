from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss
import numpy as np

# ---------------- LOAD PDF ----------------

reader = PdfReader("school_docs_/School Policies.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

# ---------------- CHUNKING ----------------

chunks = []

chunk_size = 500
overlap = 100

for i in range(0, len(text), chunk_size - overlap):
    chunks.append(text[i:i + chunk_size])

print("Chunks:", len(chunks))

# ---------------- BM25 ----------------

tokenized_chunks = [chunk.lower().split() for chunk in chunks]

bm25 = BM25Okapi(tokenized_chunks)

# ---------------- EMBEDDINGS ----------------

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

# ---------------- QUERY ----------------

query = "What is the minimum attendance required?"

# BM25 top results
bm25_scores = bm25.get_scores(query.lower().split())

bm25_ranked = np.argsort(bm25_scores)[::-1][:5]

# Dense top results
query_embedding = model.encode([query])

distances, dense_ranked = index.search(
    np.array(query_embedding).astype("float32"),
    5
)

dense_ranked = dense_ranked[0]

# ---------------- RRF ----------------

rrf_scores = {}

k = 60

for rank, idx in enumerate(bm25_ranked):
    rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (k + rank)

for rank, idx in enumerate(dense_ranked):
    rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (k + rank)

final_results = sorted(
    rrf_scores.items(),
    key=lambda x: x[1],
    reverse=True
)

print("\nHYBRID RETRIEVAL RESULTS:\n")

for i, (idx, score) in enumerate(final_results[:3], start=1):
    print(f"\nResult {i} | RRF Score: {score:.4f}")
    print(chunks[idx][:400])