from engine.knowledge_base import KnowledgeBase
from engine.vector_store import VectorStore

print("1. Loading Knowledge Base...")
kb = KnowledgeBase("data/documents.json")
print("✓ Knowledge Base Loaded")

print("2. Creating Vector Store...")
store = VectorStore()
print("✓ Vector Store Created")

print("3. Adding Documents...")

for doc in kb.get_all_documents():
    print("Adding:", doc.document_name)
    store.add_document(doc)

print("✓ All Documents Added")

print("4. Searching...")
result = store.search("I have a bike")

print("Search Result:")
print(result)