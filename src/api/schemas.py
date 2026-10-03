from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

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

# Schema cho tung ban ghi lich su tra ve
class PredictionHistoryItem(BaseModel):
    id: int
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    parking: int
    mainroad: bool
    guestroom: bool
    basement: bool
    hotwaterheating: bool
    airconditioning: bool
    prefarea: bool
    is_semi_furnished: bool
    is_unfurnished: bool
    predicted_price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema tong quan co phan trang
class PredictionHistoryResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: list[PredictionHistoryItem]


