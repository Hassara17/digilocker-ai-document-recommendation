import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        print("Loading ChromaDB...")

        self.client = chromadb.PersistentClient(
            path="./database"
        )

        self.collection = self.client.get_or_create_collection(
            name="digilocker_documents"
        )

        print("Loading Model...")

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        print("Model Loaded")

    # ==================================================
    # BUILD RICH DOCUMENT DESCRIPTION
    # ==================================================

    def build_document_text(self, document):

        name = document.document_name.lower()
        category = document.category.lower()
        doctype = document.doctype.lower()

        # ------------------------------------------------
        # VEHICLE / DRIVING
        # ------------------------------------------------

        if any(word in name for word in [
            "vehicle",
            "insurance",
            "challan",
            "driving",
            "fitness",
            "tax receipt"
        ]):

            description = """
            This is a vehicle, driving and transportation
            related government document.

            It may be related to:
            cars, bikes, motorcycles, vehicle ownership,
            driving, driving license, vehicle registration,
            vehicle insurance, road transport, vehicle tax,
            vehicle fitness, traffic violations and challans.
            """

        # ------------------------------------------------
        # EDUCATION
        # ------------------------------------------------

        elif any(word in name for word in [
            "marksheet",
            "degree",
            "diploma",
            "education",
            "apaar",
            "school",
            "certificate"
        ]) and (
            "education" in category
            or "class" in category
            or "education" in name
            or "marksheet" in name
            or "degree" in name
            or "apaar" in name
        ):

            description = """
            This is an education related government document.

            It is related to:
            students, schools, colleges, universities,
            examinations, academic records, marksheets,
            passing certificates, degrees, diplomas,
            educational qualifications and student identity.
            """

        # ------------------------------------------------
        # FINANCIAL / TAX
        # ------------------------------------------------

        elif any(word in name for word in [
            "pan",
            "tds",
            "form 16",
            "tax"
        ]):

            description = """
            This is a financial and taxation related
            government document.

            It is related to:
            income tax, taxpayers, PAN,
            salary, income, TDS, tax filing,
            financial records and employment income.
            """

        # ------------------------------------------------
        # HEALTH
        # ------------------------------------------------

        elif any(word in name for word in [
            "health",
            "medical",
            "vaccine",
            "covid",
            "ayushman",
            "jan arogya"
        ]):

            description = """
            This is a health and medical related
            government document.

            It is related to:
            healthcare, medical services,
            health insurance, vaccination,
            health identity and government
            healthcare schemes.
            """

        # ------------------------------------------------
        # IDENTITY
        # ------------------------------------------------

        elif any(word in name for word in [
            "identity",
            "ration",
            "birth",
            "caste",
            "income",
            "ckyc",
            "passport"
        ]):

            description = """
            This is an identity or eligibility related
            government document.

            It may be related to:
            identity verification, citizenship,
            birth records, caste, income,
            ration benefits, KYC and eligibility.
            """

        # ------------------------------------------------
        # DEFAULT
        # ------------------------------------------------

        else:

            description = """
            This is a government document available
            through DigiLocker.

            It may be used for identity verification,
            eligibility, official records or
            government services.
            """

        # ------------------------------------------------
        # FINAL DOCUMENT TEXT
        # ------------------------------------------------

        text = f"""
        Document: {document.document_name}

        Category: {document.category}

        Document Type: {document.doctype}

        Issuer ID: {document.issuer_id}

        Searchable: {document.searchable}

        Description:
        {description}

        Document concepts:
        {name}
        {category}
        {doctype}
        """

        return text.strip()

    # ==================================================
    # ADD / UPDATE DOCUMENT
    # ==================================================

    def add_document(self, document):

        text = self.build_document_text(
            document
        )

        # BGE passage embedding
        passage_text = f"passage: {text}"

        embedding = self.model.encode(
            passage_text,
            normalize_embeddings=True
        ).tolist()

        self.collection.upsert(
            ids=[document.doctype],

            embeddings=[embedding],

            documents=[
                document.document_name
            ],

            metadatas=[
                {
                    "category": document.category,
                    "doctype": document.doctype,
                    "issuer_id": document.issuer_id,
                    "searchable": document.searchable
                }
            ]
        )

    # ==================================================
    # SEMANTIC SEARCH
    # ==================================================

    def search(
        self,
        query,
        n_results=10
    ):

        # BGE query format
        query_text = (
            f"query: {query}"
        )

        query_embedding = self.model.encode(
            query_text,
            normalize_embeddings=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],

            n_results=n_results,

            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        candidates = []

        if not results.get("documents"):
            return candidates

        documents = results["documents"][0]

        distances = results["distances"][0]

        for document, distance in zip(
            documents,
            distances
        ):

            # Chroma cosine distance
            # with normalized embeddings
            semantic_score = 1.0 - float(
                distance
            )

            # Keep score inside [0, 1]
            semantic_score = max(
                0.0,
                min(
                    1.0,
                    semantic_score
                )
            )

            candidates.append(
                {
                    "document": document,
                    "semantic_score": semantic_score
                }
            )

        return candidates

    # ==================================================
    # SCORE ONE SPECIFIC DOCUMENT
    # ==================================================

    def score_document(
        self,
        query,
        document_name
    ):

        query_embedding = self.model.encode(
            f"query: {query}",
            normalize_embeddings=True
        )

        # ----------------------------------------------
        # Find document by stored document name
        # ----------------------------------------------

        results = self.collection.get(
            where_document={
                "$contains": document_name
            },

            include=[
                "documents",
                "embeddings"
            ]
        )

        embeddings = results.get(
            "embeddings"
        )

        # ----------------------------------------------
        # No embedding found
        # ----------------------------------------------

        if embeddings is None:
            return 0.0

        if len(embeddings) == 0:
            return 0.0

        # ----------------------------------------------
        # Get first matching embedding
        # ----------------------------------------------

        document_embedding = embeddings[0]

        # ----------------------------------------------
        # Cosine similarity
        # ----------------------------------------------

        similarity = (
            query_embedding @ document_embedding
        )

        similarity = float(
            similarity
        )

        # ----------------------------------------------
        # Keep score in [0, 1]
        # ----------------------------------------------

        similarity = max(
            0.0,
            min(
                1.0,
                similarity
            )
        )

        return similarity