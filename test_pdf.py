from pypdf import PdfReader

reader = PdfReader("school_docs_/School Policies.pdf")

print(reader.pages[0].extract_text())