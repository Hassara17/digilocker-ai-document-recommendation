# DigiLocker AI Document Recommendation System

An AI-powered document recommendation system designed for DigiLocker that recommends relevant digital documents based on a user's profile and natural-language request.

The system combines **intent detection, semantic similarity, graph-based relationships, business rules, and XGBoost ranking** to generate personalized document recommendations.

---

## Features

* Natural-language document search
* Intent-based document recommendation
* Category-aware recommendations
* Semantic document matching
* Graph-based document relationships
* XGBoost-based ranking
* Business-rule-based scoring
* Personalized recommendations using user profile
* Existing-document filtering
* Explainable recommendations
* JSON-based document knowledge base
* FastAPI backend
* React frontend
* ChromaDB vector database

---

## Recommendation Pipeline

```text
User
  |
  v
Natural Language Query
  |
  v
Intent Detection
  |
  +--------------------+
  |                    |
  v                    v
Document Intent     Category Intent
  |                    |
  +---------+----------+
            |
            v
    Candidate Generation
            |
      +-----+-----+-----+
      |           |     |
      v           v     v
  Semantic      Graph  Knowledge
   Search       Score    Base
      |           |       |
      +-----------+-------+
                  |
                  v
           Feature Builder
                  |
                  v
            XGBoost Ranker
                  |
                  v
           Business Ranker
                  |
                  v
             Final Score
                  |
                  v
            Recommendation
                  |
                  v
             Explanation
```

---

## Project Structure

```text
digilocker-recommendation/
│
├── api/                    # API routes and endpoints
├── config/                 # Configuration files
├── data/                   # Knowledge base and application data
├── database/               # ChromaDB/vector database
├── engine/                 # Recommendation and ranking engines
├── frontend/               # React frontend
├── models/                 # Model-related files
├── services/               # Application services
├── tests/                  # Test cases
├── trained_models/         # Trained ML models
│   ├── xgb_model.pkl
│   └── xgb_features.pkl
├── utils/                  # Utility and training scripts
│
├── app.py                  # FastAPI application entry point
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── README.md
└── .gitignore
```

---

## Trained XGBoost Model

The trained XGBoost recommendation model is included in the repository.

```text
trained_models/
├── xgb_model.pkl
└── xgb_features.pkl
```

The recommendation engine loads the trained model from:

```text
trained_models/xgb_model.pkl
```

The feature configuration is stored in:

```text
trained_models/xgb_features.pkl
```

Therefore, the model does **not** need to be retrained before running the application.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Hassara17/digilocker-ai-document-recommendation.git
cd digilocker-ai-document-recommendation
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Backend

The backend is implemented using **FastAPI** and the application entry point is:

```text
app.py
```

From the project root, run:

```bash
uvicorn app:app --reload
```

The FastAPI server will start at:

```text
http://127.0.0.1:8000
```

## FastAPI Swagger Documentation

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# Running the Frontend

The frontend is implemented using **React**.

Open a **new terminal** while the FastAPI server is running.

Navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will display the frontend URL in the terminal. Usually it is:

```text
http://localhost:5173
```

---

# Running the Complete Application

The backend and frontend should be run in separate terminals.

## Terminal 1 — FastAPI Backend

From the project root:

```bash
uvicorn app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Terminal 2 — React Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

The React frontend communicates with the FastAPI backend to obtain document recommendations.

---

# Recommendation Flow

The system processes a user's request through the following stages:

### 1. User Profile

The system receives user information such as:

* Age
* Occupation
* State
* Student status
* Vehicle ownership
* Taxpayer status
* Existing documents

### 2. Natural-Language Query

Example:

```text
I bought a bike
```

### 3. Intent Detection

The system identifies the intent behind the user's query and determines relevant document/category requirements.

### 4. Candidate Generation

Potential documents are generated using:

* Knowledge Base
* Semantic Search
* Graph Relationships
* Business Rules

### 5. Feature Building

Features such as:

* Semantic score
* Graph score
* User profile features
* Document attributes
* Intent-related features

are generated for candidate documents.

### 6. XGBoost Ranking

The trained XGBoost model predicts the relevance of candidate documents.

### 7. Business Ranking

Business rules are applied to refine the ranking and remove unsuitable recommendations.

### 8. Final Recommendation

The system returns the most relevant documents along with an explanation for why each document was recommended.

---

# Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Backend              | FastAPI               |
| Frontend             | React                 |
| Programming Language | Python                |
| ML Model             | XGBoost               |
| Embedding Model      | Sentence Transformers |
| Vector Database      | ChromaDB              |
| Graph Processing     | NetworkX              |
| API Server           | Uvicorn               |
| Data Format          | JSON                  |
| Frontend Build Tool  | Vite                  |

---

# API

The FastAPI backend exposes endpoints for interacting with the recommendation system.

API documentation can be accessed through:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to test the recommendation API directly.

---

# Example Query

```text
I bought a bike
```

The system analyzes the query and user profile, generates candidate documents, ranks them using the trained XGBoost model, and returns personalized recommendations with explanations.

---

# Model Files

The trained model files are version-controlled in GitHub:

```text
trained_models/xgb_model.pkl
trained_models/xgb_features.pkl
```

The repository intentionally excludes the Python virtual environment and other generated/cache files through `.gitignore`.

---

# Future Improvements

* Advanced multilingual query understanding
* Improved intent classification
* Deep-learning-based ranking
* Continuous model retraining
* User feedback-based recommendation improvement
* Improved recommendation explanations
* Production deployment
* Authentication and authorization
* Monitoring and model performance tracking

---

## License

This project is developed as an AI-powered document recommendation solution for DigiLocker.
