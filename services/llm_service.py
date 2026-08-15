import requests
import json


class LLMService:

    def __init__(
        self,
        model="llama3.2:3b",
        base_url="http://localhost:11434"
    ):

        self.model = model
        self.base_url = base_url

    # ============================================================
    # GENERATE
    # ============================================================

    def generate(self, prompt):

        try:

            response = requests.post(
                f"{self.base_url}/api/generate",

                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },

                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                ""
            ).strip()

        except Exception as e:

            print(
                f"LLM Error: {e}"
            )

            return ""

    # ============================================================
    # QUERY UNDERSTANDING
    # ============================================================

    def analyze_query(self, query):

        prompt = f"""
You are a DigiLocker document assistant.

Analyze the user's query.

User query:
"{query}"

Return ONLY valid JSON in this format:

{{
    "intent": "",
    "normalized_query": "",
    "keywords": []
}}

Rules:

1. intent should be short.
2. normalized_query should describe what documents the user is looking for.
3. keywords should contain important document-related terms.
4. Do not recommend documents.
5. Do not invent government services.
6. Return JSON only.
"""

        response = self.generate(
            prompt
        )

        try:

            return json.loads(
                response
            )

        except Exception:

            return {
                "intent": "document_search",
                "normalized_query": query,
                "keywords": []
            }

    # ============================================================
    # GENERATE EXPLANATION
    # ============================================================

    def explain_recommendations(
        self,
        query,
        recommendations
    ):

        recommendation_text = []

        for item in recommendations:

            recommendation_text.append(
                {
                    "document":
                        item["document"],

                    "category":
                        item["category"],

                    "score":
                        item["score"],

                    "reason":
                        item["reason"]
                }
            )

        prompt = f"""
You are a DigiLocker recommendation assistant.

User query:
"{query}"

The recommendation engine produced these results:

{json.dumps(
    recommendation_text,
    indent=2
)}

Write a short explanation for the user.

Rules:

1. Only use information present in the recommendations.
2. Do not invent eligibility requirements.
3. Do not change the ranking.
4. Do not add documents.
5. Explain why the top recommendations are relevant.
6. Keep the response concise.
7. Do not mention XGBoost, ChromaDB, embeddings,
   graph algorithms or internal implementation.

Return only the explanation text.
"""

        return self.generate(
            prompt
        )