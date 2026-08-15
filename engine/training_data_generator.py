import csv

from engine.feature_builder import FeatureBuilder


class TrainingDataGenerator:

    def __init__(
        self,
        kb,
        graph,
        candidate_generator
    ):

        self.kb = kb
        self.graph = graph
        self.generator = candidate_generator
        self.feature_builder = FeatureBuilder()

    # ==================================================
    # TRAINING QUERIES
    # ==================================================

    def get_training_queries(self):

        return [

            # ------------------------------------------
            # VEHICLE
            # ------------------------------------------

            {
                "query": "I bought a bike",
                "relevant_documents": [
                    "Vehicle Registration",
                    "Vehicle Insurance",
                    "Driving License",
                    "Challan"
                ]
            },

            {
                "query": "I purchased a car",
                "relevant_documents": [
                    "Vehicle Registration",
                    "Vehicle Insurance",
                    "Driving License",
                    "Challan"
                ]
            },

            {
                "query": "I bought a new vehicle",
                "relevant_documents": [
                    "Vehicle Registration",
                    "Vehicle Insurance",
                    "Driving License"
                ]
            },

            {
                "query": "I need documents for my motorcycle",
                "relevant_documents": [
                    "Vehicle Registration",
                    "Vehicle Insurance",
                    "Driving License"
                ]
            },

            {
                "query": "I need vehicle registration documents",
                "relevant_documents": [
                    "Vehicle Registration"
                ]
            },

            # ------------------------------------------
            # TAX
            # ------------------------------------------

            {
                "query": "I want to file my income tax",
                "relevant_documents": [
                    "Form 16",
                    "TDS Certificate",
                    "ePAN"
                ]
            },

            {
                "query": "I need my tax documents",
                "relevant_documents": [
                    "Form 16",
                    "TDS Certificate",
                    "ePAN"
                ]
            },

            {
                "query": "I need my TDS certificate",
                "relevant_documents": [
                    "TDS Certificate"
                ]
            },

            # ------------------------------------------
            # EDUCATION
            # ------------------------------------------

            {
                "query": "I need my school marksheet",
                "relevant_documents": [
                    "Class X Marksheet",
                    "Class XII Marksheet"
                ]
            },

            {
                "query": "I need my 12th marksheet",
                "relevant_documents": [
                    "Class XII Marksheet"
                ]
            },

            {
                "query": "I need my 10th marksheet",
                "relevant_documents": [
                    "Class X Marksheet"
                ]
            },

            {
                "query": "I need my education documents",
                "relevant_documents": [
                    "APAAR ID",
                    "Class X Marksheet",
                    "Class XII Marksheet"
                ]
            }
        ]

    # ==================================================
    # GENERATE TRAINING DATA
    # ==================================================

    def generate(
        self,
        users,
        output_file
    ):

        rows = []

        training_queries = (
            self.get_training_queries()
        )

        for user in users:

            for training_item in training_queries:

                query = training_item[
                    "query"
                ]

                relevant_documents = (
                    training_item[
                        "relevant_documents"
                    ]
                )

                print(
                    f"\nTraining query: {query}"
                )

                # ------------------------------------------
                # Generate candidates
                # ------------------------------------------

                candidates = (
                    self.generator.generate(
                        user,
                        query
                    )
                )

                for candidate in candidates:

                    # Candidate is a dictionary
                    doc_name = candidate[
                        "document"
                    ]

                    document = (
                        self.kb.get_document(
                            doc_name
                        )
                    )

                    if document is None:
                        continue

                    # ------------------------------------------
                    # Scores from CandidateGenerator
                    # ------------------------------------------

                    semantic_score = float(
                        candidate.get(
                            "semantic_score",
                            0.0
                        )
                    )

                    graph_score = int(
                        candidate.get(
                            "graph_score",
                            0
                        )
                    )

                    # ------------------------------------------
                    # Build features
                    # ------------------------------------------

                    features = (
                        self.feature_builder.build(
                            user,
                            document,
                            semantic_score,
                            graph_score
                        )
                    )

                    # ------------------------------------------
                    # REAL LABEL
                    # ------------------------------------------

                    if (
                        doc_name
                        in relevant_documents
                    ):

                        label = 1

                    else:

                        label = 0

                    row = dict(
                        features
                    )

                    row["label"] = label

                    rows.append(
                        row
                    )

        # ==================================================
        # CHECK DATASET
        # ==================================================

        if not rows:

            raise ValueError(
                "No training data was generated."
            )

        # ==================================================
        # SAVE CSV
        # ==================================================

        fieldnames = list(
            rows[0].keys()
        )

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(rows)

        print(
            "\n========================================"
        )

        print(
            "Training dataset generated."
        )

        print(
            "Total rows:",
            len(rows)
        )

        print(
            "Output:",
            output_file
        )

        print(
            "========================================"
        )