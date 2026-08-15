from engine.xgb_ranker import XGBoostRanker


def main():

    print("\n========================================")
    print("XGBOOST RANKER TEST")
    print("========================================")

    # ==========================================
    # LOAD RANKER
    # ==========================================

    ranker = XGBoostRanker()

    # ==========================================
    # CREATE SAMPLE FEATURES
    # ==========================================

    feature_list = [

        {
            "age": 22,
            "student": 1,
            "vehicle_owner": 1,
            "taxpayer": 1,

            "searchable": 1,
            "issuer_present": 0,

            "semantic_score": 0.75,
            "graph_score": 1,

            "vehicle_category": 1,
            "financial_category": 0,
            "health_category": 0,
            "employment_category": 0,
            "class10_category": 0,
            "class12_category": 0,
            "higher_education_category": 0,
            "identity_category": 0,

            "driving_license": 0,
            "vehicle_registration": 1,
            "vehicle_insurance": 1,
            "challan_document": 0,
            "vehicle_tax": 1,
            "vehicle_fitness": 1,

            "pan_document": 0,
            "epan_document": 0,
            "form16_document": 0,
            "tds_document": 0,
            "passport_document": 0,

            "health_card": 0,
            "pmjay_document": 0,
            "health_fitness": 0,
            "health_policy": 0,
            "covid_vaccine": 0,
            "national_health_id": 0,
            "health_insurance": 0,

            "uan_card": 0,
            "epran_card": 0,
            "pension_certificate": 0,
            "ration_card": 0,

            "apaar_document": 0,
            "class10_marksheet": 0,
            "class10_passing": 0,
            "class10_migration": 0,
            "class10_school_leaving": 0,

            "class12_marksheet": 0,
            "class12_passing": 0,
            "class12_migration": 0,

            "class1_9_marksheets": 0,
            "degree_document": 0,
            "provisional_degree": 0,
            "diploma_document": 0,
            "bonafide_document": 0,

            "caste_certificate": 0,
            "income_certificate": 0,
            "birth_certificate": 0,
            "ckyc_card": 0
        }
    ]

    # ==========================================
    # SCORE
    # ==========================================

    scores = ranker.score(
        feature_list
    )

    # ==========================================
    # RESULT
    # ==========================================

    print("\n========================================")
    print("RANKER RESULT")
    print("========================================")

    print(
        "Score:",
        scores[0]
    )

    print(
        "Score type:",
        type(scores[0])
    )

    print("========================================")


if __name__ == "__main__":

    main()