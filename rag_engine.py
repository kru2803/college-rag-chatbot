import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

# load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# start chromadb
client = chromadb.Client()
collection = client.get_or_create_collection(name="knowledge")


def load_documents():

    documents = []
    data_folder = "data"

    for file in os.listdir(data_folder):

        file_path = os.path.join(data_folder, file)

        if file.endswith(".txt"):

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

                chunks = text.split("\n\n")

                for chunk in chunks:
                    if chunk.strip():
                        documents.append(chunk)

    # insert embeddings
    for i, chunk in enumerate(documents):

        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)]
        )


def ask_question(question):

    query_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    context = " ".join(results["documents"][0])

    prompt = f"""
You are EduRAG, an AI education assistant.

Context:
{context}

Question:
{question}

Answer clearly based on the context.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
