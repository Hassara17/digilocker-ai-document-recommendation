
import json
import os


class RuleEngine:

    def __init__(
        self,
        rules_path="rules/rules.json"
    ):

        self.rules_path = rules_path

        self.rules = self._load_rules()

    # ==================================================
    # LOAD RULES
    # ==================================================

    def _load_rules(self):

        print(
            "\nLoading Rule Engine..."
        )

        if not os.path.exists(
            self.rules_path
        ):

            raise FileNotFoundError(
                f"Rules file not found: "
                f"{self.rules_path}"
            )

        with open(
            self.rules_path,
            "r",
            encoding="utf-8"
        ) as file:

            rules = json.load(file)

        print(
            "Rules loaded successfully."
        )

        return rules

    # ==================================================
    # DETECT INTENT
    # ==================================================

    def detect_intent(
        self,
        query
    ):

        if not query:

            return "general"

        query_lower = query.lower()

        best_intent = "general"

        best_match_count = 0

        # ==================================================
        # CHECK EACH INTENT
        # ==================================================

        for intent, config in self.rules.items():

            # Skip non-intent configuration
            if intent in [
                "general",
                "ranking"
            ]:

                continue

            keywords = config.get(
                "keywords",
                []
            )

            match_count = 0

            for keyword in keywords:

                if keyword.lower() in query_lower:

                    match_count += 1

            if match_count > best_match_count:

                best_match_count = match_count

                best_intent = intent

        return best_intent

    # ==================================================
    # INFER USER PROFILE
    # ==================================================

    def infer_profile(
        self,
        user,
        query
    ):

        query_lower = (
            query.lower()
            if query
            else ""
        )

        vehicle_owner = bool(
            getattr(
                user,
                "vehicle_owner",
                False
            )
        )

        taxpayer = bool(
            getattr(
                user,
                "taxpayer",
                False
            )
        )

        student = bool(
            getattr(
                user,
                "student",
                False
            )
        )

        # ==================================================
        # QUERY BASED INFERENCE
        # ==================================================

        vehicle_keywords = [
            "bike",
            "motorcycle",
            "scooter",
            "car",
            "vehicle",
            "automobile",
            "bought a bike",
            "bought a car",
            "purchased a bike",
            "purchased a car",
            "new vehicle"
        ]

        tax_keywords = [
            "tax",
            "income tax",
            "itr",
            "tds",
            "salary tax",
            "tax return",
            "file tax",
            "tax filing"
        ]

        education_keywords = [
            "school",
            "college",
            "student",
            "education",
            "marksheet",
            "10th",
            "12th",
            "class x",
            "class xii",
            "degree",
            "admission",
            "study",
            "academic",
            "apaar"
        ]

        if any(
            keyword in query_lower
            for keyword in vehicle_keywords
        ):

            vehicle_owner = True

        if any(
            keyword in query_lower
            for keyword in tax_keywords
        ):

            taxpayer = True

        if any(
            keyword in query_lower
            for keyword in education_keywords
        ):

            student = True

        return {
            "vehicle_owner": vehicle_owner,
            "taxpayer": taxpayer,
            "student": student
        }

    # ==================================================
    # SPECIFIC RULE MATCHING
    # ==================================================

    def apply_specific_rules(
        self,
        intent,
        query
    ):

        query_lower = (
            query.lower()
            if query
            else ""
        )

        intent_config = self.rules.get(
            intent,
            {}
        )

        specific_rules = (
            intent_config.get(
                "specific_rules",
                {}
            )
        )

        scores = {}

        # ==================================================
        # CHECK SPECIFIC RULES
        # ==================================================

        for rule_name, documents in (
            specific_rules.items()
        ):

            # Match rule name against query
            if rule_name.lower() in query_lower:

                # documents is a dictionary
                for (
                    document,
                    score
                ) in documents.items():

                    scores[document] = (
                        scores.get(
                            document,
                            0.0
                        )
                        + float(score)
                    )

        # ==================================================
        # SPECIAL CASE:
        # "school marksheet"
        # ==================================================

        if (
            intent == "education"
            and (
                "school marksheet"
                in query_lower
                or "school mark sheet"
                in query_lower
            )
        ):

            school_rules = (
                specific_rules.get(
                    "school_marksheet",
                    {}
                )
            )

            for (
                document,
                score
            ) in school_rules.items():

                scores[document] = (
                    scores.get(
                        document,
                        0.0
                    )
                    + float(score)
                )

        return scores

    # ==================================================
    # RECOMMEND DOCUMENTS
    # ==================================================

    def recommend(
        self,
        user,
        query
    ):

        print(
            "\n========== RULE ENGINE =========="
        )

        print(
            "Query:",
            query
        )

        # ==================================================
        # DETECT INTENT
        # ==================================================

        intent = self.detect_intent(
            query
        )

        print(
            "Detected intent:",
            intent
        )

        # ==================================================
        # INFER PROFILE
        # ==================================================

        profile = self.infer_profile(
            user,
            query
        )

        print(
            "Inferred vehicle owner:",
            profile["vehicle_owner"]
        )

        print(
            "Inferred taxpayer:",
            profile["taxpayer"]
        )

        print(
            "Inferred student:",
            profile["student"]
        )

        print(
            "================================="
        )

        # ==================================================
        # GET INTENT CONFIGURATION
        # ==================================================

        intent_config = self.rules.get(
            intent,
            {}
        )

        base_documents = (
            intent_config.get(
                "documents",
                {}
            )
        )

        # ==================================================
        # START DOCUMENT SCORES
        # ==================================================

        scores = {}

        for (
            document,
            score
        ) in base_documents.items():

            scores[document] = float(
                score
            )

        # ==================================================
        # APPLY SPECIFIC RULES
        # ==================================================

        specific_scores = (
            self.apply_specific_rules(
                intent,
                query
            )
        )

        for (
            document,
            score
        ) in specific_scores.items():

            scores[document] = (
                scores.get(
                    document,
                    0.0
                )
                + score
            )

        # ==================================================
        # PROFILE BASED BOOST
        # ==================================================

        if profile["vehicle_owner"]:

            vehicle_documents = [
                "Vehicle Registration",
                "Vehicle Insurance",
                "Driving License",
                "Challan"
            ]

            for document in (
                vehicle_documents
            ):

                if document in scores:

                    scores[document] += 0.10

        # ==================================================

        if profile["taxpayer"]:

            tax_documents = [
                "Form 16",
                "TDS Certificate",
                "ePAN",
                "PAN Card"
            ]

            for document in (
                tax_documents
            ):

                if document in scores:

                    scores[document] += 0.10

        # ==================================================

        if profile["student"]:

            education_documents = [
                "APAAR ID",
                "Class X Marksheet",
                "Class XII Marksheet",
                "Degree Certificate"
            ]

            for document in (
                education_documents
            ):

                if document in scores:

                    scores[document] += 0.10

        # ==================================================
        # REMOVE EXISTING DOCUMENTS
        # ==================================================

        existing_documents = getattr(
            user,
            "existing_documents",
            []
        )

        for document in list(
            scores.keys()
        ):

            if document in existing_documents:

                print(
                    f"Rule Engine removing existing: "
                    f"{document}"
                )

                del scores[document]

        # ==================================================
        # MINIMUM SCORE
        # ==================================================

        ranking_config = self.rules.get(
            "ranking",
            {}
        )

        minimum_score = float(
            ranking_config.get(
                "minimum_score",
                0.0
            )
        )

        # ==================================================
        # FILTER
        # ==================================================

        scores = {
            document: score
            for document, score
            in scores.items()
            if score >= minimum_score
        }

        # ==================================================
        # SORT
        # ==================================================

        scores = dict(
            sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        # ==================================================
        # MAX RECOMMENDATIONS
        # ==================================================

        maximum = int(
            ranking_config.get(
                "maximum_recommendations",
                10
            )
        )

        scores = dict(
            list(
                scores.items()
            )[:maximum]
        )

        # ==================================================
        # PRINT RESULTS
        # ==================================================

        print(
            "\n========== RULE RESULTS =========="
        )

        for (
            document,
            score
        ) in scores.items():

            print(
                f"{document}: "
                f"{score:.4f}"
            )

        print(
            "=================================="
        )

        return scores

