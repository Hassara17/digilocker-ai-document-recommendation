from engine.xgb_trainer import XGBoostTrainer


trainer = XGBoostTrainer(
    "data/xgb_training.xlsx"
)

trainer.train()