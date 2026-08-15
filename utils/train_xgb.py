import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "data/training_data.csv"

MODEL_PATH = "trained_models/xgb_model.pkl"

FEATURE_ORDER_PATH = (
    "trained_models/xgb_features.pkl"
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print(
    "\n========================================"
)

print(
    "LOADING TRAINING DATASET"
)

print(
    "========================================"
)

print(
    "\nLoading dataset..."
)

df = pd.read_csv(
    DATASET_PATH
)

print(
    "\nDataset shape:"
)

print(
    df.shape
)


# ============================================================
# 2. FEATURE COLUMNS
# MUST MATCH DATA GENERATOR + FEATURE BUILDER
# ============================================================

feature_columns = [

    # ========================================================
    # USER FEATURES
    # ========================================================

    "age",
    "student",
    "vehicle_owner",
    "taxpayer",

    # ========================================================
    # BASIC DOCUMENT FEATURES
    # ========================================================

    "searchable",
    "issuer_present",

    # ========================================================
    # RANKING FEATURES
    # ========================================================

    "semantic_score",
    "graph_score",

    # ========================================================
    # CATEGORY FEATURES
    # ========================================================

    "vehicle_category",
    "financial_category",
    "health_category",
    "employment_category",
    "class10_category",
    "class12_category",
    "higher_education_category",
    "identity_category",

    # ========================================================
    # VEHICLE FEATURES
    # ========================================================

    "driving_license",
    "vehicle_registration",
    "vehicle_insurance",
    "challan_document",
    "vehicle_tax",
    "vehicle_fitness",

    # ========================================================
    # FINANCIAL FEATURES
    # ========================================================

    "pan_document",
    "epan_document",
    "form16_document",
    "tds_document",
    "passport_document",

    # ========================================================
    # HEALTH FEATURES
    # ========================================================

    "health_card",
    "pmjay_document",
    "health_fitness",
    "health_policy",
    "covid_vaccine",
    "national_health_id",
    "health_insurance",

    # ========================================================
    # EMPLOYMENT / SOCIAL FEATURES
    # ========================================================

    "uan_card",
    "epran_card",
    "pension_certificate",
    "ration_card",

    # ========================================================
    # CLASS X FEATURES
    # ========================================================

    "apaar_document",
    "class10_marksheet",
    "class10_passing",
    "class10_migration",
    "class10_school_leaving",

    # ========================================================
    # CLASS XII FEATURES
    # ========================================================

    "class12_marksheet",
    "class12_passing",
    "class12_migration",

    # ========================================================
    # HIGHER EDUCATION FEATURES
    # ========================================================

    "class1_9_marksheets",
    "degree_document",
    "provisional_degree",
    "diploma_document",
    "bonafide_document",

    # ========================================================
    # IDENTITY FEATURES
    # ========================================================

    "caste_certificate",
    "income_certificate",
    "birth_certificate",
    "ckyc_card"
]


# ============================================================
# 3. LABEL COLUMN
# ============================================================

label_column = "label"


# ============================================================
# 4. FEATURE COUNT CHECK
# ============================================================

print(
    "\nExpected number of features:"
)

print(
    len(feature_columns)
)

if len(feature_columns) != 55:

    raise ValueError(
        f"Feature configuration error. "
        f"Expected 55 features but found "
        f"{len(feature_columns)}."
    )


# ============================================================
# 5. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = (
    feature_columns
    + [label_column]
)

missing_columns = [

    column
    for column in required_columns

    if column not in df.columns
]

if missing_columns:

    print(
        "\nMISSING COLUMNS:"
    )

    for column in missing_columns:

        print(
            " -",
            column
        )

    raise ValueError(
        "\nTraining dataset is missing "
        "required columns."
    )


# ============================================================
# 6. CHECK EXTRA COLUMNS
# ============================================================

extra_columns = [

    column
    for column in df.columns

    if column not in required_columns
]

if extra_columns:

    print(
        "\nWARNING: Extra columns detected:"
    )

    for column in extra_columns:

        print(
            " -",
            column
        )

    print(
        "\nExtra columns will be ignored."
    )


# ============================================================
# 7. ORDER DATASET
# ============================================================

df = df[
    required_columns
].copy()


# ============================================================
# 8. CHECK DATASET SHAPE
# ============================================================

print(
    "\nDataset after selecting required columns:"
)

print(
    df.shape
)

expected_columns = 56

if len(df.columns) != expected_columns:

    raise ValueError(
        f"Expected {expected_columns} "
        f"columns (55 features + label), "
        f"but found {len(df.columns)}."
    )


# ============================================================
# 9. CHECK NULL VALUES
# ============================================================

print(
    "\nChecking null values..."
)

null_columns = [

    column
    for column in df.columns

    if df[column].isnull().any()
]

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
        "null values."
    )

