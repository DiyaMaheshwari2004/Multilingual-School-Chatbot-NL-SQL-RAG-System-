from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

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

print("Chunks:", len(chunks))

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

print("FAISS vectors:", index.ntotal)