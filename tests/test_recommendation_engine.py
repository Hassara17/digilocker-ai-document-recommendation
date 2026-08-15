from engine.knowledge_base import KnowledgeBase
from engine.graph_builder import DocumentGraph
from engine.vector_store import VectorStore
from engine.candidate_generator import CandidateGenerator
from engine.recommendation_engine import RecommendationEngine

from models.user import User


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

print("\n========================================")
print("LOADING KNOWLEDGE BASE")
print("========================================")

kb = KnowledgeBase(
    "data/documents.json"
)

print(
    "Documents loaded:",
    len(kb.get_all_documents())
)


# ============================================================
# BUILD DOCUMENT GRAPH
# ============================================================

print("\n========================================")
print("BUILDING DOCUMENT GRAPH")
print("========================================")

graph = DocumentGraph()

graph.build_from_knowledge_base(
    kb.get_all_documents()
)

graph.print_graph()


# ============================================================
# CREATE VECTOR STORE
# ============================================================

print("\n========================================")
print("CREATING VECTOR STORE")
print("========================================")

store = VectorStore()


# ============================================================
# ADD DOCUMENTS
# ============================================================

print("\nAdding documents to vector store...")

for doc in kb.get_all_documents():

    try:

        store.add_document(
            doc
        )

    except Exception as e:

        print(
            f"Error adding "
            f"{doc.document_name}: {e}"
        )


print(
    "Vector store ready."
)


# ============================================================
# CANDIDATE GENERATOR
# ============================================================

print("\n========================================")
print("CREATING CANDIDATE GENERATOR")
print("========================================")

generator = CandidateGenerator(
    kb,
    graph,
    store
)


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

print("\n========================================")
print("CREATING RECOMMENDATION ENGINE")
print("========================================")

engine = RecommendationEngine(
    kb,
    graph,
    generator
)


# ============================================================
# SAMPLE USER
# ============================================================

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


# ============================================================
# DISPLAY USER
# ============================================================

print("\n========================================")
print("TEST USER")
print("========================================")

print(
    "Age:",
    user.age
)

print(
    "Occupation:",
    user.occupation
)

print(
    "State:",
    user.state
)

print(
    "Student:",
    user.student
)

print(
    "Vehicle Owner:",
    user.vehicle_owner
)

print(
    "Taxpayer:",
    user.taxpayer
)

print(
    "Existing Documents:",
    user.existing_documents
)


# ============================================================
# TEST QUERY
# ============================================================

query = "I bought a bike"


print("\n========================================")
print("TEST QUERY")
print("========================================")

print(
    "Query:",
    query
)


# ============================================================
# RUN RECOMMENDATION ENGINE
# ============================================================

print("\n========================================")
print("RUNNING RECOMMENDATION ENGINE")
print("========================================")


recommendations = engine.recommend(
    user,
    query=query
)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n========================================")
print("FINAL RECOMMENDATIONS")
print("========================================")


if not recommendations:

    print(
        "No recommendations generated."
    )

else:

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"\n{index}. "
            f"{recommendation['document']}"
        )

        print(
            "   Category:",
            recommendation["category"]
        )

        print(
            "   Score:",
            round(
                recommendation["score"],
                4
            )
        )

        print(
            "   Reason:",
            recommendation["reason"]
        )

        # --------------------------------------------
        # DEBUG INFORMATION
        # --------------------------------------------

        print(
            "   XGBoost:",
            round(
                recommendation.get(
                    "xgb_score",
                    0
                ),
                4
            )
        )

        print(
            "   Semantic:",
            round(
                recommendation.get(
                    "semantic_score",
                    0
                ),
                4
            )
        )

        print(
            "   Graph:",
            round(
                recommendation.get(
                    "graph_score",
                    0
                ),
                4
            )
        )

        print(
            "   Business:",
            round(
                recommendation.get(
                    "business_score",
                    0
                ),
                4
            )
        )


# ============================================================
# TEST VALIDATION
# ============================================================

print("\n========================================")
print("TEST VALIDATION")
print("========================================")


recommended_documents = [

    recommendation["document"]

    for recommendation
    in recommendations
]


print(
    "\nRecommended documents:"
)

for document in recommended_documents:

    print(
        " -",
        document
    )


# ============================================================
# CHECK VEHICLE DOCUMENT
# ============================================================

if (
    "Vehicle Registration"
    in recommended_documents
):

    print(
        "\nPASS: Vehicle Registration "
        "was recommended."
    )

else:

    print(
        "\nWARNING: Vehicle Registration "
        "was not recommended."
    )


# ============================================================
# CHECK EXISTING DOCUMENTS
# ============================================================

existing_documents = set(
    user.existing_documents
)


invalid_results = [

    document

    for document
    in recommended_documents

    if document
    in existing_documents
]


if invalid_results:

    print(
        "\nFAIL: Existing documents "
        "were recommended:"
    )

    for document in invalid_results:

        print(
            " -",
            document
        )

else:

    print(
        "\nPASS: Existing documents "
        "were correctly excluded."
    )


# ============================================================
# COMPLETION
# ============================================================

print("\n========================================")
print("TEST COMPLETED")
print("========================================\n")