import joblib
from src.config import settings
from src.api.schemas import HousePredictionRequest
import pandas as pd

MODEL_PATH = settings.model_path

# Trạm 1: Pydantic Object -> Python Dictionary
# Trạm 2: Python Dictionary -> Pandas DataFrame (Cực kỳ quan trọng)
# Trạm 3: Đưa DataFrame qua Pipeline
class ModelPredictor():
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
    def predict(self, data: HousePredictionRequest) -> float:
        data_dict = data.model_dump()
        input_df = pd.DataFrame([data_dict])

        prediction = self.model.predict(input_df)
        return float(prediction[0])

predictor = ModelPredictor()
