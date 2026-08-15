from engine.xgb_ranker import XGBoostRanker

ranker = XGBoostRanker()

features = [
    {
        "age": 22,
        "student": 1,
        "vehicle_owner": 1,
        "taxpayer": 1,
        "searchable": 0,
        "issuer_present": 1,
        "semantic_score": 0.94,
        "graph_score": 1
    }
]

scores = ranker.score(features)

print(scores)