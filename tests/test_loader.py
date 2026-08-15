from engine.knowledge_base import KnowledgeBase

kb = KnowledgeBase("data/documents.json")

documents = kb.get_all_documents()

print("====================================")
print("KNOWLEDGE BASE TEST")
print("====================================")

print("Total documents:", len(documents))

print("\nDocuments:")

for doc in documents:
    print(
        f"{doc.document_name} - "
        f"{doc.category}"
    )