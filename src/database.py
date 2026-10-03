import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Lấy URL kết nối từ biến môi trường (hoặc dùng giá trị mặc định cho local dev)
# Cấu trúc: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/house_price_db"
)

# Khởi tạo Engine với Connection Pooling mặc định của SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=5,       # Số lượng kết nối duy trì sẵn trong pool
    max_overflow=10,   # Số kết nối tối đa có thể tạo thêm khi vượt quá pool_size
    pool_timeout=30,   # Thời gian chờ (giây) trước khi báo lỗi nếu hết kết nối
)

# Tạo SessionLocal class - mỗi instance của class này là một database session độc lập
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base class dùng để kế thừa cho các ORM Models sau này
Base = declarative_base()

def get_db():
    """
    Dependency function để cấp một Database Session cho mỗi API request.
    Đảm bảo session luôn được đóng lại dù API có chạy thành công hay văng lỗi.
    """
    db = SessionLocal() # Mở một session (mượn 1 kết nối từ Pool)
    try:
        yield db        # Tạm dừng hàm ở đây, đẩy session cho FastAPI xử lý request
    finally:
        db.close()      # BẤT CHẤP request thành công hay mô hình ML văng lỗi, 
                        # khi request kết thúc, dòng này luôn được chạy để trả kết nối về Pool.