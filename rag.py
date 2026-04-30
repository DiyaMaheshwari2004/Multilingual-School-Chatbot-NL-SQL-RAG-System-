documents = [
    "Assignments are class-based and updated regularly.",
    "Marks are stored subject-wise for each student.",
    "Timetable is fixed based on class schedule.",
    "Parents can view their child's academic performance.",
    "Students can access only their own data."
]

def retrieve_context(query):
    query = query.lower()

    for doc in documents:
        if any(word in doc.lower() for word in query.split()):
            return doc

    return "I can help with marks, assignments, and timetable."
