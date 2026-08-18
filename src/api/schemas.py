from typing import Literal
from pydantic import BaseModel, Field

class HousePredictionRequest(BaseModel):
    area: float = Field(..., gt=0, description='Diện tích căn nhà (sqft)')
    bedrooms: int = Field(..., ge=1, description='Số phòng ngủ')
    bathrooms: int = Field(..., ge=1, description='Số phòng tắm')
    stories: int = Field(..., ge=1, description='Số tầng')
    parking: int = Field(..., ge=0, description='Số chỗ đỗ xe')

    mainroad: Literal['yes', 'no']
    guestroom: Literal['yes', 'no']
    basement: Literal['yes', 'no']
    hotwaterheating: Literal['yes', 'no']
    airconditioning: Literal['yes', 'no']
    prefarea: Literal['yes', 'no']
    furnishingstatus: Literal['furnished', 'semi-furnished', 'unfurnished']

class HousePredictionResponse(BaseModel):
    predicted_price: float
    message: str="Success"