def build_relationships(graph):
    """
    Build the DigiLocker document knowledge graph.

    Relationships are intentionally bidirectional because
    recommendations may need to traverse the graph from
    either the existing document or the newly recommended document.
    """

    # ============================================================
    # VEHICLE DOCUMENTS
    # ============================================================

    graph.add_relation(
        "Driving License",
        "Vehicle Registration"
    )

    graph.add_relation(
        "Vehicle Registration",
        "Vehicle Insurance"
    )

    graph.add_relation(
        "Vehicle Insurance",
        "Challan"
    )

    graph.add_relation(
        "Vehicle Registration",
        "Vehicle Tax Receipt"
    )

    graph.add_relation(
        "Vehicle Registration",
        "Vehicle Fitness Certificate"
    )


    # ============================================================
    # FINANCIAL / TAX DOCUMENTS
    # ============================================================

    graph.add_relation(
        "PAN Card",
        "ePAN"
    )

    graph.add_relation(
        "ePAN",
        "Form 16"
    )

    graph.add_relation(
        "Form 16",
        "TDS Certificate"
    )

    graph.add_relation(
        "PAN Card",
        "Passport"
    )


    # ============================================================
    # SCHOOL EDUCATION
    # ============================================================

    graph.add_relation(
        "Class 1-9 Marksheets",
        "Class X Marksheet"
    )

    graph.add_relation(
        "APAAR ID",
        "Class X Marksheet"
    )

    graph.add_relation(
        "Class X Marksheet",
        "Class X Passing Certificate"
    )

    graph.add_relation(
        "Class X Passing Certificate",
        "Class XII Marksheet"
    )

    graph.add_relation(
        "Class XII Marksheet",
        "Class XII Passing Certificate"
    )


    # ============================================================
    # HIGHER EDUCATION
    # ============================================================

    graph.add_relation(
        "Class XII Passing Certificate",
        "Degree Certificate"
    )

    graph.add_relation(
        "Degree Certificate",
        "Provisional Degree Certificate"
    )

    graph.add_relation(
        "Degree Certificate",
        "Bonafide Certificate"
    )

    # Diploma pathway
    graph.add_relation(
        "Class XII Passing Certificate",
        "Diploma Certificate"
    )

    graph.add_relation(
        "Diploma Certificate",
        "Bonafide Certificate"
    )


    # ============================================================
    # IDENTITY & ELIGIBILITY
    # ============================================================

    graph.add_relation(
        "Birth Certificate",
        "Income Certificate"
    )

    graph.add_relation(
        "Income Certificate",
        "Caste Certificate"
    )

    graph.add_relation(
        "Income Certificate",
        "CKYC Card"
    )

    graph.add_relation(
        "Birth Certificate",
        "CKYC Card"
    )

    graph.add_relation(
        "Ration Card",
        "Income Certificate"
    )

    graph.add_relation(
        "Ration Card",
        "Caste Certificate"
    )


    # ============================================================
    # HEALTH
    # ============================================================

    graph.add_relation(
        "Health Card/ Certificate",
        "Pradhan Mantri Jan Arogya Yojana"
    )

    graph.add_relation(
        "Pradhan Mantri Jan Arogya Yojana",
        "Insurance - Health"
    )

    graph.add_relation(
        "Insurance - Health",
        "National Health ID Card"
    )

    graph.add_relation(
        "Covid Vaccine Certificate",
        "National Health ID Card"
    )

    graph.add_relation(
        "National Health ID Card",
        "Health Card/ Certificate"
    )


    # ============================================================
    # EMPLOYMENT / RETIREMENT
    # ============================================================

    graph.add_relation(
        "UAN Card",
        "ePRAN Card"
    )

    graph.add_relation(
        "ePRAN Card",
        "Pension Certificate"
    )


    # ============================================================
    # CROSS-CATEGORY RELATIONSHIPS
    # ============================================================

    # Higher education → employment
    graph.add_relation(
        "Degree Certificate",
        "UAN Card"
    )

    graph.add_relation(
        "Diploma Certificate",
        "UAN Card"
    )

    # Identity → financial
    graph.add_relation(
        "CKYC Card",
        "PAN Card"
    )

    # Identity → health
    graph.add_relation(
        "Birth Certificate",
        "National Health ID Card"
    )

    # Government eligibility → health
    graph.add_relation(
        "Ration Card",
        "Pradhan Mantri Jan Arogya Yojana"
    )