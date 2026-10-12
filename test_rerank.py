from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

query = "What is minimum attendance required?"

chunks = [
    "Students must maintain at least 75% attendance.",
    "Field trip attendance is recorded.",
    "Library books must be returned in 14 days."
]

pairs = [[query, chunk] for chunk in chunks]

scores = model.predict(pairs)

for chunk, score in zip(chunks, scores):
    print(score, "->", chunk)