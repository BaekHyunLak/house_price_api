from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_client_happy_path():
    """
    Case 1: Gửi dữ liệu chuẩn xác 100%.
    Kỳ vọng: API chạy mượt mà, trả về mã 200 và có chứa key predicted_price.
    """
    valid_payload = {
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
        "furnishingstatus": "semi-furnished"
    }
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert "message" in data
    assert data["message"] == "Success"
    
    assert isinstance(data["predicted_price"], float)

def test_predict_validation_error():
    """
    Case 2: Cố tình gửi dữ liệu sai quy tắc.
    Kỳ vọng: Pydantic của FastAPI sẽ chặn lại và ném ra lỗi 422.
    """
    invalid_payload = {
        "area": -50,              # LỖI 1: Diện tích bị âm (phải > 0)
        "bedrooms": 4,
        "bathrooms": 2,
        "stories": 3,
        "parking": 2,
        "mainroad": "maybe",      # LỖI 2: Sai danh mục (chỉ được yes/no)
        "guestroom": "no",
        "basement": "no",
        "hotwaterheating": "no",
        "airconditioning": "yes",
        "prefarea": "yes",
        "furnishingstatus": "semi-furnished"
    }
    
    response = client.post("/predict", json=invalid_payload)
    
    # Kiểm tra mã trạng thái phải là 422 (Unprocessable Entity)
    assert response.status_code == 422
    
    # Có thể kiểm tra thêm xem trong thông báo lỗi có chỉ đích danh trường 'area' và 'mainroad' không
    error_data = response.json()
    error_locations = [err["loc"][-1] for err in error_data["detail"]]
    
    assert "area" in error_locations
    assert "mainroad" in error_locations
