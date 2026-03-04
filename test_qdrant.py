from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

QDRANT_PATH = r"C:\Users\Bastian\propelland-rag-data\qdrant"
PROJECT_COLLECTION = "project_cards"

# Initialize Qdrant client
qdrant = QdrantClient(path=QDRANT_PATH)

print("Current collections:", qdrant.get_collections())

# Create a test point
point = PointStruct(
    id=1,
    vector=[0.1, 0.2, 0.3],
    payload={
        "project_name": "Test Project",
        "company": "Test Company",
        "industry": "Test Industry",
        "services": ["Test Service 1", "Test Service 2"],
        "summary": "This is a test project",
        "path": "C:\\test\\path"
    }
)

# Upsert the point
try:
    qdrant.upsert(collection_name=PROJECT_COLLECTION, points=[point])
    print("Upsert successful")
    
    # Check if collection exists
    print("Collections after upsert:", qdrant.get_collections())
    
    # Query the collection
    hits = qdrant.query_points(
        collection_name=PROJECT_COLLECTION,
        query=[0.1, 0.2, 0.3],
        limit=1
    )
    print("Query results:", hits.points)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")