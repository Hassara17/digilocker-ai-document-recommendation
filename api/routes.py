from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from models.user import User

from engine.knowledge_base import KnowledgeBase
from engine.graph_builder import DocumentGraph
from engine.vector_store import VectorStore
from engine.candidate_generator import CandidateGenerator
from engine.recommendation_engine import RecommendationEngine


router = APIRouter()


# ============================================================
# LOAD RECOMMENDATION SYSTEM
# ============================================================

print("\nLoading Knowledge Base...")

kb = KnowledgeBase(
    "data/documents.json"
)


print("\nBuilding Document Graph...")

graph = DocumentGraph()

graph.build_from_knowledge_base(
    kb.get_all_documents()
)


print("\nLoading Vector Store...")

store = VectorStore()


print("\nAdding documents to Vector Store...")

for document in kb.get_all_documents():

    try:

        store.add_document(document)

    except Exception as e:

        print(
            f"Error adding "
            f"{document.document_name}: {e}"
        )


print("\nCreating Candidate Generator...")

generator = CandidateGenerator(
    kb,
    graph,
    store
)


print("\nCreating Recommendation Engine...")

recommendation_engine = RecommendationEngine(
    kb,
    graph,
    generator
)


print("\nRecommendation System Loaded Successfully.\n")


# ============================================================
# REQUEST MODEL
# ============================================================

class RecommendationRequest(BaseModel):

    age: int = 22

    occupation: str = ""

    state: str = ""

    vehicle_owner: bool = False

    taxpayer: bool = False

    student: bool = False

    existing_documents: List[str] = []

    query: str = ""


# ============================================================
# ROOT
# ============================================================

@router.get("/")
def home():

    return {
        "status": "success",
        "message": "DigiLocker Recommendation API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# RECOMMENDATION
# ============================================================

@router.post("/recommend")
def recommend(
    request: RecommendationRequest
):

    # ========================================================
    # CREATE USER
    # ========================================================

    user = User(

        age=request.age,

        occupation=request.occupation,

        state=request.state,

        vehicle_owner=request.vehicle_owner,

        taxpayer=request.taxpayer,

        student=request.student,

        existing_documents=
            request.existing_documents
    )


    # ========================================================
    # RUN RECOMMENDATION ENGINE
    # ========================================================

    recommendations = (
        recommendation_engine.recommend(
            user,
            query=request.query
        )
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return {

        "status": "success",

        "query": request.query,

        "user": {

            "age": user.age,

            "occupation":
                user.occupation,

            "state":
                user.state,

            "vehicle_owner":
                user.vehicle_owner,

            "taxpayer":
                user.taxpayer,

            "student":
                user.student,

            "existing_documents":
                user.existing_documents
        },

        "recommendations":
            recommendations
    }