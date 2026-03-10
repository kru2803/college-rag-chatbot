import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Start ChromaDB
client = chromadb.Client()

collection = client.get_or_create_collection(name="knowledge")

# Load knowledge
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

# Insert embeddings
for i, chunk in enumerate(documents):
    embedding = embedding_model.encode(chunk).tolist()

    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        ids=[str(i)]
    )
print("Knowledge indexed.")

while True:
    question = input("\nAsk question: ")

    if question.lower() == "exit":
        break

    query_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    #print("\nRetrieved Context:\n")
    #for doc in results["documents"][0]:
    #    print(doc)

    

    context = " ".join(results["documents"][0])

    prompt = f"""
    Use the context below to answer the question.

    Context:
    {context}

    Question:
    {question}
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    print("Answer:", response["message"]["content"])