import os

import pandas as pd
import xgboost as xgb
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


class XGBoostTrainer:

    def __init__(
        self,
        csv_path="data/xgb_training.csv"
    ):

        self.csv_path = csv_path

    def train(self):

        print("\nLoading training dataset...")

        # =====================================================
        # LOAD DATASET
        # =====================================================

        df = pd.read_csv(
            self.csv_path
        )

        print("\nDataset shape:")
        print(df.shape)

        # =====================================================
        # EXACT FEATURE ORDER
        #
        # MUST MATCH FeatureBuilder
        # =====================================================

        feature_columns = [

            # =================================================
            # USER FEATURES
            # =================================================

            "age",
            "student",
            "vehicle_owner",
            "taxpayer",

            # =================================================
            # BASIC DOCUMENT FEATURES
            # =================================================

            "searchable",
            "issuer_present",

            # =================================================
            # RANKING FEATURES
            # =================================================

            "semantic_score",
            "graph_score",

            # =================================================
            # CATEGORY FEATURES
            # =================================================

            "vehicle_category",
            "financial_category",
            "health_category",
            "employment_category",
            "class10_category",
            "class12_category",
            "higher_education_category",
            "identity_category",

            # =================================================
            # VEHICLE FEATURES
            # =================================================

            "driving_license",
            "vehicle_registration",
            "vehicle_insurance",
            "challan_document",
            "vehicle_tax",
            "vehicle_fitness",

            # =================================================
            # FINANCIAL FEATURES
            # =================================================

            "pan_document",
            "epan_document",
            "form16_document",
            "tds_document",
            "passport_document",

            # =================================================
            # HEALTH FEATURES
            # =================================================

            "health_card",
            "pmjay_document",
            "health_fitness",
            "health_policy",
            "covid_vaccine",
            "national_health_id",
            "health_insurance",

            # =================================================
            # EMPLOYMENT / SOCIAL FEATURES
            # =================================================

            "uan_card",
            "epran_card",
            "pension_certificate",
            "ration_card",

            # =================================================
            # CLASS X FEATURES
            # =================================================

            "apaar_document",
            "class10_marksheet",
            "class10_passing",
            "class10_migration",
            "class10_school_leaving",

            # =================================================
            # CLASS XII FEATURES
            # =================================================

            "class12_marksheet",
            "class12_passing",
            "class12_migration",

            # =================================================
            # HIGHER EDUCATION FEATURES
            # =================================================

            "class1_9_marksheets",
            "degree_document",
            "provisional_degree",
            "diploma_document",
            "bonafide_document",

            # =================================================
            # IDENTITY FEATURES
            # =================================================

            "caste_certificate",
            "income_certificate",
            "birth_certificate",
            "ckyc_card"
        ]

        # =====================================================
        # FEATURE COUNT
        # =====================================================

        print(
            "\nExpected number of features:",
            len(feature_columns)
        )

        # Should be 55

        if len(feature_columns) != 55:

            raise ValueError(
                f"Internal feature configuration error. "
                f"Expected 55 features, "
                f"found {len(feature_columns)}."
            )

        # =====================================================
        # CHECK MISSING FEATURES
        # =====================================================

        missing = [

            feature
            for feature in feature_columns
            if feature not in df.columns

        ]

        if missing:

            print("\nMISSING FEATURES:")

            for feature in missing:

                print(
                    " -",
                    feature
                )

            raise ValueError(
                "\nTraining dataset is missing "
                "required features."
            )

        # =====================================================
        # CHECK LABEL
        # =====================================================

        if "label" not in df.columns:

            raise ValueError(
                "\nTraining dataset does not contain "
                "'label' column."
            )

        # =====================================================
        # CHECK EXTRA FEATURES
        # =====================================================

        extra = [

            column
            for column in df.columns

            if (
                column not in feature_columns
                and column != "label"
            )

        ]

        if extra:

            print(
                "\nWARNING: Extra columns detected:"
            )

            for column in extra:

                print(
                    " -",
                    column
                )

        # =====================================================
        # CREATE X AND Y
        # =====================================================

        X = df[
            feature_columns
        ].copy()

        y = df[
            "label"
        ].copy()

        # =====================================================
        # CHECK DATA TYPES
        # =====================================================

        print(
            "\nFeature data types:"
        )

        print(
            X.dtypes
        )

        # =====================================================
        # CHECK NULL VALUES
        # =====================================================

        null_columns = (

            X.columns[
                X.isnull().any()
            ].tolist()

        )

        if null_columns:

            print(
                "\nNULL VALUES FOUND:"
            )

            for column in null_columns:

                print(
                    " -",
                    column
                )

            raise ValueError(
                "\nTraining dataset contains "
                "null feature values."
            )

        # =====================================================
        # CHECK LABEL VALUES
        # =====================================================

        print(
            "\nLabel distribution:"
        )

        print(
            y.value_counts()
        )

        if y.nunique() < 2:

            raise ValueError(
                "\nTraining data must contain "
                "both label 0 and label 1."
            )

        # =====================================================
        # TRAIN / TEST SPLIT
        # =====================================================

        X_train, X_test, y_train, y_test = (

            train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42,
                stratify=y
            )

        )

        print(
            "\nTraining samples:",
            len(X_train)
        )

        print(
            "Testing samples:",
            len(X_test)
        )

        # =====================================================
        # TRAIN XGBOOST
        # =====================================================

        print(
            "\nTraining XGBoost..."
        )

        model = xgb.XGBClassifier(

            n_estimators=200,

            max_depth=5,

            learning_rate=0.05,

            subsample=0.9,

            colsample_bytree=0.9,

            objective="binary:logistic",

            eval_metric="logloss",

            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        print(
            "Training completed."
        )

        # =====================================================
        # PREDICTIONS
        # =====================================================

        predictions = model.predict(
            X_test
        )

        probabilities = (

            model.predict_proba(
                X_test
            )[:, 1]

        )

        # =====================================================
        # EVALUATION
        # =====================================================

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        roc_auc = roc_auc_score(
            y_test,
            probabilities
        )

        # =====================================================
        # PRINT EVALUATION
        # =====================================================

        print(
            "\n========== XGBOOST EVALUATION =========="
        )

        print(
            f"Accuracy : {accuracy:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall   : {recall:.4f}"
        )

        print(
            f"F1 Score : {f1:.4f}"
        )

        print(
            f"ROC-AUC  : {roc_auc:.4f}"
        )

        print(
            "========================================"
        )

        # =====================================================
        # FEATURE IMPORTANCE
        # =====================================================

        importance = pd.Series(

            model.feature_importances_,

            index=feature_columns

        ).sort_values(
            ascending=False
        )

        print(
            "\nFeature Importance:"
        )

        print(
            importance
        )

        # =====================================================
        # CREATE MODEL DIRECTORY
        # =====================================================

        os.makedirs(
            "trained_models",
            exist_ok=True
        )

        # =====================================================
        # SAVE MODEL
        # =====================================================

        model_path = (
            "trained_models/xgb_model.pkl"
        )

        joblib.dump(
            model,
            model_path
        )

        print(
            "\nModel saved successfully:"
        )

        print(
            model_path
        )

        # =====================================================
        # SAVE FEATURE ORDER
        # =====================================================

        feature_order_path = (
            "trained_models/xgb_features.pkl"
        )

        joblib.dump(
            feature_columns,
            feature_order_path
        )

        print(
            "\nFeature order saved:"
        )

        print(
            feature_order_path
        )

        # =====================================================
        # SAVE TRAINING METRICS
        # =====================================================

        metrics = {

            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc,

            "training_samples":
                len(X_train),

            "testing_samples":
                len(X_test),

            "feature_count":
                len(feature_columns)
        }

        metrics_path = (
            "trained_models/xgb_metrics.pkl"
        )

        joblib.dump(
            metrics,
            metrics_path
        )

        print(
            "\nMetrics saved:"
        )

        print(
            metrics_path
        )

        return model


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    trainer = XGBoostTrainer()

    trainer.train()