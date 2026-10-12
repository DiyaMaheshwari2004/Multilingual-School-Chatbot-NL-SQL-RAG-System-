from pypdf import PdfReader

reader = PdfReader("school_docs_/School Policies.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

chunk_size = 500
overlap = 100

chunks = []

for i in range(0, len(text), chunk_size - overlap):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])