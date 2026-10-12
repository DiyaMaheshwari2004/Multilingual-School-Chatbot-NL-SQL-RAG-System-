from pypdf import PdfReader
from rank_bm25 import BM25Okapi

reader = PdfReader("school_docs_/School Policies.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

chunks = []

chunk_size = 500
overlap = 100

for i in range(0, len(text), chunk_size - overlap):
    chunks.append(text[i:i + chunk_size])

tokenized_chunks = [chunk.lower().split() for chunk in chunks]

bm25 = BM25Okapi(tokenized_chunks)

query = "minimum attendance requirement"

results = bm25.get_top_n(
    query.lower().split(),
    chunks,
    n=3
)

print("\nTop Results:\n")

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(result[:300])