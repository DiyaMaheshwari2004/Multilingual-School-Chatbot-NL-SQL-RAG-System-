import os
from PyPDF2 import PdfReader

# ---------------- STORE DOCUMENTS ----------------
documents = []


# ---------------- LOAD ALL PDF FILES ----------------
def load_pdfs():

    global documents

    base_folder = "school_docs_"

    if not os.path.exists(base_folder):
        print("school_docs folder not found")
        return

    for root, dirs, files in os.walk(base_folder):

        for file in files:

            if file.endswith(".pdf"):

                file_path = os.path.join(root, file)

                try:
                    reader = PdfReader(file_path)

                    full_text = ""

                    for page in reader.pages:

                        text = page.extract_text()

                        if text:
                            full_text += text + " "

                    documents.append({
                        "file_name": file,
                        "content": full_text.lower()
                    })

                    print(f"Loaded PDF: {file}")

                except Exception as e:
                    print(f"Error loading {file}: {e}")


# ---------------- SEARCH FUNCTION ----------------
def search_rag(query):

    query = query.lower()

    best_match = None
    highest_score = 0

    for doc in documents:

        score = 0

        for word in query.split():

            if word in doc["content"]:
                score += 1

        if score > highest_score:
            highest_score = score
            best_match = doc

    if best_match and highest_score > 0:

        content = best_match["content"][:1200]

        return (
            f"According to {best_match['file_name']}:\n\n"
            f"{content}"
        )

    return "No relevant information found in school documents."


# ---------------- LOAD PDFs ON STARTUP ----------------
load_pdfs()