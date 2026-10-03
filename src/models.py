from src.database import Base
from sqlalchemy import Column, Float, Integer, String, DateTime
from datetime import datetime, timezone

# Kế thừa từ Base đã khởi tạo ở database, để cho SQLAIchemy biết đây là 1 thực thể cần ánh xạ xuống DB
class PredictionHistory(Base):
    __tablename__ = "prediction_database"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 13 đặc trưng đầu vào từ Housing.csv
    area = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    stories = Column(Integer, nullable=False)
    parking = Column(Integer, nullable=False)

    # Các biến nhị phân (0 hoặc 1)
    mainroad = Column(Integer, nullable=False)
    guestroom = Column(Integer, nullable=False)
    basement = Column(Integer, nullable=False)
    hotwaterheating = Column(Integer, nullable=False)
    airconditioning = Column(Integer, nullable=False)
    prefarea = Column(Integer, nullable=False)
    is_semi_furnished = Column(Integer, nullable=False)
    is_unfurnished = Column(Integer, nullable=False)

    # Kết quả dự đoán từ mô hình
    predicted_price = Column(Float, nullable=False)
    # Thời điểm thực hiện dự đoán
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)