import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.database import Base, get_db
from src.api.security import get_api_key
# 1. Tạo Database SQLite in-memory dùng riêng cho Testing
# StaticPool & check_same_thread=False giúp giữ nguyên DB trên cùng một luồng test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Tạo mới toàn bộ các bảng trước mỗi test và dọn sạch sau khi test xong."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Ghi đè (Override) dependency get_db của FastAPI để 
    trỏ vào SQLite test DB thay vì PostgreSQL thật.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    def override_get_api_key():
        return "valid_test_key"
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_api_key] = override_get_api_key
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()