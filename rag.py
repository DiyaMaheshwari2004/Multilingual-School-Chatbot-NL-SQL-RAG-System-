import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pypdf import PdfReader

# ---------------- MODEL ----------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- STORAGE ----------------

documents = []
embeddings = None
index = None

# ---------------- LOAD PDF TEXT ----------------

def load_pdfs(folder_path):

    global documents

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            path = os.path.join(folder_path, file)

            try:
                reader = PdfReader(path)

                text = ""

                for page in reader.pages:

                    extracted = page.extract_text()

                    if extracted:
                        text += extracted

                # Split into chunks
                chunks = split_text(text)

                for chunk in chunks:

                    documents.append({
                        "source": file,
                        "text": chunk
                    })

                print(f"Loaded PDF: {file}")

            except Exception as e:

                print(f"Error loading {file}: {e}")

# ---------------- TEXT SPLITTER ----------------

def split_text(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])

        chunks.append(chunk)

    return chunks

# ---------------- CREATE EMBEDDINGS ----------------

def create_embeddings(folder_path="school_docs_"):

    global embeddings
    global index

    load_pdfs(folder_path)

    if not documents:

        print("No PDFs found.")
        return

    texts = [doc["text"] for doc in documents]

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    print("✅ Embeddings created successfully")

# ---------------- SEARCH RAG ----------------

def search_rag(query, top_k=3):

    global index

    if index is None:

        return "Knowledge base not loaded."

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(documents):

            results.append(documents[idx]["text"])

    if not results:

        return "No relevant information found."

    return "\n\n".join(results)