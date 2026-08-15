# DigiLocker AI Document Recommendation System

An AI-powered document recommendation system designed for DigiLocker that recommends relevant digital documents based on a user's profile and natural-language request.

The system combines **intent detection, semantic similarity, graph-based relationships, business rules, and XGBoost ranking** to generate personalized document recommendations.

---

## Features

- Natural-language document search
- Intent-based document recommendation
- Category-aware recommendations
- Semantic document matching
- Graph-based document relationships
- XGBoost-based ranking
- Business-rule-based scoring
- Personalized recommendations using user profile
- Existing-document filtering
- Explainable recommendations
- JSON-based document knowledge base
- FastAPI backend
- React frontend
- ChromaDB vector database

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
     +------+------+
     |      |      |
     v      v      v
 Semantic  Graph  Knowledge
  Search  Score    Base
     |      |      |
     +------+------+
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