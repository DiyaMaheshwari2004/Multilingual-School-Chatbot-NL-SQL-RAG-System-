from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Students must maintain at least 75% attendance."

embedding = model.encode(text)

print("Embedding size:", len(embedding))