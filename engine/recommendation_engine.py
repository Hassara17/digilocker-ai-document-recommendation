import json
import os
import re

from engine.feature_builder import FeatureBuilder
from engine.xgb_ranker import XGBoostRanker
from engine.explainer import RecommendationExplainer
from engine.business_ranker import BusinessRanker


class RecommendationEngine:

    def __init__(
        self,
        kb,
        graph,
        candidate_generator,
        documents_json_path="data/documents.json"
    ):

        self.kb = kb
        self.graph = graph
        self.generator = candidate_generator

        self.feature_builder = FeatureBuilder()
        self.ranker = XGBoostRanker()
        self.explainer = RecommendationExplainer()
        self.business_ranker = BusinessRanker()

        self.documents_json_path = documents_json_path

        # ======================================================
        # LOAD DOCUMENT CONFIGURATION
        # ======================================================

        self.document_config = self.load_document_config(
            documents_json_path
        )

        self.document_metadata = {}
        self.category_documents = {}

        self.build_document_indexes()

        # ======================================================
        # DOCUMENT KEYWORDS
        # ======================================================

        self.document_keywords = {

            # ==================================================
            # VEHICLE
            # ==================================================

            "Driving License": [
                "driving license",
                "driving licence",
                "driver license",
                "driver licence",
                "dl"
            ],

            "Vehicle Registration": [
                "vehicle registration",
                "vehicle registration certificate",
                "registration certificate",
                "vehicle rc",
                "rc"
            ],

            "Vehicle Insurance": [
                "vehicle insurance",
                "vehicle insurance document",
                "bike insurance",
                "my bike insurance",
                "insurance for bike",
                "insurance for my bike",
                "motorcycle insurance",
                "motorcycle insurance document",
                "car insurance",
                "insurance for car",
                "insurance for my car"
            ],

            "Challan": [
                "challan",
                "traffic challan",
                "traffic fine",
                "traffic fines"
            ],

            "Vehicle Tax Receipt": [
                "vehicle tax receipt",
                "vehicle tax",
                "road tax"
            ],

            "Vehicle Fitness Certificate": [
                "vehicle fitness certificate",
                "vehicle fitness",
                "fitness certificate"
            ],

            # ==================================================
            # TAX
            # ==================================================

            "PAN Card": [
                "pan card",
                "my pan card",
                "pan"
            ],

            "Form 16": [
                "form 16",
                "form16",
                "my form 16"
            ],

            "TDS Certificate": [
                "tds certificate",
                "tds",
                "my tds certificate"
            ],

            "ePAN": [
                "epan",
                "e-pan",
                "e pan"
            ],

            "Passport": [
                "passport",
                "my passport"
            ],

            # ==================================================
            # HEALTH
            # ==================================================

            "Health Card/ Certificate": [
                "health card",
                "health certificate",
                "health card certificate"
            ],

            "Pradhan Mantri Jan Arogya Yojana": [
                "pmjay",
                "pm jay",
                "ayushman bharat",
                "ayushman card",
                "pradhan mantri jan arogya yojana"
            ],

            "Health Fitness Certificate": [
                "health fitness certificate",
                "health fitness"
            ],

            "Policy Document-Health": [
                "health policy",
                "health insurance policy",
                "medical policy",
                "policy document health"
            ],

            # ==================================================
            # CATEGORY 5
            # ==================================================

            "UAN Card": [
                "uan card",
                "uan",
                "universal account number"
            ],

            "ePRAN Card": [
                "epran card",
                "epran",
                "e-pran",
                "e pran"
            ],

            "Pension Certificate": [
                "pension certificate",
                "pension document",
                "pension"
            ],

            "Ration Card": [
                "ration card"
            ],

            # ==================================================
            # CLASS X
            # ==================================================

            "APAAR ID": [
                "apaar id",
                "apaar"
            ],

            "Class X Marksheet": [
                "class x marksheet",
                "class 10 marksheet",
                "10th marksheet",
                "10th mark sheet",
                "class 10 mark sheet"
            ],

            "Class X Passing Certificate": [
                "class x passing certificate",
                "class 10 passing certificate",
                "10th passing certificate"
            ],

            "Class X Migration Certificate": [
                "class x migration certificate",
                "class 10 migration certificate",
                "10th migration certificate"
            ],

            "Class X School Leaving Certificate": [
                "class x school leaving certificate",
                "class 10 school leaving certificate",
                "10th school leaving certificate",
                "school leaving certificate"
            ],

            # ==================================================
            # CLASS XII
            # ==================================================

            "Class XII Marksheet": [
                "class xii marksheet",
                "class 12 marksheet",
                "12th marksheet",
                "12th mark sheet",
                "class 12 mark sheet"
            ],

            "Class XII Passing Certificate": [
                "class xii passing certificate",
                "class 12 passing certificate",
                "12th passing certificate"
            ],

            "Class XII Migration Certificate": [
                "class xii migration certificate",
                "class 12 migration certificate",
                "12th migration certificate"
            ],

            # ==================================================
            # HIGHER EDUCATION
            # ==================================================

            "Class I to IX Marksheets": [
                "class i to ix marksheets",
                "class 1 to 9 marksheets",
                "class 1 to 9 mark sheets",
                "school marksheets",
                "school mark sheets"
            ],

            "Degree Certificate": [
                "degree certificate",
                "degree document",
                "graduation certificate",
                "graduation degree",
                "my degree certificate"
            ],

            "Provisional Degree Certificate": [
                "provisional degree certificate",
                "provisional degree"
            ],

            "Diploma Certificate": [
                "diploma certificate",
                "diploma document"
            ],

            "Bonafide Certificate": [
                "bonafide certificate",
                "bonafide"
            ],

            # ==================================================
            # IDENTITY
            # ==================================================

            "Caste Certificate": [
                "caste certificate",
                "caste document",
                "sc certificate",
                "st certificate",
                "obc certificate"
            ],

            "Income Certificate": [
                "income certificate",
                "income proof"
            ],

            "Birth Certificate": [
                "birth certificate",
                "date of birth certificate"
            ],

            "CKYC Card": [
                "ckyc card",
                "ckyc"
            ],

            # ==================================================
            # HEALTH
            # ==================================================

            "Covid Vaccine Certificate": [
                "covid vaccine certificate",
                "covid vaccination certificate",
                "covid certificate",
                "vaccine certificate"
            ],

            "National Health ID Card": [
                "national health id card",
                "national health id",
                "health id",
                "abha card",
                "abha id",
                "abha"
            ],

            "Insurance - Health": [
                "health insurance",
                "medical insurance",
                "insurance health"
            ]
        }

        # ======================================================
        # CATEGORY / INTENT KEYWORDS
        # ======================================================

        self.intent_keywords = {

            # ==================================================
            # CLASS XII
            # ==================================================

            "class_xii": [
                "class xii documents",
                "class xii document",
                "class 12 documents",
                "class 12 document",
                "12th documents",
                "12th document",
                "class xii",
                "class 12",
                "12th class",
                "12th"
            ],

            # ==================================================
            # CLASS X
            # ==================================================

            "class_x": [
                "class x documents",
                "class x document",
                "class 10 documents",
                "class 10 document",
                "10th documents",
                "10th document",
                "class x",
                "class 10",
                "10th class",
                "10th"
            ],

            # ==================================================
            # HIGHER EDUCATION
            # ==================================================

            "higher_education": [

                "higher & other education docs",
                "higher and other education docs",
                "higher & other education documents",
                "higher and other education documents",

                "higher education docs",
                "higher education documents",

                "higher education",
                "higher studies",

                "college documents",
                "college document",

                "university documents",
                "university document",

                "academic record",
                "academic records",
                "academic document",
                "academic documents"
            ],

            # ==================================================
            # IDENTITY
            # ==================================================

            "identity": [
                "identity documents",
                "identity document",
                "identity proof",

                "identity & eligibility docs",
                "identity and eligibility docs",
                "eligibility documents",
                "eligibility document",

                "caste",
                "caste certificate",
                "sc certificate",
                "st certificate",
                "obc certificate",

                "income certificate",
                "income proof",

                "birth certificate",
                "date of birth certificate",

                "ration card",

                "ckyc",
                "ckyc card"
            ],

            # ==================================================
            # HEALTH
            # ==================================================

            "health_medical": [
                "health documents",
                "health document",
                "health & medical documents",
                "health and medical documents",

                "covid",
                "covid vaccine",
                "vaccine certificate",

                "health id",
                "national health id",
                "abha",

                "health insurance",
                "medical insurance",

                "healthcare",
                "health",
                "medical",
                "hospital",
                "doctor",

                "pmjay",
                "ayushman",
                "ayushman bharat"
            ],

            # ==================================================
            # CATEGORY 5
            # ==================================================

            "category_5": [
                "category 5",
                "category five",

                "uan",
                "uan card",
                "universal account number",

                "epf",
                "pf",
                "provident fund",
                "employee provident fund",

                "epran",
                "e-pran",
                "pran",

                "pension",
                "retirement",

                "employment",
                "employee document"
            ],

            # ==================================================
            # CATEGORY 3
            # ==================================================

            "category_3": [
                "category 3",
                "category three",

                "income tax",
                "income-tax",

                "income tax filing",
                "income tax document",
                "income tax documents",

                "itr",
                "itr filing",

                "tax filing",
                "tax return",

                "file tax",
                "file income tax",

                "filing tax",

                "tds",
                "form 16",

                "salary tax",
                "tax documents",

                "pan"
            ],

            # ==================================================
            # CATEGORY 2
            # ==================================================

            "category_2": [
                "category 2",
                "category two",

                "vehicle tax",
                "vehicle tax receipt",
                "road tax",

                "vehicle fitness",
                "vehicle fitness certificate",
                "fitness certificate",

                "challan",
                "traffic challan",
                "traffic fine",

                "vehicle compliance"
            ],

            # ==================================================
            # CATEGORY 1
            # ==================================================

            "category_1": [
                "category 1",
                "category one",

                "driving license",
                "driving licence",

                "vehicle registration",
                "registration certificate",

                "vehicle insurance",
                "car insurance",
                "bike insurance",

                "vehicle document",
                "vehicle documents",

                "driving document",

                "bike documents",
                "bike document",

                "car documents",
                "car document",

                "vehicle documents"
            ]
        }

    # ==========================================================
    # LOAD DOCUMENT JSON
    # ==========================================================

    def load_document_config(self, path):

        if not os.path.exists(path):

            raise FileNotFoundError(
                f"documents.json not found: {path}"
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):

            raise ValueError(
                "documents.json must contain a JSON list."
            )

        return data

    # ==========================================================
    # BUILD DOCUMENT INDEXES
    # ==========================================================

    def build_document_indexes(self):

        self.document_metadata = {}
        self.category_documents = {}

        for category_block in self.document_config:

            category = category_block.get(
                "category",
                "Unknown"
            )

            documents = category_block.get(
                "documents",
                []
            )

            self.category_documents[category] = []

            for document in documents:

                document_name = document.get(
                    "document_name"
                )

                if not document_name:
                    continue

                self.category_documents[
                    category
                ].append(document_name)

                # Store first metadata entry
                if document_name not in self.document_metadata:

                    self.document_metadata[
                        document_name
                    ] = {
                        "category": category,
                        "doctype": document.get(
                            "doctype",
                            ""
                        ),
                        "issuer_id": document.get(
                            "issuer_id",
                            ""
                        ),
                        "searchable": document.get(
                            "searchable",
                            False
                        )
                    }

        print(
            "\nLoaded document configuration:",
            len(self.document_metadata),
            "unique documents"
        )

    # ==========================================================
    # NORMALIZE TEXT
    # ==========================================================

    def normalize_text(self, text):

        if not text:
            return ""

        text = str(text).lower().strip()

        text = text.replace("/", " ")
        text = text.replace("-", " ")
        text = text.replace("_", " ")

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # ==========================================================
    # NORMALIZE DOCUMENT NAME
    # ==========================================================

    def normalize_document_name(self, name):

        return self.normalize_text(name)

    # ==========================================================
    # KEYWORD MATCH
    # ==========================================================

    def keyword_matches(
        self,
        query,
        keyword
    ):

        query = self.normalize_text(query)
        keyword = self.normalize_text(keyword)

        if not query or not keyword:
            return False

        pattern = (
            r"(?<![a-z0-9])"
            +
            re.escape(keyword)
            +
            r"(?![a-z0-9])"
        )

        return bool(
            re.search(
                pattern,
                query
            )
        )

    # ==========================================================
    # EXACT DOCUMENT INTENT
    # ==========================================================

    def detect_document_intent(self, query):

        if not query:
            return None

        query_normalized = self.normalize_text(
            query
        )

        matches = []

        for (
            document_name,
            keywords
        ) in self.document_keywords.items():

            for keyword in keywords:

                if self.keyword_matches(
                    query_normalized,
                    keyword
                ):

                    matches.append(
                        (
                            document_name,
                            len(
                                self.normalize_text(
                                    keyword
                                )
                            )
                        )
                    )

        if not matches:
            return None

        # Longest keyword = most specific
        matches.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return matches[0][0]

    # ==========================================================
    # CATEGORY INTENT
    # ==========================================================

    def detect_intent(self, query):

        if not query:
            return "general"

        query = self.normalize_text(
            query
        )

        # ======================================================
        # IMPORTANT ORDER
        # ======================================================
        #
        # Specific education categories first.
        # This prevents "class xii" from falling into
        # generic higher education.
        # ======================================================

        intent_order = [
            "class_xii",
            "class_x",
            "higher_education",
            "identity",
            "health_medical",
            "category_5",
            "category_3",
            "category_2",
            "category_1"
        ]

        # ------------------------------------------------------
        # SPECIAL VEHICLE DETECTION
        # ------------------------------------------------------

        vehicle_phrases = [
            "bought a bike",
            "bought bike",
            "purchased a bike",
            "purchased bike",

            "bought a car",
            "bought car",
            "purchased a car",
            "purchased car",

            "new bike",
            "new car",
            "new vehicle",

            "bike documents",
            "bike document",

            "car documents",
            "car document",

            "vehicle documents",
            "vehicle document"
        ]

        for phrase in vehicle_phrases:

            if self.keyword_matches(
                query,
                phrase
            ):

                return "category_1"

        # ------------------------------------------------------
        # NORMAL INTENT DETECTION
        # ------------------------------------------------------

        for intent in intent_order:

            keywords = self.intent_keywords.get(
                intent,
                []
            )

            for keyword in keywords:

                if self.keyword_matches(
                    query,
                    keyword
                ):

                    return intent

        return "general"

    # ==========================================================
    # CATEGORY MAPPING
    # ==========================================================

    def get_category_for_intent(
        self,
        intent
    ):

        mapping = {

            "category_1":
                "Category 1",

            "category_2":
                "Category 2",

            "category_3":
                "Category 3",

            "category_4":
                "Category 4",

            "category_5":
                "Category 5",

            "class_x":
                "Class X Documents",

            "class_xii":
                "Class XII Documents",

            "higher_education":
                "Higher & Other Education Docs",

            "identity":
                "Identity & Eligibility Docs",

            "health_medical":
                "Health & Medical Documents"
        }

        return mapping.get(intent)

    # ==========================================================
    # DOCUMENTS FOR INTENT
    # ==========================================================

    def get_documents_for_intent(
        self,
        intent
    ):

        category = self.get_category_for_intent(
            intent
        )

        if not category:
            return []

        return list(
            self.category_documents.get(
                category,
                []
            )
        )

    # ==========================================================
    # DOCUMENT CATEGORY
    # ==========================================================

    def get_document_category(
        self,
        document_name,
        intent=None
    ):

        # IMPORTANT:
        # If an intent category contains the document,
        # use that category.
        #
        # This fixes APAAR ID and other duplicate documents.

        if intent:

            intent_category = (
                self.get_category_for_intent(
                    intent
                )
            )

            if (
                intent_category
                and
                document_name in
                self.category_documents.get(
                    intent_category,
                    []
                )
            ):

                return intent_category

        metadata = self.document_metadata.get(
            document_name
        )

        if metadata:
            return metadata["category"]

        return "Unknown"

    # ==========================================================
    # KB LOOKUP
    # ==========================================================

    def get_kb_document(
        self,
        document_name
    ):

        try:

            document = self.kb.get_document(
                document_name
            )

            if document is not None:
                return document

        except Exception as error:

            print(
                "KB lookup failed:",
                document_name,
                error
            )

        return None

    # ==========================================================
    # CREATE CANDIDATE
    # ==========================================================

    def create_candidate(
        self,
        document_name,
        semantic_score=0.0,
        graph_score=0.0
    ):

        return {
            "document": document_name,
            "semantic_score": float(
                semantic_score
            ),
            "graph_score": float(
                graph_score
            )
        }

    # ==========================================================
    # ENSURE INTENT CANDIDATES
    # ==========================================================

    def ensure_intent_candidates(
        self,
        candidates,
        intent
    ):

        if intent == "general":
            return candidates

        required_documents = (
            self.get_documents_for_intent(
                intent
            )
        )

        existing_names = {
            self.normalize_document_name(
                candidate.get(
                    "document",
                    ""
                )
            )
            for candidate in candidates
        }

        for document_name in required_documents:

            normalized_name = (
                self.normalize_document_name(
                    document_name
                )
            )

            if normalized_name in existing_names:
                continue

            document = self.get_kb_document(
                document_name
            )

            if document is None:

                print(
                    "WARNING: Document exists in "
                    "documents.json but not KB:",
                    document_name
                )

                continue

            candidates.append(
                self.create_candidate(
                    document_name,
                    semantic_score=0.0,
                    graph_score=0.0
                )
            )

            existing_names.add(
                normalized_name
            )

        return candidates

    # ==========================================================
    # HARD INTENT FILTER
    # ==========================================================

    def filter_by_intent(
        self,
        candidates,
        intent
    ):

        allowed_documents = {
            self.normalize_document_name(
                name
            )
            for name in self.get_documents_for_intent(
                intent
            )
        }

        filtered = []

        for candidate in candidates:

            document_name = candidate.get(
                "document",
                ""
            )

            normalized_name = (
                self.normalize_document_name(
                    document_name
                )
            )

            if normalized_name in allowed_documents:

                filtered.append(candidate)

        return filtered

    # ==========================================================
    # EXACT DOCUMENT FILTER
    # ==========================================================

    def build_exact_document_candidates(
        self,
        candidates,
        document_name
    ):

        if not document_name:
            return candidates

        requested_normalized = (
            self.normalize_document_name(
                document_name
            )
        )

        filtered = []

        for candidate in candidates:

            candidate_name = candidate.get(
                "document",
                ""
            )

            if (
                self.normalize_document_name(
                    candidate_name
                )
                ==
                requested_normalized
            ):

                filtered.append(candidate)

        # If vector search missed it,
        # retrieve directly from KB.

        if not filtered:

            document = self.get_kb_document(
                document_name
            )

            if document is not None:

                filtered.append(
                    self.create_candidate(
                        document_name,
                        semantic_score=1.0,
                        graph_score=1.0
                    )
                )

        return filtered

    # ==========================================================
    # REASON
    # ==========================================================

    def get_reason(
        self,
        document_name,
        default_reason
    ):

        reasons = {

            "Driving License":
                "Driving License is relevant for driving and vehicle-related services.",

            "Vehicle Registration":
                "Vehicle Registration is relevant for vehicle ownership and registration records.",

            "Vehicle Insurance":
                "Vehicle Insurance is required for vehicle insurance coverage.",

            "Challan":
                "Challan information is relevant for vehicle and traffic-related requirements.",

            "Vehicle Tax Receipt":
                "Vehicle Tax Receipt is relevant for vehicle tax and road-tax records.",

            "Vehicle Fitness Certificate":
                "Vehicle Fitness Certificate is relevant for vehicle fitness and compliance.",

            "PAN Card":
                "PAN Card is relevant for tax identification, financial services and identity verification.",

            "Form 16":
                "Form 16 is relevant for income-tax filing and salary-related tax information.",

            "TDS Certificate":
                "TDS Certificate is relevant for verifying tax deducted at source.",

            "ePAN":
                "ePAN is relevant for PAN-based tax identification and verification.",

            "Passport":
                "Passport is relevant for identity verification and international travel.",

            "Health Card/ Certificate":
                "Health Card/Certificate is relevant for healthcare services and health records.",

            "Pradhan Mantri Jan Arogya Yojana":
                "Pradhan Mantri Jan Arogya Yojana is relevant for eligible government healthcare benefits.",

            "Health Fitness Certificate":
                "Health Fitness Certificate is relevant for health and fitness verification.",

            "Policy Document-Health":
                "Health policy documents are relevant for health insurance coverage and verification.",

            "UAN Card":
                "UAN Card is relevant for accessing your Universal Account Number and EPF-related services.",

            "ePRAN Card":
                "ePRAN Card is relevant for accessing your digital PRAN and pension-related services.",

            "Pension Certificate":
                "Pension Certificate is relevant for pension and retirement-related records.",

            "Ration Card":
                "Ration Card is relevant for household and public-distribution services.",

            "APAAR ID":
                "APAAR ID is relevant for digital academic identity and education-related records.",

            "Class X Marksheet":
                "Class X Marksheet is relevant for 10th-standard academic records.",

            "Class X Passing Certificate":
                "Class X Passing Certificate is relevant for proof of 10th-standard completion.",

            "Class X Migration Certificate":
                "Class X Migration Certificate is relevant for school and academic record transfer.",

            "Class X School Leaving Certificate":
                "Class X School Leaving Certificate is relevant for proof of leaving a school.",

            "Class XII Marksheet":
                "Class XII Marksheet is relevant for 12th-standard academic records.",

            "Class XII Passing Certificate":
                "Class XII Passing Certificate is relevant for proof of 12th-standard completion.",

            "Class XII Migration Certificate":
                "Class XII Migration Certificate is relevant for academic record transfer.",

            "Class I to IX Marksheets":
                "Class I to IX Marksheets are relevant for school-level academic records.",

            "Degree Certificate":
                "Degree Certificate is relevant for higher-education qualification verification.",

            "Provisional Degree Certificate":
                "Provisional Degree Certificate is useful when proof of degree completion is required before the final certificate is available.",

            "Diploma Certificate":
                "Diploma Certificate is relevant for academic qualification verification.",

            "Bonafide Certificate":
                "Bonafide Certificate is relevant for verifying student status and educational enrollment.",

            "Caste Certificate":
                "Caste Certificate is relevant for caste verification and eligibility for applicable government services and benefits.",

            "Income Certificate":
                "Income Certificate is relevant for verifying income and eligibility for applicable services.",

            "Birth Certificate":
                "Birth Certificate is relevant for verifying date and place of birth.",

            "CKYC Card":
                "CKYC Card is relevant for centralized KYC and identity verification.",

            "Covid Vaccine Certificate":
                "COVID Vaccine Certificate is relevant to vaccination and immunization records.",

            "National Health ID Card":
                "National Health ID Card is relevant for digital health identification and records.",

            "Insurance - Health":
                "Health Insurance is relevant for health insurance coverage and verification."
        }

        return reasons.get(
            document_name,
            default_reason
        )

    # ==========================================================
    # RECOMMEND
    # ==========================================================

    def recommend(
        self,
        user,
        query=""
    ):

        print("\n")
        print("=" * 60)
        print("             RECOMMENDATION ENGINE")
        print("=" * 60)

        print(
            "\nQuery:",
            query
        )

        # ======================================================
        # 1. EXACT DOCUMENT INTENT
        # ======================================================

        requested_document = (
            self.detect_document_intent(
                query
            )
        )

        if requested_document:

            print(
                "Requested Document:",
                requested_document
            )

        else:

            print(
                "Requested Document: None"
            )

        # ======================================================
        # 2. CATEGORY INTENT
        # ======================================================

        intent = self.detect_intent(
            query
        )

        print(
            "Detected Intent:",
            intent
        )

        intent_category = (
            self.get_category_for_intent(
                intent
            )
        )

        print(
            "Intent Category:",
            intent_category
        )

        # ======================================================
        # 3. GENERATE CANDIDATES
        # ======================================================

        print(
            "\n========== GENERATING CANDIDATES =========="
        )

        try:

            candidates = self.generator.generate(
                user,
                query
            )

        except Exception as error:

            print(
                "Candidate generator error:",
                error
            )

            candidates = []

        if candidates is None:
            candidates = []

        print(
            "Candidates before intent filtering:",
            len(candidates)
        )

        # ======================================================
        # 4. EXACT DOCUMENT REQUEST
        # ======================================================

        if requested_document:

            print(
                "\n========== EXACT DOCUMENT FILTER =========="
            )

            print(
                "Requested:",
                requested_document
            )

            candidates = (
                self.build_exact_document_candidates(
                    candidates,
                    requested_document
                )
            )

            print(
                "Candidates after exact-document filter:",
                len(candidates)
            )

        # ======================================================
        # 5. CATEGORY INTENT
        # ======================================================

        elif intent != "general":

            print(
                "\n========== INTENT FILTER =========="
            )

            print(
                "Intent:",
                intent
            )

            print(
                "Category:",
                intent_category
            )

            # --------------------------------------------------
            # Inject every document belonging to the intent
            # --------------------------------------------------

            candidates = (
                self.ensure_intent_candidates(
                    candidates,
                    intent
                )
            )

            print(
                "Candidates after injection:",
                len(candidates)
            )

            # --------------------------------------------------
            # HARD FILTER
            #
            # THIS IS THE MAIN FIX.
            #
            # XGBoost/Graph cannot introduce unrelated
            # documents after this point.
            # --------------------------------------------------

            candidates = (
                self.filter_by_intent(
                    candidates,
                    intent
                )
            )

            print(
                "Candidates after HARD intent filter:",
                len(candidates)
            )

            for candidate in candidates:

                print(
                    "  -",
                    candidate.get(
                        "document"
                    )
                )

        # ======================================================
        # 6. BUILD FEATURES
        # ======================================================

        feature_list = []
        documents = []
        valid_candidates = []

        print(
            "\n========== BUILDING FEATURES =========="
        )

        existing_documents = (
            getattr(
                user,
                "existing_documents",
                []
            )
            or []
        )

        existing_normalized = {

            self.normalize_document_name(
                document
            )

            for document in existing_documents
        }

        for candidate in candidates:

            doc_name = candidate.get(
                "document",
                ""
            )

            # --------------------------------------------------
            # SKIP EXISTING DOCUMENT
            # --------------------------------------------------

            if (
                self.normalize_document_name(
                    doc_name
                )
                in existing_normalized
            ):

                print(
                    "SKIPPING EXISTING DOCUMENT:",
                    doc_name
                )

                continue

            # --------------------------------------------------
            # KB DOCUMENT
            # --------------------------------------------------

            document = self.get_kb_document(
                doc_name
            )

            if document is None:

                print(
                    "WARNING: Document not found in KB:",
                    doc_name
                )

                continue

            semantic_score = float(
                candidate.get(
                    "semantic_score",
                    0.0
                )
            )

            graph_score = float(
                candidate.get(
                    "graph_score",
                    0.0
                )
            )

            # --------------------------------------------------
            # FEATURES
            # --------------------------------------------------

            try:

                features = self.feature_builder.build(
                    user,
                    document,
                    semantic_score,
                    graph_score
                )

            except Exception as error:

                print(
                    "Feature building failed for",
                    doc_name,
                    ":",
                    error
                )

                continue

            feature_list.append(
                features
            )

            documents.append(
                document
            )

            valid_candidates.append(
                candidate
            )

            print(
                f"{doc_name} | "
                f"Semantic={semantic_score:.4f} | "
                f"Graph={graph_score:.4f}"
            )

        # ======================================================
        # 7. NO CANDIDATES
        # ======================================================

        if not feature_list:

            print(
                "\nNo valid candidates available."
            )

            return []

        # ======================================================
        # 8. XGBOOST
        # ======================================================

        print(
            "\n========== XGBOOST RANKING =========="
        )

        try:

            xgb_scores = self.ranker.score(
                feature_list
            )

        except Exception as error:

            print(
                "XGBoost ranking failed:",
                error
            )

            xgb_scores = [
                0.0
                for _ in feature_list
            ]

        # ======================================================
        # 9. FINAL SCORE
        # ======================================================

        results = []

        print(
            "\n========== FINAL SCORE CALCULATION =========="
        )

        for (
            document,
            xgb_score,
            candidate
        ) in zip(
            documents,
            xgb_scores,
            valid_candidates
        ):

            document_name = (
                document.document_name
            )

            xgb_score = float(
                xgb_score
            )

            semantic_score = float(
                candidate.get(
                    "semantic_score",
                    0.0
                )
            )

            graph_score = float(
                candidate.get(
                    "graph_score",
                    0.0
                )
            )

            # ==================================================
            # BUSINESS SCORE
            # ==================================================

            try:

                business_score = float(
                    self.business_ranker.score(
                        document,
                        query,
                        user
                    )
                )

            except Exception as error:

                print(
                    "Business ranker error:",
                    error
                )

                business_score = 0.0

            business_score = max(
                0.0,
                min(
                    1.0,
                    business_score
                )
            )

            # ==================================================
            # INTENT SCORE
            # ==================================================

            if requested_document:

                # Exact document
                intent_score = 1.0

            elif intent != "general":

                # Candidate already passed hard intent filter
                intent_score = 1.0

            else:

                intent_score = 0.0

            # ==================================================
            # FINAL SCORE
            # ==================================================
            #
            # IMPORTANT:
            #
            # Intent is now a HARD FILTER.
            #
            # Therefore these weights only rank documents
            # inside the relevant candidate set.
            #
            # XGB       35%
            # Semantic  10%
            # Graph     10%
            # Business  20%
            # Intent    25%
            #
            # ==================================================

            final_score = (

                0.35 * xgb_score

                + 0.10 * semantic_score

                + 0.10 * graph_score

                + 0.20 * business_score

                + 0.25 * intent_score
            )

            final_score = max(
                0.0,
                min(
                    1.0,
                    final_score
                )
            )

            # ==================================================
            # EXPLANATION
            # ==================================================

            try:

                reason = self.explainer.explain(
                    user,
                    document
                )

            except Exception:

                reason = (
                    "This document is relevant "
                    "to your request."
                )

            reason = self.get_reason(
                document_name,
                reason
            )

            # ==================================================
            # CATEGORY
            # ==================================================

            result_category = (
                self.get_document_category(
                    document_name,
                    intent
                )
            )

            # ==================================================
            # RESULT
            # ==================================================

            results.append(
                {
                    "document":
                        document_name,

                    "category":
                        result_category,

                    "score":
                        final_score,

                    "reason":
                        reason,

                    "xgb_score":
                        xgb_score,

                    "semantic_score":
                        semantic_score,

                    "graph_score":
                        graph_score,

                    "business_score":
                        business_score
                }
            )

            print(
                f"{document_name}: "
                f"XGB={xgb_score:.4f} | "
                f"Semantic={semantic_score:.4f} | "
                f"Graph={graph_score:.4f} | "
                f"Business={business_score:.4f} | "
                f"Intent={intent_score:.4f} | "
                f"Final={final_score:.4f}"
            )

        # ======================================================
        # 10. SORT
        # ======================================================

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # ======================================================
        # 11. TOP 5
        # ======================================================

        results = results[:5]

        # ======================================================
        # 12. FINAL OUTPUT
        # ======================================================

        print(
            "\n========== FINAL RECOMMENDATIONS =========="
        )

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"{index}. "
                f"{result['document']} | "
                f"Score={result['score']:.4f} | "
                f"Category={result['category']}"
            )

        print(
            "===========================================\n"
        )

        return results