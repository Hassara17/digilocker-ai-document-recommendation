from engine.knowledge_base import KnowledgeBase
from engine.feature_builder import FeatureBuilder
from models.user import User


print("=" * 60)
print("FEATURE BUILDER TEST")
print("=" * 60)

# Load Knowledge Base
kb = KnowledgeBase("data/documents.json")
documents = kb.get_all_documents()

print(f"Total documents: {len(documents)}")

# Create test user
user = User(
    age=22,
    occupation="Student",
    state="Delhi",
    vehicle_owner=True,
    taxpayer=True,
    student=True,
    existing_documents=[]
)

# Create FeatureBuilder
builder = FeatureBuilder()

# Generate features for every document
for document in documents:

    features = builder.build(
        user=user,
        document=document,
        semantic_score=0.50,
        graph_score=1
    )

    print("\n" + "-" * 60)
    print(f"DOCUMENT: {document.document_name}")
    print(f"CATEGORY: {document.category}")
    print("FEATURES:")

    for key, value in features.items():
        print(f"{key}: {value}")

print("\n" + "=" * 60)
print("FEATURE BUILDER TEST COMPLETED")
print("=" * 60)