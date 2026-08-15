from engine.rule_engine import RuleEngine
from models.user import User

rule_engine = RuleEngine("data/rules.json")

user = User(
    age=22,
    occupation="Student",
    state="Delhi",
    vehicle_owner=True,
    taxpayer=True,
    student=True,
    existing_documents=[]
)

recommendations = rule_engine.recommend(user)

print("Rule Based Recommendations:\n")

for doc in recommendations:
    print(doc)