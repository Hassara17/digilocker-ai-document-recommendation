from engine.rule_engine import RuleEngine


class CandidateGenerator:

    def __init__(
        self,
        kb,
        graph,
        vector_store
    ):

        self.kb = kb
        self.graph = graph
        self.vector_store = vector_store

        self.rule_engine = RuleEngine(
            "data/rules.json"
        )

    def generate(
        self,
        user,
        query=None
    ):

        candidates = {}

        # ==================================================
        # 1. RULE-BASED CANDIDATES
        # ==================================================

        rule_docs = self.rule_engine.recommend(
            user,
            query
        )

        for doc in rule_docs:

            if doc in user.existing_documents:
                continue

            candidates[doc] = {
                "document": doc,
                "semantic_score": 0.0,
                "graph_score": 0,
                "rule_score": 1
            }

        # ==================================================
        # 2. GRAPH-BASED CANDIDATES
        # ==================================================

        print(
            "\n========== EXISTING DOCUMENTS =========="
        )

        for existing_doc in user.existing_documents:

            print(
                "Existing:",
                existing_doc
            )

            if not self.graph.has_document(
                existing_doc
            ):

                print(
                    "NOT FOUND IN GRAPH"
                )

                continue

            connected_docs = (
                self.graph.next_documents(
                    existing_doc
                )
            )

            print(
                "Connected:",
                connected_docs
            )

            # ----------------------------------------------
            # Add connected documents as candidates
            # ----------------------------------------------

            for related_doc in connected_docs:

                if related_doc in user.existing_documents:
                    continue

                # Candidate does not exist yet
                if related_doc not in candidates:

                    candidates[related_doc] = {
                        "document": related_doc,
                        "semantic_score": 0.0,
                        "graph_score": 1,
                        "rule_score": 0
                    }

                # Candidate already exists from rules
                else:

                    candidates[related_doc][
                        "graph_score"
                    ] = 1

        print(
            "========================================\n"
        )

        # ==================================================
        # 3. SEMANTIC SEARCH
        # ==================================================

        if query:

            semantic_results = (
                self.vector_store.search(
                    query,
                    n_results=10
                )
            )

            for result in semantic_results:

                doc = result["document"]

                semantic_score = float(
                    result["semantic_score"]
                )

                # ------------------------------------------
                # Skip documents user already owns
                # ------------------------------------------

                if doc in user.existing_documents:
                    continue

                # ------------------------------------------
                # New semantic candidate
                # ------------------------------------------

                if doc not in candidates:

                    candidates[doc] = {
                        "document": doc,
                        "semantic_score": semantic_score,
                        "graph_score": 0,
                        "rule_score": 0
                    }

                # ------------------------------------------
                # Candidate already exists
                # ------------------------------------------

                else:

                    candidates[doc][
                        "semantic_score"
                    ] = semantic_score

        # ==================================================
        # 4. SCORE CANDIDATES NOT IN TOP SEMANTIC RESULTS
        # ==================================================

        if query:

            for doc_name, candidate in (
                candidates.items()
            ):

                if candidate[
                    "semantic_score"
                ] == 0.0:

                    candidate[
                        "semantic_score"
                    ] = float(
                        self.vector_store.score_document(
                            query,
                            doc_name
                        )
                    )

        # ==================================================
        # 5. DEBUG OUTPUT
        # ==================================================

        print(
            "\n========== CANDIDATE GENERATOR =========="
        )

        for candidate in candidates.values():

            print(
                f"{candidate['document']} | "
                f"semantic="
                f"{candidate['semantic_score']:.4f} | "
                f"graph="
                f"{candidate['graph_score']} | "
                f"rule="
                f"{candidate['rule_score']}"
            )

        print(
            "==========================================\n"
        )

        # ==================================================
        # 6. RETURN CANDIDATES
        # ==================================================

        return list(
            candidates.values()
        )