from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
from typing import Annotated
from contextlib import asynccontextmanager

# Kiểm duyệt dữ liệu đầu vào
from src.api.schemas import HousePredictionRequest, HousePredictionResponse, PredictionHistoryItem, PredictionHistoryResponse
from src.ml.predictor import predictor

from src.database import get_db, Base, engine
from src.models import PredictionHistory
from src.api.security import get_api_key

# Cấu hình logging để dễ debug khi chạy container
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Khởi tạo bảng data thành công")
    except Exception as e:
        logger.error(f"Lỗi khởi tạo database metadata: {e}")

    yield


# Khởi tạo FastAPI (Quầy giao dịch)
app = FastAPI(
    title='House Price Prediction API',
    description="API dự đoán giá nhà dựa trên ML",
    version="2.0.0",
    lifespan=lifespan
)

DbSession = Annotated[Session, Depends(get_db)]
ApiKeyAuth = Annotated[str, Depends(get_api_key)]

def map_request_to_prediction_record(
        req: HousePredictionRequest,
        predicted_price: float 
) -> PredictionHistory:
    """
    Hàm mapper chuyển đổi Data Contract (Pydantic Schema) 
    sang Data Entity (SQLAlchemy Model).
    """
    return PredictionHistory(
        area=req.area,
        bedrooms=req.bedrooms,
        bathrooms=req.bathrooms,
        stories=req.stories,
        parking=req.parking,
        mainroad=(req.mainroad == "yes"),
        guestroom=(req.guestroom == "yes"),
        basement=(req.basement == "yes"),
        hotwaterheating=(req.hotwaterheating == "yes"),
        airconditioning=(req.airconditioning == "yes"),
        prefarea=(req.prefarea == "yes"),
        is_semi_furnished=(req.furnishingstatus == "semi-furnished"),
        is_unfurnished=(req.furnishingstatus == "unfurnished"),
        predicted_price=predicted_price
    )

# Endpoint kiểm tra sức khỏe hệ thống (Health Check)
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 'healthy'}

# Endpoint history
@app.get(
    "/history",
    response_model=PredictionHistoryResponse,
    summary="Xem lại danh sách lịch sử dự đoán",
    description="Truy vấn danh sách lịch sử dự đoán từ cơ sở dữ liệu có hỗ trợ phân trang (pagination) và sắp xếp mới nhất"
)
def get_prediction_history(
    api_key: ApiKeyAuth,
    db: DbSession,
    limit: int = Query(default=10, ge=1, le=100, description="Số lượng bản ghi tối đa trên một trang"),
    offset: int = Query(default=0, ge=0, description="Số lượng bản ghi bỏ qua (vị trí bắt đầu)")
):
    try:
        # Đếm tổng số bản ghi trong bảng
        total_records = db.query(PredictionHistory).count()

        # Truy vấn dữ liệu có phân trang, sắp xếp theo time mới nhất
        records = (
            db.query(PredictionHistory)
            .order_by(PredictionHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return PredictionHistoryResponse(
            total=total_records,
            limit=limit,
            offset=offset,
            data=records
        )
    except Exception as e:
        logger.error(f"Lỗi khi truy vấn lịch sử dự đoán: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể lấy dữ liệu lịch sử từ database."
        )


# Tạo endpoint POST
@app.post("/predict", response_model=HousePredictionResponse)
def predict_price(
    request_data: HousePredictionRequest,
    api_key: ApiKeyAuth,
    db: DbSession
):

    # 1. Dự đoán giá
    try:
        price = round(predictor.predict(request_data), 2)
    except Exception as e:
        logger.error(f"ML Model inference error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi trong quá trình suy luận mô hình ML."
        )

    # 2. Lưu vào DB 
    try:
        db_record = map_request_to_prediction_record(request_data, price)
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dự đoán thành công nhưng lưu trữ lịch sử thất bại: {str(e)}"
        )
    # 3. Trả kết quả    
    return HousePredictionResponse(
        predicted_price=round(price, 2),
        message="Success"
    )
    