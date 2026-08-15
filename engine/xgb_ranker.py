import os

import joblib
import pandas as pd


class XGBoostRanker:

    def __init__(
        self,
        model_path="trained_models/xgb_model.pkl",
        feature_order_path="trained_models/xgb_features.pkl"
    ):

        print(
            "\nLoading XGBoost model..."
        )

        # ==========================================
        # CHECK MODEL
        # ==========================================

        if not os.path.exists(
            model_path
        ):

            raise FileNotFoundError(
                f"\nXGBoost model not found:\n"
                f"{model_path}\n\n"
                f"Train the model first using "
                f"xgb_trainer.py."
            )

        # ==========================================
        # LOAD MODEL
        # ==========================================

        self.model = joblib.load(
            model_path
        )

        print(
            "XGBoost model loaded."
        )

        # ==========================================
        # LOAD FEATURE ORDER
        # ==========================================

        if not os.path.exists(
            feature_order_path
        ):

            raise FileNotFoundError(
                f"\nFeature order file not found:\n"
                f"{feature_order_path}\n\n"
                f"Retrain the XGBoost model "
                f"using xgb_trainer.py."
            )

        self.feature_columns = joblib.load(
            feature_order_path
        )

        print(
            "\nFeature order loaded."
        )

        print(
            "Number of model features:",
            len(self.feature_columns)
        )

        # ==========================================
        # CHECK MODEL FEATURE COUNT
        # ==========================================

        model_feature_count = getattr(
            self.model,
            "n_features_in_",
            None
        )

        if (
            model_feature_count is not None
            and model_feature_count
            != len(self.feature_columns)
        ):

            raise ValueError(
                "\nModel and feature-order mismatch.\n"
                f"Model expects: "
                f"{model_feature_count} features\n"
                f"Feature file contains: "
                f"{len(self.feature_columns)} features\n\n"
                f"Retrain the XGBoost model."
            )

        # ==========================================
        # PRINT FEATURE ORDER
        # ==========================================

        print(
            "\nExpected feature order:"
        )

        for index, feature in enumerate(
            self.feature_columns,
            start=1
        ):

            print(
                f"{index:02d}. {feature}"
            )

    # ==================================================
    # SCORE
    # ==================================================

    def score(
        self,
        feature_list
    ):

        print(
            "\n========== XGBOOST DEBUG =========="
        )

        # ==========================================
        # 1. CHECK INPUT
        # ==========================================

        if not feature_list:

            raise ValueError(
                "\nFeature list is empty."
            )

        # ==========================================
        # 2. CONVERT TO DATAFRAME
        # ==========================================

        df = pd.DataFrame(
            feature_list
        )

        print(
            "\nDataFrame:"
        )

        print(
            df
        )

        print(
            "\nReceived DataFrame columns:"
        )

        print(
            df.columns.tolist()
        )

        # ==========================================
        # 3. CHECK FEATURE COUNT
        # ==========================================

        print(
            "\nExpected number of features:",
            len(self.feature_columns)
        )

        print(
            "Received number of columns:",
            len(df.columns)
        )

        # ==========================================
        # 4. CHECK MISSING FEATURES
        # ==========================================

        missing = [

            col
            for col in self.feature_columns
            if col not in df.columns

        ]

        if missing:

            print(
                "\nMISSING FEATURES:"
            )

            for feature in missing:

                print(
                    " -",
                    feature
                )

            raise ValueError(
                "\nFeatureBuilder did not "
                "return all required features."
            )

        # ==========================================
        # 5. CHECK EXTRA FEATURES
        # ==========================================

        extra = [

            col
            for col in df.columns
            if col not in self.feature_columns

        ]

        if extra:

            print(
                "\nWARNING: Extra features:"
            )

            for feature in extra:

                print(
                    " -",
                    feature
                )

            print(
                "\nExtra features will be ignored."
            )

        # ==========================================
        # 6. ORDER FEATURES EXACTLY
        # ==========================================

        df = df[
            self.feature_columns
        ].copy()

        # ==========================================
        # 7. CONVERT FEATURES TO NUMERIC
        # ==========================================

        for column in self.feature_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="raise"
            )

        # ==========================================
        # 8. CHECK NULL VALUES
        # ==========================================

        if df.isnull().any().any():

            null_columns = df.columns[
                df.isnull().any()
            ].tolist()

            print(
                "\nNULL FEATURES:"
            )

            for feature in null_columns:

                print(
                    " -",
                    feature
                )

            raise ValueError(
                "\nFeature input contains "
                "null values."
            )

        # ==========================================
        # 9. FINAL XGBOOST INPUT
        # ==========================================

        print(
            "\nFinal XGBoost Input:"
        )

        print(
            df
        )

        print(
            "\nFinal feature count:",
            len(df.columns)
        )

        print(
            "\nFinal feature order:"
        )

        for index, feature in enumerate(
            df.columns,
            start=1
        ):

            print(
                f"{index:02d}. {feature}"
            )

        # ==========================================
        # 10. PREDICT PROBABILITY
        # ==========================================

        print(
            "\nRunning XGBoost prediction..."
        )

        probabilities = (

            self.model.predict_proba(
                df
            )[:, 1]

        )

        # ==========================================
        # 11. PRINT SCORES
        # ==========================================

        print(
            "\nXGBoost Scores:"
        )

        for index, probability in enumerate(
            probabilities,
            start=1
        ):

            print(
                f"Document {index}: "
                f"{probability:.6f}"
            )

        print(
            "===================================\n"
        )

        return probabilities