print(
    "No null values found."
)


# ============================================================
# 10. CREATE X AND y
# ============================================================

X = df[
    feature_columns
].copy()

y = df[
    label_column
].copy()


# ============================================================
# 11. DISPLAY FEATURE INFORMATION
# ============================================================

print(
    "\n========================================"
)

print(
    "FEATURE CONFIGURATION"
)

print(
    "========================================"
)

for index, feature in enumerate(
    feature_columns,
    start=1
):

    print(
        f"{index:02d}. {feature}"
    )


print(
    "\nTotal features:",
    len(feature_columns)
)


# ============================================================
# 12. LABEL DISTRIBUTION
# ============================================================

print(
    "\n========================================"
)

print(
    "LABEL DISTRIBUTION"
)

print(
    "========================================"
)

print(
    y.value_counts()
)

print(
    "\nLabel percentages:"
)

print(
    y.value_counts(
        normalize=True
    ) * 100
)


# ============================================================
# 13. CHECK LABEL CLASSES
# ============================================================

if y.nunique() < 2:

    raise ValueError(
        "\nTraining data must contain "
        "both label 0 and label 1."
    )


# ============================================================
# 14. TRAIN / TEST SPLIT
# ============================================================

print(
    "\n========================================"
)

print(
    "TRAIN / TEST SPLIT"
)

print(
    "========================================"
)

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


# ============================================================
# 15. CREATE XGBOOST MODEL
# ============================================================

print(
    "\n========================================"
)

print(
    "CREATING XGBOOST MODEL"
)

print(
    "========================================"
)

model = XGBClassifier(

    n_estimators=200,

    max_depth=5,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="binary:logistic",

    eval_metric="logloss",

    random_state=42,

    n_jobs=-1
)


# ============================================================
# 16. TRAIN MODEL
# ============================================================

print(
    "\nTraining XGBoost..."
)

model.fit(
    X_train,
    y_train
)

print(
    "Training completed."
)


# ============================================================
# 17. PREDICTIONS
# ============================================================

print(
    "\nGenerating predictions..."
)

y_pred = model.predict(
    X_test
)

y_probability = (

    model.predict_proba(
        X_test
    )[:, 1]
)


# ============================================================
# 18. EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


# ============================================================
# 19. PRINT EVALUATION
# ============================================================

print(
    "\n========================================"
)

print(
    "XGBOOST EVALUATION"
)

print(
    "========================================"
)

print(
    f"\nAccuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)


# ============================================================
# 20. CLASSIFICATION REPORT
# ============================================================

print(
    "\n========================================"
)

print(
    "CLASSIFICATION REPORT"
)

print(
    "========================================"
)

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 21. CONFUSION MATRIX
# ============================================================

print(
    "========================================"
)

print(
    "CONFUSION MATRIX"
)

print(
    "========================================"
)

cm = confusion_matrix(
    y_test,
    y_pred
)

print(
    cm
)


# ============================================================
# 22. FEATURE IMPORTANCE
# ============================================================

print(
    "\n========================================"
)

print(
    "FEATURE IMPORTANCE"
)

print(
    "========================================"
)

importance = pd.DataFrame({

    "feature":
        feature_columns,

    "importance":
        model.feature_importances_

})

importance = (

    importance
    .sort_values(
        by="importance",
        ascending=False
    )
)

print(
    importance.to_string(
        index=False
    )
)


# ============================================================
# 23. CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    "trained_models",
    exist_ok=True
)


# ============================================================
# 24. SAVE MODEL
# ============================================================

print(
    "\nSaving XGBoost model..."
)

joblib.dump(
    model,
    MODEL_PATH
)

print(
    "Model saved to:"
)

print(
    MODEL_PATH
)


# ============================================================
# 25. SAVE FEATURE ORDER
# ============================================================

print(
    "\nSaving feature order..."
)

joblib.dump(
    feature_columns,
    FEATURE_ORDER_PATH
)

print(
    "Feature order saved to:"
)

print(
    FEATURE_ORDER_PATH
)


# ============================================================
# 26. FINAL VALIDATION
# ============================================================

print(
    "\n========================================"
)

print(
    "FINAL TRAINING VALIDATION"
)

print(
    "========================================"
)

print(
    "Dataset features :",
    len(feature_columns)
)

print(
    "Dataset columns  :",
    len(df.columns)
)

print(
    "Training samples  :",
    len(X_train)
)

print(
    "Testing samples   :",
    len(X_test)
)

print(
    "Model saved       :",
    os.path.exists(
        MODEL_PATH
    )
)

print(
    "Feature order     :",
    os.path.exists(
        FEATURE_ORDER_PATH
    )
)

print(
    "\n========================================"
)

print(
    "XGBOOST TRAINING COMPLETE"
)

print(
    "========================================\n"
)