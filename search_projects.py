from dotenv import load_dotenv
import os, sys
import warnings
from openai import OpenAI
from qdrant_client import QdrantClient

# Suppress msvcrt import warning from portalocker (Windows specific)
warnings.filterwarnings("ignore", category=ImportWarning)

def main():
    load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Use local Qdrant storage instead of Docker
    qdrant = QdrantClient(path=r"C:\Users\Bastian\propelland-rag-data\qdrant")

    query = sys.argv[1]

    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    hits = qdrant.query_points(
        collection_name="project_cards",
        query=embedding,
        limit=5
    ).points

    for h in hits:
        print("\nScore:", h.score)
        print("Project:", h.payload.get("project_name"))
        print("Company:", h.payload.get("company"))
        print("Industry:", h.payload.get("industry"))
        print("Services:", h.payload.get("services"))
        print("Path:", h.payload.get("path"))
    
    # Properly close Qdrant client
    qdrant.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        sys.exit(1)