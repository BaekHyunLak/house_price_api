import os
import pytest
from src.models import PredictionHistory
from src.api.security import get_api_key
from src.api.main import app
# Payload mẫu hợp lệ
VALID_PAYLOAD = {
    "area": 7420,
    "bedrooms": 4,
    "bathrooms": 2,
    "stories": 3,
    "parking": 2,
    "mainroad": "yes",
    "guestroom": "no",
    "basement": "no",
    "hotwaterheating": "no",
    "airconditioning": "yes",
    "prefarea": "yes",
    "furnishingstatus": "furnished"
}

# Lấy API Key từ biến môi trường hoặc dùng key test mặc định
VALID_API_KEY = os.getenv("API_KEY", "mlops_phase2_secret_key_2026")
AUTH_HEADERS = {"X-API-KEY": VALID_API_KEY}


# ==========================================
# 1. TEST BẢO MẬT & XÁC THỰC (AUTHENTICATION)
# ==========================================

def test_predict_missing_api_key(client):
    """Xóa override để test hàm get_api_key thật khi không có header."""
    app.dependency_overrides.pop(get_api_key, None)
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 403


def test_predict_invalid_api_key(client):
    """Xóa override để test hàm get_api_key thật khi header sai."""
    app.dependency_overrides.pop(get_api_key, None)
    headers = {"X-API-KEY": "wrong_key_123"}
    response = client.post("/predict", json=VALID_PAYLOAD, headers=headers)
    assert response.status_code == 403


# ==========================================
# 2. TEST VALIDATION DỮ LIỆU ĐẦU VÀO (PYDANTIC)
# ==========================================

def test_predict_invalid_data_validation(client):
    """Gửi dữ liệu sai ràng buộc (area <= 0) -> Phải trả về 422 Unprocessable Entity."""
    invalid_payload = VALID_PAYLOAD.copy()
    invalid_payload["area"] = -100  # Vi phạm ràng buộc gt=0

    response = client.post("/predict", json=invalid_payload, headers=AUTH_HEADERS)
    assert response.status_code == 422


# ==========================================
# 3. TEST INFERENCE VÀ LƯU DATABASE THỰC TẾ
# ==========================================

def test_predict_success_and_save_to_db(client, db_session):
    """
    Test Happy Path:
    - Trả về 200 OK và có giá tiền dự đoán.
    - Database SQLite thực sự ghi nhận đúng 1 bản ghi với đúng giá trị mapping.
    """
    response = client.post("/predict", json=VALID_PAYLOAD, headers=AUTH_HEADERS)
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_price" in data
    assert data["message"] == "Success"

    # Kiểm tra trực tiếp trong DB test
    records = db_session.query(PredictionHistory).all()
    assert len(records) == 1
    saved_record = records[0]
    assert saved_record.area == 7420
    
    # Sửa từ 'is True/False' sang '== True/False' để tương thích cả SQLite lẫn PostgreSQL
    assert bool(saved_record.mainroad) is True
    assert bool(saved_record.is_semi_furnished) is False
    assert bool(saved_record.is_unfurnished) is False
    assert saved_record.predicted_price == data["predicted_price"]


# ==========================================
# 4. TEST ENDPOINT LỊCH SỬ (GET /history)
# ==========================================

def test_get_history_empty(client):
    """Kiểm tra khi chưa có lượt dự đoán nào thì mảng data rỗng."""
    response = client.get("/history", headers=AUTH_HEADERS)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["total"] == 0
    assert res_data["data"] == []


def test_get_history_pagination(client):
    """Thực hiện dự đoán 2 lần, sau đó lấy lịch sử xem có đúng 2 bản ghi không."""
    client.post("/predict", json=VALID_PAYLOAD, headers=AUTH_HEADERS)
    client.post("/predict", json=VALID_PAYLOAD, headers=AUTH_HEADERS)

    response = client.get("/history?limit=10&offset=0", headers=AUTH_HEADERS)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["total"] == 2
    assert len(res_data["data"]) == 2