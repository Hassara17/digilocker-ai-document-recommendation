import requests


API_URL = "http://127.0.0.1:8000/recommend"


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [

    # --------------------------------------------------------
    # VEHICLE
    # --------------------------------------------------------

    {
        "name": "Bike Purchase",
        "query": "I bought a bike",
        "user": {
            "age": 22,
            "occupation": "Student",
            "state": "Delhi",
            "vehicle_owner": True,
            "taxpayer": False,
            "student": True,
            "existing_documents": []
        },
        "expected": [
            "Vehicle Registration",
            "Vehicle Insurance",
            "Driving License",
            "Challan"
        ]
    },

    {
        "name": "Vehicle Registration",
        "query": "I need to register my new car",
        "user": {
            "age": 30,
            "occupation": "Employee",
            "state": "Delhi",
            "vehicle_owner": True,
            "taxpayer": False,
            "student": False,
            "existing_documents": []
        },
        "expected": [
            "Vehicle Registration"
        ]
    },

    {
        "name": "Vehicle Insurance",
        "query": "I need insurance for my bike",
        "user": {
            "age": 30,
            "occupation": "Employee",
            "state": "Delhi",
            "vehicle_owner": True,
            "taxpayer": False,
            "student": False,
            "existing_documents": []
        },
        "expected": [
            "Vehicle Insurance"
        ]
    },

    {
        "name": "Driving License",
        "query": "I need a driving license",
        "user": {
            "age": 22,
            "occupation": "Student",
            "state": "Delhi",
            "vehicle_owner": True,
            "taxpayer": False,
            "student": True,
            "existing_documents": []
        },
        "expected": [
            "Driving License"
        ]
    },

    {
        "name": "Challan",
        "query": "I want to check my challan",
        "user": {
            "age": 30,
            "occupation": "Employee",
            "state": "Delhi",
            "vehicle_owner": True,
            "taxpayer": False,
            "student": False,
            "existing_documents": []
        },
        "expected": [
            "Challan"
        ]
    },


    # --------------------------------------------------------
    # TAX
    # --------------------------------------------------------

    {
        "name": "Income Tax",
        "query": "I want to file my income tax",
        "user": {
            "age": 30,
            "occupation": "Employee",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": True,
            "student": False,
            "existing_documents": [
                "Aadhaar Card",
                "PAN Card"
            ]
        },
        "expected": [
            "Form 16",
            "TDS Certificate",
            "ePAN"
        ]
    },

    {
        "name": "TDS",
        "query": "I need my TDS certificate",
        "user": {
            "age": 30,
            "occupation": "Employee",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": True,
            "student": False,
            "existing_documents": []
        },
        "expected": [
            "TDS Certificate"
        ]
    },

    {
        "name": "PAN for Tax",
        "query": "I need my PAN for tax filing",
        "user": {
            "age": 30,
            "occupation": "Employee",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": True,
            "student": False,
            "existing_documents": []
        },
        "expected": [
            "PAN Card",
            "ePAN"
        ]
    },


    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    {
        "name": "10th Marksheet",
        "query": "I need my 10th marksheet",
        "user": {
            "age": 22,
            "occupation": "Student",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": False,
            "student": True,
            "existing_documents": [
                "Aadhaar Card",
                "PAN Card"
            ]
        },
        "expected": [
            "Class X Marksheet"
        ]
    },

    {
        "name": "12th Marksheet",
        "query": "I need my 12th marksheet",
        "user": {
            "age": 22,
            "occupation": "Student",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": False,
            "student": True,
            "existing_documents": []
        },
        "expected": [
            "Class XII Marksheet"
        ]
    },

    {
        "name": "Degree Certificate",
        "query": "I need my degree certificate",
        "user": {
            "age": 24,
            "occupation": "Student",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": False,
            "student": True,
            "existing_documents": []
        },
        "expected": [
            "Degree Certificate"
        ]
    },

    {
        "name": "APAAR",
        "query": "I need my APAAR ID",
        "user": {
            "age": 22,
            "occupation": "Student",
            "state": "Delhi",
            "vehicle_owner": False,
            "taxpayer": False,
            "student": True,
            "existing_documents": []
        },
        "expected": [
            "APAAR ID"
        ]
    }
]


# ============================================================
# METRICS
# ============================================================

