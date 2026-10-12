import requests

context = """
Students must maintain at least 75% attendance during the academic year.
Students below this percentage may not be allowed to appear for final examinations.
"""

query = "What is the minimum attendance requirement?"

prompt = f"""
You are a school assistant.

Answer ONLY from the provided passages.

Passages:
{context}

Question:
{query}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
)

print(response.json()["response"])