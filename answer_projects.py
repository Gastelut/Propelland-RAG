from dotenv import load_dotenv
import os, sys
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(url="http://localhost:6333")

question = sys.argv[1]
TOPK = 8

q_emb = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
).data[0].embedding

hits = qdrant.query_points(
    collection_name="project_cards",
    query=q_emb,
    limit=TOPK,
    with_payload=True
).points

sources = []
for i, h in enumerate(hits, start=1):
    p = h.payload or {}
    sources.append(
        f"[PROJECT {i}] score={h.score}\n"
        f"project_name: {p.get('project_name')}\n"
        f"company: {p.get('company')}\n"
        f"industry: {p.get('industry')}\n"
        f"services: {p.get('services')}\n"
        f"summary: {p.get('summary')}\n"
        f"path: {p.get('path')}\n"
    )

context = "\n".join(sources)

sys_prompt = (
    "You answer using ONLY the provided PROJECT sources.\n"
    "If the answer is not supported by the sources, say you don't have enough data.\n"
    "When you mention a project/company, cite it like [PROJECT 1].\n"
    "End with a Sources section listing each cited PROJECT with its path."
)

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": f"Question: {question}\n\nSources:\n{context}"}
    ]
)

print(resp.choices[0].message.content)