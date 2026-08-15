import os
import random
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_PATH = "data/training_data.csv"
NUM_ROWS = 5000

random.seed(42)


# ============================================================
# DOCUMENT DEFINITIONS
# ============================================================

DOCUMENTS = {

    # ---------------- VEHICLE ----------------

    "Driving License": "vehicle",
    "Vehicle Registration": "vehicle",
    "Vehicle Insurance": "vehicle",
    "Challan": "vehicle",
    "Vehicle Tax Receipt": "vehicle",
    "Vehicle Fitness Certificate": "vehicle",

    # ---------------- FINANCIAL ----------------

    "PAN Card": "financial",
    "ePAN": "financial",
    "Form 16": "financial",
    "TDS Certificate": "financial",
    "Passport": "financial",

    # ---------------- HEALTH ----------------

    "Health Card/ Certificate": "health",
    "Pradhan Mantri Jan Arogya Yojana": "health",
    "Health Fitness Certificate": "health",
    "Policy Document-Health": "health",
    "Covid Vaccine Certificate": "health",
    "National Health ID Card": "health",
    "Insurance - Health": "health",

    # ---------------- EMPLOYMENT ----------------

    "UAN Card": "employment",
    "ePRAN Card": "employment",
    "Pension Certificate": "employment",
    "Ration Card": "employment",

    # ---------------- CLASS X ----------------

    "APAAR ID": "class10",
    "Class X Marksheet": "class10",
    "Class X Passing Certificate": "class10",
    "Class X Migration Certificate": "class10",
    "Class X School Leaving Certificate": "class10",

    # ---------------- CLASS XII ----------------

    "Class XII Marksheet": "class12",
    "Class XII Passing Certificate": "class12",
    "Class XII Migration Certificate": "class12",

    # ---------------- HIGHER EDUCATION ----------------

    "Class 1-9 Marksheets": "higher_education",
    "Degree Certificate": "higher_education",
    "Provisional Degree Certificate": "higher_education",
    "Diploma Certificate": "higher_education",
    "Bonafide Certificate": "higher_education",

    # ---------------- IDENTITY ----------------

    "Caste Certificate": "identity",
    "Income Certificate": "identity",
    "Birth Certificate": "identity",
    "CKYC Card": "identity",
}


# ============================================================
# QUERY TEMPLATES
# ============================================================

QUERY_TEMPLATES = {

    "vehicle": [

        "I bought a bike",
        "I bought a car",
        "I purchased a motorcycle",
        "I purchased a scooter",
        "I purchased a new vehicle",
        "I bought a new vehicle",
        "I need documents for my bike",
        "I need vehicle documents",
        "I need documents after buying a car",
        "I want to register my vehicle",
        "I need vehicle registration",
        "I need bike insurance",
        "I need car insurance",
        "I need driving documents",
        "I need information about my vehicle",
        "I recently purchased a motorcycle",
        "I recently bought a vehicle",
        "I want to register my bike",
        "I need my vehicle tax document",
        "I need vehicle fitness certificate",
        "I want to check my challan",
    ],

    "financial": [

        "I want to file my income tax",
        "I need my PAN",
        "I need PAN related documents",
        "I want to file ITR",
        "I need Form 16",
        "I need my TDS certificate",
        "I need tax documents",
        "I want income tax documents",
        "I need documents for tax filing",
    ],

    "health": [

        "I need health documents",
        "I need health insurance",
        "I need my health card",
        "I need medical documents",
        "I need health certificate",
        "I need vaccination certificate",
        "I need PMJAY document",
        "I need National Health ID",
    ],

    "employment": [

        "I need employment documents",
        "I need my UAN",
        "I need pension documents",
        "I need employment records",
        "I need ePRAN",
        "I need ration card",
    ],

    "class10": [

        "I need my 10th marksheet",
        "I need class 10 documents",
        "I need my school certificate",
        "I need class X marksheet",
        "I need my 10th passing certificate",
    ],

    "class12": [

        "I need my 12th marksheet",
        "I need class 12 documents",
        "I need class XII marksheet",
        "I need my 12th passing certificate",
    ],

    "higher_education": [

        "I need my degree certificate",
        "I need higher education documents",
        "I need my provisional degree",
        "I need my diploma certificate",
        "I need bonafide certificate",
        "I need university documents",
    ],

    "identity": [

        "I need my birth certificate",
        "I need income certificate",
        "I need caste certificate",
        "I need CKYC",
        "I need identity documents",
    ],
}


