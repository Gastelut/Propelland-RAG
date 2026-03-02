from dotenv import load_dotenv
import os, sys
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(url="http://localhost:6333")

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