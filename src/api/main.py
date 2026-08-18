from fastapi import FastAPI

# Kiểm duyệt dữ liệu đầu vào
from src.api.schemas import HousePredictionRequest, HousePredictionResponse
from src.ml.predictor import predictor

# Khởi tạo FastAPI (Quầy giao dịch)
app = FastAPI(
    title='House Price Prediction API',
    description="API dự đoán giá nhà dựa trên ML",
    version="1.0.0"
)

# Tạo endpoint POST
@app.post("/predict", response_model=HousePredictionResponse)
def predict_price(request_data: HousePredictionRequest):

    price = predictor.predict(request_data)
    return HousePredictionResponse(
        predicted_price=round(price, 2),
        message="Success"
    )
    
