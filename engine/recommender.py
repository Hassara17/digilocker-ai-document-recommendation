from engine.rule_engine import RuleEngine
from engine.vector_store import VectorStore


class RecommendationEngine:

    def __init__(self, kb, graph):

        self.kb = kb
        self.graph = graph

        self.rule_engine = RuleEngine("data/rules.json")
        self.vector_store = VectorStore()

        # Load all documents into ChromaDB
        for doc in self.kb.get_all_documents():
            try:
                self.vector_store.add_document(doc)
            except Exception:
                # Ignore duplicate document IDs
                pass

    def recommend(self, user):

        recommendations = set()

        user_docs = set(user.existing_documents)

        # -----------------------------
        # 1. Rule-based recommendations
        # -----------------------------
        rule_docs = self.rule_engine.recommend(user)

        for doc in rule_docs:
            if doc not in user_docs:
                recommendations.add(doc)

        # -----------------------------
        # 2. Knowledge Graph recommendations
        # -----------------------------
        for doc in user_docs:

            if self.graph.has_document(doc):

                next_docs = self.graph.next_documents(doc)

                for next_doc in next_docs:

                    if next_doc not in user_docs:
                        recommendations.add(next_doc)

        return list(recommendations)