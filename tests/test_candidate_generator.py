from engine.knowledge_base import KnowledgeBase
from engine.graph_builder import DocumentGraph
from engine.vector_store import VectorStore
from engine.candidate_generator import CandidateGenerator
from models.user import User


# ==================================================
# 1. LOAD KNOWLEDGE BASE
# ==================================================

kb = KnowledgeBase(
    "data/documents.json"
)


# ==================================================
# 2. BUILD GRAPH FROM KNOWLEDGE BASE
# ==================================================

graph = DocumentGraph()

graph.build_from_knowledge_base(
    kb.get_all_documents()
)

graph.print_graph()


# ==================================================
# 3. CREATE VECTOR STORE
# ==================================================

store = VectorStore()


# ==================================================
# 4. ADD DOCUMENTS TO CHROMADB
# ==================================================

for doc in kb.get_all_documents():

    try:

        store.add_document(doc)

    except Exception as e:

        print(
            f"Error adding {doc.document_name}: {e}"
        )


# ==================================================
# 5. CREATE CANDIDATE GENERATOR
# ==================================================

generator = CandidateGenerator(
    kb,
    graph,
    store
)


# ==================================================
# 6. SAMPLE USER
# ==================================================

user = User(
    age=22,
    occupation="Student",
    state="Delhi",

    vehicle_owner=True,
    taxpayer=True,
    student=True,

    existing_documents=[
        "Driving License",
        "PAN Card"
    ]
)


# ==================================================
# 7. GENERATE CANDIDATES
# ==================================================

candidates = generator.generate(
    user,
    query="I bought a bike"
)


# ==================================================
# 8. DISPLAY RESULTS
# ==================================================

print(
    "\n========== FINAL CANDIDATES =========="
)

for candidate in candidates:

    print(
        f"{candidate['document']} | "
        f"semantic={candidate['semantic_score']:.4f} | "
        f"graph={candidate['graph_score']} | "
        f"rule={candidate['rule_score']}"
    )

print(
    "======================================="
)