# ============================================================
# QUERY → DOCUMENT RELEVANCE
# ============================================================

def query_document_relevance(
    query,
    document,
    category
):
    """
    Returns a relevance score in [0, 1].

    1.0 = highly relevant
    0.7 = relevant
    0.3 = weakly related
    0.0 = unrelated
    """

    query = query.lower()

    # ========================================================
    # VEHICLE INTENT
    # ========================================================

    if category == "vehicle":

        if document == "Vehicle Registration":

            if any(
                word in query
                for word in [
                    "bought",
                    "buy",
                    "purchased",
                    "purchase",
                    "register",
                    "registration",
                    "bike",
                    "car",
                    "vehicle",
                    "motorcycle",
                    "scooter"
                ]
            ):

                return 1.0

        if document == "Vehicle Insurance":

            if any(
                word in query
                for word in [
                    "insurance",
                    "bike",
                    "car",
                    "vehicle",
                    "motorcycle",
                    "scooter",
                    "bought",
                    "purchased"
                ]
            ):

                return 0.95

        if document == "Vehicle Tax Receipt":

            if any(
                word in query
                for word in [
                    "tax",
                    "vehicle",
                    "bike",
                    "car",
                    "registration"
                ]
            ):

                return 0.85

        if document == "Vehicle Fitness Certificate":

            if any(
                word in query
                for word in [
                    "fitness",
                    "vehicle",
                    "bike",
                    "car"
                ]
            ):

                return 0.85

        if document == "Driving License":

            if any(
                word in query
                for word in [
                    "drive",
                    "driving",
                    "license",
                    "licence"
                ]
            ):

                return 1.0

            if any(
                word in query
                for word in [
                    "bike",
                    "car",
                    "vehicle",
                    "motorcycle",
                    "scooter"
                ]
            ):

                return 0.70

        if document == "Challan":

            if "challan" in query:

                return 1.0

            if any(
                word in query
                for word in [
                    "vehicle",
                    "bike",
                    "car"
                ]
            ):

                return 0.55

        return 0.20


    # ========================================================
    # FINANCIAL INTENT
    # ========================================================

    if category == "financial":

        if any(
            word in query
            for word in [
                "tax",
                "income",
                "itr",
                "pan",
                "tds",
                "form 16"
            ]
        ):

            if document == "PAN Card":
                return 1.0

            if document == "ePAN":
                return 0.95

            if document == "Form 16":
                return 0.95

            if document == "TDS Certificate":
                return 0.90

            return 0.40

        return 0.05


    # ========================================================
    # HEALTH INTENT
    # ========================================================

    if category == "health":

        if any(
            word in query
            for word in [
                "health",
                "medical",
                "insurance",
                "vaccine",
                "vaccination",
                "pmjay"
            ]
        ):

            return 0.90

        return 0.05


    # ========================================================
    # EMPLOYMENT INTENT
    # ========================================================

    if category == "employment":

        if any(
            word in query
            for word in [
                "employment",
                "job",
                "uan",
                "pension",
                "pran",
                "ration"
            ]
        ):

            return 0.90

        return 0.05


    # ========================================================
    # EDUCATION INTENT
    # ========================================================

    if category in [
        "class10",
        "class12",
        "higher_education"
    ]:

        if any(
            word in query
            for word in [
                "education",
                "school",
                "marksheet",
                "10th",
                "12th",
                "class",
                "degree",
                "diploma",
                "university",
                "college",
                "academic"
            ]
        ):

            return 0.90

        return 0.05


    # ========================================================
    # IDENTITY INTENT
    # ========================================================

    if category == "identity":

        if any(
            word in query
            for word in [
                "identity",
                "birth",
                "caste",
                "income",
                "ckyc"
            ]
        ):

            return 0.90

        return 0.05


    return 0.0


# ============================================================
# GENERATE USER PROFILE
# ============================================================

