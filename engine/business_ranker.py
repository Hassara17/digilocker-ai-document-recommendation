class BusinessRanker:

    def __init__(self):
        pass

    # ==========================================================
    # NORMALIZE
    # ==========================================================

    def normalize(self, text):

        if not text:
            return ""

        return (
            text.lower()
            .strip()
        )

    # ==========================================================
    # VEHICLE INTENT
    # ==========================================================

    def is_vehicle_query(self, query):

        query = self.normalize(query)

        vehicle_keywords = [

            # General
            "vehicle",
            "vehicle documents",
            "vehicle document",
            "automobile",

            # Bike
            "bike",
            "bikes",
            "motorcycle",
            "motorcycles",
            "scooter",
            "scooters",

            # Car
            "car",
            "cars",

            # Purchase
            "bought a bike",
            "bought bike",
            "buy a bike",
            "buy bike",
            "buying a bike",
            "buying bike",

            "purchased a bike",
            "purchase a bike",

            "bought a car",
            "buy a car",
            "buying a car",
            "purchased a car",

            "new bike",
            "new car",
            "new vehicle",

            # Documents
            "registration",
            "rc",
            "insurance",
            "vehicle insurance",
            "driving license",
            "driving licence",
            "challan",
            "road tax",
            "vehicle tax",
            "fitness certificate"
        ]

        return any(
            keyword in query
            for keyword in vehicle_keywords
        )

    # ==========================================================
    # TAX INTENT
    # ==========================================================

    def is_tax_query(self, query):

        query = self.normalize(query)

        tax_keywords = [

            "income tax",
            "income-tax",
            "itr",
            "tax filing",
            "tax return",
            "file tax",
            "filing tax",
            "tax documents",
            "tds",
            "form 16",
            "salary tax"
        ]

        return any(
            keyword in query
            for keyword in tax_keywords
        )

    # ==========================================================
    # EDUCATION INTENT
    # ==========================================================

    def is_education_query(self, query):

        query = self.normalize(query)

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
            "academic",
            "apaar",
            "university",
            "graduation"
        ]

        return any(
            keyword in query
            for keyword in education_keywords
        )

    # ==========================================================
    # SCORE
    # ==========================================================

    def score(
        self,
        document,
        query="",
        user=None
    ):

        if not query:
            return 0.0

        query_lower = self.normalize(query)

        document_name = (
            document.document_name
        )

        score = 0.0

        # ======================================================
        # VEHICLE INTENT
        # ======================================================

        if self.is_vehicle_query(query_lower):

            vehicle_priority = {

                "Vehicle Registration": 1.00,

                "Vehicle Insurance": 0.90,

                "Driving License": 0.75,

                "Vehicle Tax Receipt": 0.65,

                "Vehicle Fitness Certificate": 0.55,

                "Challan": 0.20
            }

            score = vehicle_priority.get(
                document_name,
                0.0
            )

            # --------------------------------------------------
            # PURCHASE INTENT
            # --------------------------------------------------

            purchase_words = [
                "bought",
                "buy",
                "buying",
                "purchased",
                "purchase",
                "new"
            ]

            is_purchase = any(
                word in query_lower
                for word in purchase_words
            )

            if is_purchase:

                purchase_priority = {

                    "Vehicle Registration": 0.20,

                    "Vehicle Insurance": 0.15,

                    "Driving License": 0.10,

                    "Vehicle Tax Receipt": 0.10
                }

                score += purchase_priority.get(
                    document_name,
                    0.0
                )

            # --------------------------------------------------
            # REGISTRATION
            # --------------------------------------------------

            if (
                "registration" in query_lower
                or " rc" in f" {query_lower}"
                or query_lower.startswith("rc")
            ):

                if document_name == "Vehicle Registration":
                    score += 0.20

            # --------------------------------------------------
            # INSURANCE
            # --------------------------------------------------

            if "insurance" in query_lower:

                if document_name == "Vehicle Insurance":
                    score += 0.20

            # --------------------------------------------------
            # LICENSE
            # --------------------------------------------------

            if (
                "license" in query_lower
                or "licence" in query_lower
            ):

                if document_name == "Driving License":
                    score += 0.20

            # --------------------------------------------------
            # TAX
            # --------------------------------------------------

            if (
                "road tax" in query_lower
                or "vehicle tax" in query_lower
                or "tax receipt" in query_lower
            ):

                if document_name == "Vehicle Tax Receipt":
                    score += 0.20

            # --------------------------------------------------
            # FITNESS
            # --------------------------------------------------

            if "fitness" in query_lower:

                if document_name == "Vehicle Fitness Certificate":
                    score += 0.20

            # --------------------------------------------------
            # CHALLAN
            # --------------------------------------------------

            if "challan" in query_lower:

                if document_name == "Challan":
                    score += 0.30

        # ======================================================
        # TAX INTENT
        # ======================================================

        elif self.is_tax_query(query_lower):

            tax_priority = {

                "Form 16": 0.90,

                "TDS Certificate": 0.85,

                "ePAN": 0.70,

                "PAN Card": 0.65,

                "Passport": 0.10
            }

            score = tax_priority.get(
                document_name,
                0.0
            )

            # --------------------------------------------------
            # TDS
            # --------------------------------------------------

            if "tds" in query_lower:

                if document_name == "TDS Certificate":
                    score += 0.15

            # --------------------------------------------------
            # FORM 16
            # --------------------------------------------------

            if "form 16" in query_lower:

                if document_name == "Form 16":
                    score += 0.15

            # --------------------------------------------------
            # PAN
            # --------------------------------------------------

            if "pan" in query_lower:

                if document_name in [
                    "PAN Card",
                    "ePAN"
                ]:

                    score += 0.15

        # ======================================================
        # EDUCATION INTENT
        # ======================================================

        elif self.is_education_query(query_lower):

            education_priority = {

                "Class X Marksheet": 0.80,

                "Class XII Marksheet": 0.80,

                "APAAR ID": 0.65,

                "Degree Certificate": 0.60,

                "Provisional Degree Certificate": 0.50,

                "Diploma Certificate": 0.50,

                "Bonafide Certificate": 0.45
            }

            score = education_priority.get(
                document_name,
                0.0
            )

            # --------------------------------------------------
            # CLASS X
            # --------------------------------------------------

            if (
                "10th" in query_lower
                or "class x" in query_lower
            ):

                if document_name == "Class X Marksheet":
                    score += 0.15

                elif document_name == "Class XII Marksheet":
                    score -= 0.10

            # --------------------------------------------------
            # CLASS XII
            # --------------------------------------------------

            if (
                "12th" in query_lower
                or "class xii" in query_lower
            ):

                if document_name == "Class XII Marksheet":
                    score += 0.15

                elif document_name == "Class X Marksheet":
                    score -= 0.10

            # --------------------------------------------------
            # DEGREE
            # --------------------------------------------------

            if "degree" in query_lower:

                if document_name == "Degree Certificate":
                    score += 0.20

            # --------------------------------------------------
            # APAAR
            # --------------------------------------------------

            if "apaar" in query_lower:

                if document_name == "APAAR ID":
                    score += 0.20

        # ======================================================
        # PROFILE SIGNALS
        #
        # IMPORTANT:
        # Profile should NEVER dominate query intent.
        # ======================================================

        if user is not None:

            # --------------------------------------------------
            # VEHICLE OWNER
            # --------------------------------------------------

            if getattr(
                user,
                "vehicle_owner",
                False
            ):

                vehicle_profile_priority = {

                    "Vehicle Registration": 0.08,

                    "Vehicle Insurance": 0.06,

                    "Driving License": 0.04
                }

                score += vehicle_profile_priority.get(
                    document_name,
                    0.0
                )

            # --------------------------------------------------
            # TAXPAYER
            # --------------------------------------------------

            if getattr(
                user,
                "taxpayer",
                False
            ):

                tax_profile_priority = {

                    "PAN Card": 0.05,

                    "ePAN": 0.04,

                    "Form 16": 0.03,

                    "TDS Certificate": 0.03
                }

                score += tax_profile_priority.get(
                    document_name,
                    0.0
                )

            # --------------------------------------------------
            # STUDENT
            # --------------------------------------------------

            if getattr(
                user,
                "student",
                False
            ):

                education_profile_priority = {

                    "APAAR ID": 0.06,

                    "Class X Marksheet": 0.04,

                    "Class XII Marksheet": 0.04,

                    "Degree Certificate": 0.03,

                    "Bonafide Certificate": 0.03
                }

                score += education_profile_priority.get(
                    document_name,
                    0.0
                )

        # ======================================================
        # NORMALIZE BUSINESS SCORE
        #
        # Always return 0.0 - 1.0
        # ======================================================

        score = max(
            0.0,
            min(
                1.0,
                score
            )
        )

        return score