def calculate_mrr(results):

    reciprocal_ranks = []

    for result in results:

        recommendations = result["recommendations"]
        expected = result["expected"]

        rank = None

        for index, item in enumerate(
            recommendations,
            start=1
        ):

            if item["document"] in expected:

                rank = index
                break

        if rank is None:

            reciprocal_ranks.append(0)

        else:

            reciprocal_ranks.append(
                1 / rank
            )

    if not reciprocal_ranks:
        return 0

    return sum(reciprocal_ranks) / len(
        reciprocal_ranks
    )


# ============================================================
# RUN TESTS
# ============================================================

def run_tests():

    print("\n")
    print("=" * 70)
    print("       DIGILOCKER RECOMMENDATION EVALUATION")
    print("=" * 70)

    results = []

    top1_correct = 0
    top3_correct = 0
    top5_correct = 0

    existing_document_failures = 0

    for test in TEST_CASES:

        print("\n")
        print("-" * 70)
        print("TEST:", test["name"])
        print("QUERY:", test["query"])
        print("EXPECTED:", test["expected"])

        payload = {
            **test["user"],
            "query": test["query"]
        }

        try:

            response = requests.post(
                API_URL,
                json=payload,
                timeout=30
            )

        except Exception as error:

            print("❌ API ERROR")
            print(error)

            continue

        if response.status_code != 200:

            print(
                "❌ HTTP ERROR:",
                response.status_code
            )

            print(
                response.text
            )

            continue

        data = response.json()

        recommendations = data.get(
            "recommendations",
            []
        )

        recommendation_names = [
            item["document"]
            for item in recommendations
        ]

        print(
            "\nACTUAL:",
            recommendation_names
        )

        # ====================================================
        # TOP 1
        # ====================================================

        top1_pass = (
            len(recommendation_names) > 0
            and recommendation_names[0]
            in test["expected"]
        )

        if top1_pass:

            top1_correct += 1

            print(
                "TOP-1: ✅ PASS"
            )

        else:

            print(
                "TOP-1: ❌ FAIL"
            )

        # ====================================================
        # TOP 3
        # ====================================================

        top3 = recommendation_names[:3]

        top3_pass = any(
            item in test["expected"]
            for item in top3
        )

        if top3_pass:

            top3_correct += 1

            print(
                "TOP-3: ✅ PASS"
            )

        else:

            print(
                "TOP-3: ❌ FAIL"
            )

        # ====================================================
        # TOP 5
        # ====================================================

        top5 = recommendation_names[:5]

        top5_pass = any(
            item in test["expected"]
            for item in top5
        )

        if top5_pass:

            top5_correct += 1

            print(
                "TOP-5: ✅ PASS"
            )

        else:

            print(
                "TOP-5: ❌ FAIL"
            )

        # ====================================================
        # EXISTING DOCUMENT CHECK
        # ====================================================

        existing_documents = test[
            "user"
        ].get(
            "existing_documents",
            []
        )

        invalid_existing = [
            document
            for document in recommendation_names
            if document in existing_documents
        ]

        if invalid_existing:

            existing_document_failures += 1

            print(
                "EXISTING DOCUMENT CHECK: ❌ FAIL"
            )

            print(
                "Invalid recommendations:",
                invalid_existing
            )

        else:

            print(
                "EXISTING DOCUMENT CHECK: ✅ PASS"
            )

        # ====================================================
        # SAVE RESULT
        # ====================================================

        results.append(
            {
                "name": test["name"],
                "expected": test["expected"],
                "recommendations": recommendations
            }
        )

    # ========================================================
    # METRICS
    # ========================================================

    total_tests = len(results)

    if total_tests == 0:

        print(
            "\nNo tests were successfully executed."
        )

        return

    top1_accuracy = (
        top1_correct / total_tests
    )

    top3_accuracy = (
        top3_correct / total_tests
    )

    top5_accuracy = (
        top5_correct / total_tests
    )

    mrr = calculate_mrr(
        results
    )

    existing_document_accuracy = (
        (
            total_tests
            - existing_document_failures
        )
        / total_tests
    )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                 FINAL EVALUATION")
    print("=" * 70)

    print(
        f"\nTotal Tests: {total_tests}"
    )

    print(
        f"Top-1 Accuracy: "
        f"{top1_accuracy * 100:.2f}%"
    )

    print(
        f"Top-3 Accuracy: "
        f"{top3_accuracy * 100:.2f}%"
    )

    print(
        f"Top-5 Accuracy: "
        f"{top5_accuracy * 100:.2f}%"
    )

    print(
        f"MRR: "
        f"{mrr:.4f}"
    )

    print(
        f"Existing Document Safety: "
        f"{existing_document_accuracy * 100:.2f}%"
    )

    print("\n")

    print("=" * 70)
    print("Evaluation completed.")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_tests()