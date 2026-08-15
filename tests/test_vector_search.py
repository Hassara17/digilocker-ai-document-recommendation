from engine.knowledge_base import KnowledgeBase
from engine.vector_store import VectorStore

kb = KnowledgeBase("data/documents.json")

store = VectorStore()

for doc in kb.get_all_documents():

    try:
        store.add_document(doc)

    except Exception as e:
        print(
            f"Error adding {doc.document_name}: {e}"
        )


query = "I bought a bike"

results = store.search(
    query,
    n_results=10
)

print("\n========== SEMANTIC RESULTS ==========")

for result in results:

    print(
        result["document"],
        "->",
        result["semantic_score"]
    )