def generate_user():

    age = random.randint(
        18,
        60
    )

    student = int(
        age <= 25
        and random.random() < 0.65
    )

    vehicle_owner = int(
        random.random() < 0.45
    )

    taxpayer = int(
        age >= 22
        and random.random() < 0.65
    )

    occupation = random.choice(
        [
            "Student",
            "Employee",
            "Business Owner",
            "Government Employee",
            "Self Employed",
            "Other"
        ]
    )

    if student:
        occupation = "Student"

    return {
        "age": age,
        "student": student,
        "vehicle_owner": vehicle_owner,
        "taxpayer": taxpayer,
        "occupation": occupation
    }


# ============================================================
# CATEGORY FEATURES
# ============================================================

def category_features(category):

    return {

        "vehicle_category":
            int(category == "vehicle"),

        "financial_category":
            int(category == "financial"),

        "health_category":
            int(category == "health"),

        "employment_category":
            int(category == "employment"),

        "class10_category":
            int(category == "class10"),

        "class12_category":
            int(category == "class12"),

        "higher_education_category":
            int(category == "higher_education"),

        "identity_category":
            int(category == "identity"),
    }


# ============================================================
# DOCUMENT FEATURES
# ============================================================

DOCUMENT_FEATURES = {

    "Driving License": "driving_license",
    "Vehicle Registration": "vehicle_registration",
    "Vehicle Insurance": "vehicle_insurance",
    "Challan": "challan_document",
    "Vehicle Tax Receipt": "vehicle_tax",
    "Vehicle Fitness Certificate": "vehicle_fitness",

    "PAN Card": "pan_document",
    "ePAN": "epan_document",
    "Form 16": "form16_document",
    "TDS Certificate": "tds_document",
    "Passport": "passport_document",

    "Health Card/ Certificate": "health_card",
    "Pradhan Mantri Jan Arogya Yojana": "pmjay_document",
    "Health Fitness Certificate": "health_fitness",
    "Policy Document-Health": "health_policy",
    "Covid Vaccine Certificate": "covid_vaccine",
    "National Health ID Card": "national_health_id",
    "Insurance - Health": "health_insurance",

    "UAN Card": "uan_card",
    "ePRAN Card": "epran_card",
    "Pension Certificate": "pension_certificate",
    "Ration Card": "ration_card",

    "APAAR ID": "apaar_document",
    "Class X Marksheet": "class10_marksheet",
    "Class X Passing Certificate": "class10_passing",
    "Class X Migration Certificate": "class10_migration",
    "Class X School Leaving Certificate":
        "class10_school_leaving",

    "Class XII Marksheet":
        "class12_marksheet",

    "Class XII Passing Certificate":
        "class12_passing",

    "Class XII Migration Certificate":
        "class12_migration",

    "Class 1-9 Marksheets":
        "class1_9_marksheets",

    "Degree Certificate":
        "degree_document",

    "Provisional Degree Certificate":
        "provisional_degree",

    "Diploma Certificate":
        "diploma_document",

    "Bonafide Certificate":
        "bonafide_document",

    "Caste Certificate":
        "caste_certificate",

    "Income Certificate":
        "income_certificate",

    "Birth Certificate":
        "birth_certificate",

    "CKYC Card":
        "ckyc_card",
}


# ============================================================
# GENERATE ONE ROW
# ============================================================

