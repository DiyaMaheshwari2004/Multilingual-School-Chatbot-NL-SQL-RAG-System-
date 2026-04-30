from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Students can check their marks subject-wise.",
    "Assignments are given class-wise and have deadlines.",
    "Timetable shows daily subject schedule.",
    "Parents can view their child academic data.",
    "Marks are stored per student and subject.",
    "School supports classes from 1 to 10.",
    "Parents can have maximum two children.",
    "You can ask questions in English, Hindi or Hinglish."
]

doc_embeddings = model.encode(documents)

def retrieve_context(query):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, doc_embeddings)[0]
    return documents[scores.argmax()]