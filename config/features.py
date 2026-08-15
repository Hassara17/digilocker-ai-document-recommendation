# config/features.py

FEATURE_COLUMNS = [
    # User features
    "age",
    "student",
    "vehicle_owner",
    "taxpayer",

    # Document features
    "searchable",
    "issuer_present",

    # Ranking features
    "semantic_score",
    "graph_score",

    # Category features
    "vehicle_category",
    "financial_category",
    "health_category",
    "employment_category",
    "class10_category",
    "class12_category",
    "higher_education_category",
    "identity_category",

    # Vehicle documents
    "driving_license",
    "vehicle_registration",
    "vehicle_insurance",
    "challan_document",
    "vehicle_tax",
    "vehicle_fitness",

    # Financial documents
    "pan_document",
    "epan_document",
    "form16_document",
    "tds_document",
    "passport_document",

    # Health documents
    "health_card",
    "pmjay_document",
    "health_fitness",
    "health_policy",
    "covid_vaccine",
    "national_health_id",
    "health_insurance",

    # Employment / social documents
    "uan_card",
    "epran_card",
    "pension_certificate",
    "ration_card",

    # Education documents
    "apaar_document",

    "class10_marksheet",
    "class10_passing",
    "class10_migration",
    "class10_school_leaving",

    "class12_marksheet",
    "class12_passing",
    "class12_migration",

    "class1_9_marksheets",

    "degree_document",
    "provisional_degree",
    "diploma_document",
    "bonafide_document",

    # Identity documents
    "caste_certificate",
    "income_certificate",
    "birth_certificate",
    "ckyc_card",
]