def generate_row():

    user = generate_user()

    # Pick an intent
    intent = random.choice(
        list(QUERY_TEMPLATES.keys())
    )

    query = random.choice(
        QUERY_TEMPLATES[intent]
    )

    # Pick document
    document, category = random.choice(
        list(DOCUMENTS.items())
    )

    # ========================================================
    # QUERY / DOCUMENT RELEVANCE
    # ========================================================

    relevance = query_document_relevance(
        query,
        document,
        category
    )

    # ========================================================
    # SEMANTIC SCORE
    # ========================================================

    if relevance >= 0.9:

        semantic_score = random.uniform(
            0.75,
            0.98
        )

    elif relevance >= 0.7:

        semantic_score = random.uniform(
            0.60,
            0.85
        )

    elif relevance >= 0.3:

        semantic_score = random.uniform(
            0.35,
            0.60
        )

    else:

        semantic_score = random.uniform(
            0.05,
            0.35
        )

    # ========================================================
    # GRAPH SCORE
    #
    # Graph relevance is now weaker than query relevance.
    # This prevents graph_score=1 from dominating.
    # ========================================================

    graph_score = 0

    if category == "vehicle" and user["vehicle_owner"]:

        graph_score = random.choice(
            [0, 0.25, 0.5, 0.75, 1]
        )

    elif category == "financial" and user["taxpayer"]:

        graph_score = random.choice(
            [0, 0.25, 0.5]
        )

    elif category in [
        "class10",
        "class12",
        "higher_education"
    ] and user["student"]:

        graph_score = random.choice(
            [0, 0.25, 0.5]
        )

    else:

        graph_score = 0

    # ========================================================
    # BUSINESS / INTENT EFFECT
    # ========================================================

    # Positive examples must strongly correspond
    # to query intent.

    intent_match = int(
        category == intent
    )

    # ========================================================
    # LABEL
    # ========================================================

    # Strongly relevant document
    if relevance >= 0.9:

        label = 1

    # Relevant document
    elif relevance >= 0.7:

        label = 1 if random.random() < 0.85 else 0

    # Weak relevance
    elif relevance >= 0.3:

        label = 1 if random.random() < 0.15 else 0

    # Unrelated
    else:

        label = 0

    # ========================================================
    # IMPORTANT PROFILE OVERRIDE
    # ========================================================

    # Vehicle documents should be positive when
    # user owns a vehicle AND query is vehicle-related.

    if (
        intent == "vehicle"
        and user["vehicle_owner"]
        and category == "vehicle"
        and relevance >= 0.7
    ):

        label = 1

    # Financial documents should NOT become positive
    # simply because taxpayer=True.

    if (
        intent == "vehicle"
        and category == "financial"
    ):

        label = 0

    # Similarly, unrelated categories remain negative.

    if (
        intent == "vehicle"
        and category not in [
            "vehicle"
        ]
    ):

        label = 0

    # ========================================================
    # BASIC DOCUMENT FEATURES
    # ========================================================

    searchable = 1

    issuer_present = random.choice(
        [0, 1]
    )

    # ========================================================
    # BUILD ROW
    # ========================================================

    row = {

        "age":
            user["age"],

        "student":
            user["student"],

        "vehicle_owner":
            user["vehicle_owner"],

        "taxpayer":
            user["taxpayer"],

        "searchable":
            searchable,

        "issuer_present":
            issuer_present,

        "semantic_score":
            round(
                semantic_score,
                6
            ),

        "graph_score":
            graph_score,
    }

    # ========================================================
    # CATEGORY FEATURES
    # ========================================================

    row.update(
        category_features(
            category
        )
    )

    # ========================================================
    # ALL DOCUMENT FLAGS
    # ========================================================

    for feature_name in DOCUMENT_FEATURES.values():

        row[feature_name] = 0

    # Candidate document is represented
    # by its corresponding feature.

    document_feature = DOCUMENT_FEATURES.get(
        document
    )

    if document_feature:

        row[
            document_feature
        ] = 1

    # ========================================================
    # LABEL
    # ========================================================

    row["label"] = label

    return row


# ============================================================
# GENERATE DATASET
# ============================================================

def generate_dataset():

    print(
        "\n========================================"
    )

    print(
        "CREATING TRAINING DATASET"
    )

    print(
        "========================================"
    )

    rows = []

    for i in range(
        NUM_ROWS
    ):

        rows.append(
            generate_row()
        )

        if (
            (i + 1) % 500
            == 0
        ):

            print(
                f"Generated "
                f"{i + 1}/{NUM_ROWS} rows..."
            )

    df = pd.DataFrame(
        rows
    )

    # ========================================================
    # SAVE
    # ========================================================

    os.makedirs(
        "data",
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "DATASET VALIDATION"
    )

    print(
        "========================================"
    )

    print(
        "\nDataset shape:"
    )

    print(
        df.shape
    )

    print(
        "\nLabel distribution:"
    )

    print(
        df["label"].value_counts()
    )

    print(
        "\nLabel percentages:"
    )

    print(
        (
            df["label"]
            .value_counts(
                normalize=True
            )
            * 100
        ).round(2)
    )

    print(
        "\nSaved to:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        "\n========================================"
    )

    print(
        "DATASET CREATED SUCCESSFULLY"
    )

    print(
        "========================================"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generate_dataset()