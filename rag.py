from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import chromadb
import os

# ---------------- EMBEDDING MODEL ----------------
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ---------------- CHROMA DB ----------------
client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="school_rag"
)

# ---------------- DOCUMENT FOLDER ----------------
DOCS_FOLDER = "school_docs"

# ---------------- LOAD ALL PDFS ----------------
def load_pdfs():

    documents = []

    for root, dirs, files in os.walk(DOCS_FOLDER):

        for file in files:

            if file.endswith(".pdf"):

                pdf_path = os.path.join(root, file)

                try:

                    reader = PdfReader(pdf_path)

                    text = ""

                    for page in reader.pages:

                        extracted = page.extract_text()

                        if extracted:
                            text += extracted

                    documents.append({
                        "file": file,
                        "text": text
                    })

                    print(f"Loaded: {file}")

                except Exception as e:

                    print(f"Error reading {file}: {e}")

    return documents

# ---------------- SPLIT TEXT ----------------
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for doc in documents:

        split_texts = splitter.split_text(
            doc["text"]
        )

        for chunk in split_texts:

            chunks.append({
                "text": chunk,
                "source": doc["file"]
            })

    return chunks

# ---------------- CREATE EMBEDDINGS ----------------
def create_embeddings():

    existing = collection.count()

    if existing > 0:
        print("Embeddings already exist.")
        return

    print("Creating embeddings...")

    documents = load_pdfs()

    chunks = split_documents(documents)

    for index, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk["text"]
        ).tolist()

        collection.add(
            ids=[str(index)],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[
                {
                    "source": chunk["source"]
                }
            ]
        )

    print("Embeddings created successfully.")

# ---------------- SEARCH RAG ----------------
def search_rag(query):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = results["documents"][0]

    context = "\n\n".join(docs)

    return context