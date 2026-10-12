from sentence_transformers import CrossEncoder

print("Loading model...")

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

print("Model loaded successfully!")