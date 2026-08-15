from engine.knowledge_base import KnowledgeBase
from engine.graph_builder import DocumentGraph
from engine.vector_store import VectorStore
from engine.candidate_generator import CandidateGenerator
from engine.training_data_generator import TrainingDataGenerator

from models.user import User

kb = KnowledgeBase("data/documents.json")

graph = DocumentGraph()

graph.add_relation("Driving License", "Vehicle Registration")
graph.add_relation("Vehicle Registration", "Vehicle Insurance")
graph.add_relation("Vehicle Insurance", "Challan")

graph.add_relation("APAAR ID", "Class X Marksheet")
graph.add_relation("Class X Marksheet", "Class XII Marksheet")
graph.add_relation("Class XII Marksheet", "Degree Certificate")

graph.add_relation("PAN Card", "ePAN")
graph.add_relation("ePAN", "Form 16")

store = VectorStore()

for doc in kb.get_all_documents():
    try:
        store.add_document(doc)
    except:
        pass

generator = CandidateGenerator(kb, graph, store)

users = [

    User(
        age=22,
        occupation="Student",
        state="Delhi",
        vehicle_owner=True,
        taxpayer=True,
        student=True,
        existing_documents=["Driving License"]
    ),

    User(
        age=35,
        occupation="Engineer",
        state="Delhi",
        vehicle_owner=True,
        taxpayer=True,
        student=False,
        existing_documents=["PAN Card"]
    ),

    User(
        age=18,
        occupation="Student",
        state="UP",
        vehicle_owner=False,
        taxpayer=False,
        student=True,
        existing_documents=[]
    )
]

trainer = TrainingDataGenerator(
    kb,
    graph,
    generator
)

trainer.generate(
    users,
    "data/training_data.csv"
)