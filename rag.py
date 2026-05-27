documents = [
    "Assignments are class-based and updated regularly.",
    "Marks are stored subject-wise for each student.",
    "Timetable is fixed based on class schedule.",
    "Parents can view their child's academic performance.",
    "Students can access only their own data."
]

# Dummy function so app.py doesn't crash
def create_embeddings():
    print("Lightweight RAG Loaded")

# Search function
def search_rag(query):
    query = query.lower()

    for doc in documents:
        if any(word in doc.lower() for word in query.split()):
            return doc

    return "No relevant information found."