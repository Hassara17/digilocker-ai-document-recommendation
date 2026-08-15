import json

from models.document import Document


class KnowledgeBase:

    def __init__(
        self,
        path
    ):

        self.documents = []

        self.load(
            path
        )

    # =====================================================
    # LOAD KNOWLEDGE BASE
    # =====================================================

    def load(
        self,
        path
    ):

        print(
            f"\nLoading Knowledge Base: {path}"
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(
                f
            )

        # =================================================
        # VALIDATE ROOT
        # =================================================

        if not isinstance(
            data,
            list
        ):

            raise ValueError(
                "\nKnowledge Base JSON "
                "must contain a list of categories."
            )

        # =================================================
        # LOAD DOCUMENTS
        # =================================================

        for category in data:

            if "category" not in category:

                raise ValueError(
                    "\nKnowledge Base category "
                    "is missing 'category'."
                )

            if "documents" not in category:

                raise ValueError(
                    f"\nCategory "
                    f"'{category['category']}' "
                    f"is missing 'documents'."
                )

            category_name = (
                category["category"]
            )

            for doc in category[
                "documents"
            ]:

                required_fields = [

                    "document_name",
                    "doctype",
                    "issuer_id",
                    "searchable"

                ]

                for field in required_fields:

                    if field not in doc:

                        raise ValueError(
                            f"\nDocument in category "
                            f"'{category_name}' "
                            f"is missing field "
                            f"'{field}'."
                        )

                document = Document(

                    document_name=doc[
                        "document_name"
                    ],

                    doctype=doc[
                        "doctype"
                    ],

                    issuer_id=doc[
                        "issuer_id"
                    ],

                    searchable=doc[
                        "searchable"
                    ],

                    category=category_name

                )

                self.documents.append(
                    document
                )

        print(
            f"Loaded {len(self.documents)} "
            f"documents."
        )

    # =====================================================
    # GET ALL DOCUMENTS
    # =====================================================

    def get_all_documents(
        self
    ):

        return self.documents

    # =====================================================
    # GET SINGLE DOCUMENT
    # =====================================================

    def get_document(
        self,
        document_name
    ):

        for document in self.documents:

            if (
                document.document_name
                == document_name
            ):

                return document

        return None