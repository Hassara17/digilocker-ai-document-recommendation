from engine.knowledge_base import KnowledgeBase
from engine.graph_builder import DocumentGraph
from engine.relationships import build_relationships
from engine.recommender import RecommendationEngine
from models.user import User

# Load documents
kb = KnowledgeBase("data/documents.json")

# Create graph
graph = DocumentGraph()

# Add all documents as nodes
for doc in kb.get_all_documents():
    graph.add_document(doc)

# Build relationships
build_relationships(graph)

# Create recommendation engine
engine = RecommendationEngine(kb, graph)

# Test user
user = User(
    age=22,
    occupation="Student",
    state="Delhi",
    vehicle_owner=True,
    taxpayer=True,
    student=True,
    existing_documents=[
        "Driving License",
        "PAN Card",
        "APAAR ID"
    ]
)

recommendations = engine.recommend(user)

print("\nRecommended Documents:\n")

for doc in recommendations:
    print("•", doc)