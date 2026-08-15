class DocumentGraph:

    def __init__(self):
        self.graph = {}

    def add_document(self, document):

        name = document.document_name

        if name not in self.graph:
            self.graph[name] = set()

    def add_relation(self, doc1, doc2):

        if doc1 not in self.graph:
            self.graph[doc1] = set()

        if doc2 not in self.graph:
            self.graph[doc2] = set()

        # Bidirectional relationship
        self.graph[doc1].add(doc2)
        self.graph[doc2].add(doc1)

    def build_from_knowledge_base(self, documents):

        # First create all document nodes
        for document in documents:
            self.add_document(document)

        # Group documents by category
        categories = {}

        for document in documents:

            category = document.category
            doc_name = document.document_name

            if category not in categories:
                categories[category] = []

            categories[category].append(doc_name)

        # Connect documents belonging to
        # the same category
        for category, docs in categories.items():

            for i in range(len(docs)):

                for j in range(i + 1, len(docs)):

                    self.add_relation(
                        docs[i],
                        docs[j]
                    )

    def has_document(self, document):

        return document in self.graph

    def next_documents(self, document):

        if document not in self.graph:
            return []

        return list(
            self.graph[document]
        )

    def print_graph(self):

        print(
            "\n========== GRAPH RELATIONSHIPS =========="
        )

        for document, related in self.graph.items():

            print(
                f"{document} -> {list(related)}"
            )

        print(
            "=========================================\n"
        )