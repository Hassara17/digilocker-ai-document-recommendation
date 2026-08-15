class FeatureBuilder:

    def build(
        self,
        user,
        document,
        semantic_score=0.0,
        graph_score=0
    ):
        """
        Build ML features for a user-document pair.

        Returns:
            dict: Feature dictionary used by the ranking/training pipeline.
        """

        # =====================================================
        # NORMALIZE DOCUMENT INFORMATION
        # =====================================================

        category = str(document.category or "").strip().lower()
        name = str(document.document_name or "").strip().lower()

        # Normalize common separators
        category = category.replace("-", " ")
        category = " ".join(category.split())

        name = name.replace("-", " ")
        name = " ".join(name.split())

        # =====================================================
        # USER FEATURES
        # =====================================================

        age = int(getattr(user, "age", 0))

        student = int(bool(getattr(user, "student", False)))
        vehicle_owner = int(bool(getattr(user, "vehicle_owner", False)))
        taxpayer = int(bool(getattr(user, "taxpayer", False)))

        # =====================================================
        # DOCUMENT BASIC FEATURES
        # =====================================================

        searchable = int(bool(getattr(document, "searchable", False)))

        issuer_id = str(getattr(document, "issuer_id", "") or "").strip()

        issuer_present = int(issuer_id != "")

        # =====================================================
        # CATEGORY FEATURES
        # =====================================================

        # Vehicle category
        vehicle_category = int(
            "category 1" in category
            or "category 2" in category
            or "vehicle" in category
        )

        # Financial category
        financial_category = int(
            "category 3" in category
            or "financial" in category
        )

        # Health category
        health_category = int(
            "category 4" in category
            or "health" in category
            or "medical" in category
        )

        # Employment category
        employment_category = int(
            "category 5" in category
            or "employment" in category
        )

        # Class X category
        class10_category = int(
            "class x documents" in category
            or "class 10 documents" in category
            or "class x" in category and "documents" in category
        )

        # Class XII category
        class12_category = int(
            "class xii documents" in category
            or "class 12 documents" in category
            or "class xii" in category and "documents" in category
        )

        # Higher education category
        higher_education_category = int(
            "higher & other education" in category
            or "higher and other education" in category
            or "higher education" in category
        )

        # Identity / eligibility category
        identity_category = int(
            "identity & eligibility" in category
            or "identity and eligibility" in category
            or "identity" in category and "eligibility" in category
        )

        # =====================================================
        # VEHICLE FEATURES
        # =====================================================

        driving_license = int(
            "driving license" in name
            or "driving licence" in name
        )

        vehicle_registration = int(
            "vehicle registration" in name
            or "registration certificate" in name
            or name == "rc"
        )

        # IMPORTANT:
        # Only classify as vehicle insurance if the document
        # explicitly indicates vehicle/motor insurance.
        vehicle_insurance = int(
            "vehicle insurance" in name
            or "motor insurance" in name
            or "motor vehicle insurance" in name
            or "car insurance" in name
            or "bike insurance" in name
            or "two wheeler insurance" in name
        )

        challan_document = int(
            "challan" in name
        )

        vehicle_tax = int(
            "vehicle tax" in name
            or "road tax" in name
        )

        vehicle_fitness = int(
            "vehicle fitness" in name
            or "fitness certificate" in name
        )

        # =====================================================
        # FINANCIAL FEATURES
        # =====================================================

        pan_document = int(
            name == "pan card"
            or name == "pan"
        )

        epan_document = int(
            name == "epan"
            or name == "e pan"
            or name == "e pan card"
        )

        form16_document = int(
            "form 16" in name
            or "form16" in name
        )

        tds_document = int(
            "tds certificate" in name
            or "tds" == name
        )

        passport_document = int(
            "passport" in name
        )

        # =====================================================
        # HEALTH FEATURES
        # =====================================================

        health_card = int(
            "health card" in name
        )

        pmjay_document = int(
            "pradhan mantri jan arogya yojana" in name
            or "pmjay" in name
        )

        health_fitness = int(
            "health fitness" in name
            or "medical fitness" in name
        )

        health_policy = int(
            "policy document health" in name
            or "health policy" in name
            or "health insurance policy" in name
        )

        covid_vaccine = int(
            "covid vaccine" in name
            or "covid vaccination" in name
            or "covid vaccine certificate" in name
        )

        national_health_id = int(
            "national health id" in name
            or "health id" in name
            or "abha" in name
        )

        health_insurance = int(
            "insurance health" in name
            or "health insurance" in name
            or "insurance health" in name
        )

        # =====================================================
        # EMPLOYMENT / SOCIAL FEATURES
        # =====================================================

        uan_card = int(
            "uan card" in name
            or "uan" == name
        )

        epran_card = int(
            "epran card" in name
            or "e pran card" in name
            or "epran" == name
        )

        pension_certificate = int(
            "pension certificate" in name
        )

        ration_card = int(
            "ration card" in name
        )

        # =====================================================
        # CLASS X FEATURES
        # =====================================================

        apaar_document = int(
            "apaar id" in name
            or "apaar" == name
        )

        class10_marksheet = int(
            "class x marksheet" in name
            or "class 10 marksheet" in name
        )

        class10_passing = int(
            "class x passing certificate" in name
            or "class 10 passing certificate" in name
        )

        class10_migration = int(
            "class x migration certificate" in name
            or "class 10 migration certificate" in name
        )

        class10_school_leaving = int(
            "class x school leaving certificate" in name
            or "class 10 school leaving certificate" in name
        )

        # =====================================================
        # CLASS XII FEATURES
        # =====================================================

        class12_marksheet = int(
            "class xii marksheet" in name
            or "class 12 marksheet" in name
        )

        class12_passing = int(
            "class xii passing certificate" in name
            or "class 12 passing certificate" in name
        )

        class12_migration = int(
            "class xii migration certificate" in name
            or "class 12 migration certificate" in name
        )

        # =====================================================
        # HIGHER EDUCATION FEATURES
        # =====================================================

        class1_9_marksheets = int(
            "class i to ix marksheets" in name
            or "class 1 to 9 marksheets" in name
            or "class i-ix marksheets" in name
        )

        degree_document = int(
            "degree certificate" in name
            or name == "degree"
        )

        provisional_degree = int(
            "provisional degree certificate" in name
            or "provisional degree" in name
        )

        diploma_document = int(
            "diploma certificate" in name
            or name == "diploma"
        )

        bonafide_document = int(
            "bonafide certificate" in name
            or "bonafide" == name
        )

        # =====================================================
        # IDENTITY / ELIGIBILITY FEATURES
        # =====================================================

        caste_certificate = int(
            "caste certificate" in name
        )

        income_certificate = int(
            "income certificate" in name
        )

        birth_certificate = int(
            "birth certificate" in name
        )

        ckyc_card = int(
            "ckyc card" in name
            or "ckyc" == name
        )

        # =====================================================
        # FINAL FEATURE DICTIONARY
        # =====================================================

        features = {

            # -------------------------------------------------
            # USER FEATURES
            # -------------------------------------------------

            "age": age,
            "student": student,
            "vehicle_owner": vehicle_owner,
            "taxpayer": taxpayer,

            # -------------------------------------------------
            # BASIC DOCUMENT FEATURES
            # -------------------------------------------------

            "searchable": searchable,
            "issuer_present": issuer_present,

            # -------------------------------------------------
            # RANKING FEATURES
            # -------------------------------------------------

            "semantic_score": float(semantic_score),
            "graph_score": int(graph_score),

            # -------------------------------------------------
            # CATEGORY FEATURES
            # -------------------------------------------------

            "vehicle_category": vehicle_category,
            "financial_category": financial_category,
            "health_category": health_category,
            "employment_category": employment_category,
            "class10_category": class10_category,
            "class12_category": class12_category,
            "higher_education_category": higher_education_category,
            "identity_category": identity_category,

            # -------------------------------------------------
            # VEHICLE FEATURES
            # -------------------------------------------------

            "driving_license": driving_license,
            "vehicle_registration": vehicle_registration,
            "vehicle_insurance": vehicle_insurance,
            "challan_document": challan_document,
            "vehicle_tax": vehicle_tax,
            "vehicle_fitness": vehicle_fitness,

            # -------------------------------------------------
            # FINANCIAL FEATURES
            # -------------------------------------------------

            "pan_document": pan_document,
            "epan_document": epan_document,
            "form16_document": form16_document,
            "tds_document": tds_document,
            "passport_document": passport_document,

            # -------------------------------------------------
            # HEALTH FEATURES
            # -------------------------------------------------

            "health_card": health_card,
            "pmjay_document": pmjay_document,
            "health_fitness": health_fitness,
            "health_policy": health_policy,
            "covid_vaccine": covid_vaccine,
            "national_health_id": national_health_id,
            "health_insurance": health_insurance,

            # -------------------------------------------------
            # EMPLOYMENT / SOCIAL FEATURES
            # -------------------------------------------------

            "uan_card": uan_card,
            "epran_card": epran_card,
            "pension_certificate": pension_certificate,
            "ration_card": ration_card,

            # -------------------------------------------------
            # CLASS X FEATURES
            # -------------------------------------------------

            "apaar_document": apaar_document,
            "class10_marksheet": class10_marksheet,
            "class10_passing": class10_passing,
            "class10_migration": class10_migration,
            "class10_school_leaving": class10_school_leaving,

            # -------------------------------------------------
            # CLASS XII FEATURES
            # -------------------------------------------------

            "class12_marksheet": class12_marksheet,
            "class12_passing": class12_passing,
            "class12_migration": class12_migration,

            # -------------------------------------------------
            # HIGHER EDUCATION FEATURES
            # -------------------------------------------------

            "class1_9_marksheets": class1_9_marksheets,
            "degree_document": degree_document,
            "provisional_degree": provisional_degree,
            "diploma_document": diploma_document,
            "bonafide_document": bonafide_document,

            # -------------------------------------------------
            # IDENTITY FEATURES
            # -------------------------------------------------

            "caste_certificate": caste_certificate,
            "income_certificate": income_certificate,
            "birth_certificate": birth_certificate,
            "ckyc_card": ckyc_card
        }

        return features