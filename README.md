# 🏡 End-to-End House Price Prediction API (MLOps Ready)
 
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistence-4169E1.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/pytest-Passing-brightgreen.svg)](https://docs.pytest.org/)
 
Dịch vụ Web API dự đoán giá bất động sản theo tiêu chuẩn Production/MLOps. Hệ thống tích hợp toàn diện từ quy trình xử lý dữ liệu, huấn luyện mô hình với K-Fold Cross-Validation, kiểm soát chất lượng dữ liệu đầu vào (Data Validation Gateway), bảo mật truy cập bằng API Key, lưu trữ lịch sử giao dịch vào cơ sở dữ liệu quan hệ (PostgreSQL) và tự động hóa kiểm thử, đóng gói bằng Docker.
 
---
 
## 📌 Tính năng nổi bật
 
- **Machine Learning Core & Model Governance:**
  - Tiền xử lý dữ liệu với `ColumnTransformer`: chuẩn hóa thuộc tính số bằng `StandardScaler`, mã hóa nhãn phân loại bằng `OneHotEncoder`.
  - Tinh chỉnh siêu tham số tự động (`GridSearchCV` 5-Fold Cross-Validation) giữa Linear Regression và Random Forest.
  - Lưu trữ artifact mô hình (`model.pkl`) kèm metadata theo dõi nguồn gốc (`model_metadata.json` gồm các chỉ số $R^2$, MAE, RMSE).
- **Production-grade API Design:**
  - Cổng kiểm soát dữ liệu đầu vào (Input Guardrail) sử dụng Pydantic Schema (`Literal`, `Field` constraints) ngăn chặn dữ liệu bẩn chạm vào mô hình.
  - Xác thực bảo mật qua Header `X-API-KEY`.
  - Endpoint `GET /history` truy vấn lịch sử dự đoán hỗ trợ phân trang (`limit`, `offset`) và sắp xếp bản ghi mới nhất.
- **Data Persistence:**
  - Bền vững hóa mọi lượt dự đoán vào PostgreSQL thông qua SQLAlchemy ORM.
  - Xử lý transaction an toàn (`commit` / `rollback`), lưu timestamp chuẩn UTC.
- **Kiểm thử tự động (Automated Testing):**
  - Kiểm thử toàn diện tầng API, Bảo mật, Validation và Database bằng `pytest`.
  - Sử dụng SQLite In-Memory (`sqlite:///:memory:`) và kỹ thuật Dependency Injection Override, giúp bộ test chạy độc lập hoàn toàn mà không cần bật cơ sở dữ liệu thật.
- **Triển khai nhất quán (DevOps/MLOps):**
  - Quản lý phụ thuộc chính xác bằng trình quản lý gói `uv` (`uv.lock`).
  - Đóng gói toàn bộ service bằng Docker và điều phối đa dịch vụ (API + PostgreSQL) bằng Docker Compose.
---
 
## 📁 Cấu trúc thư mục
 
```text
.
├── artifacts/                  # Model artifacts & lineage metadata
│   ├── model.pkl               # Pipeline đã huấn luyện (Preprocessor + Model)
│   └── model_metadata.json     # Hyperparameters, evaluation metrics (R2, MAE, RMSE)
├── data/
│   ├── raw/Housing.csv         # Dữ liệu bất động sản thô
│   └── processed/Housing.csv   # Dữ liệu đã qua tiền xử lý
├── notebooks/
│   └── eda_and_training.ipynb  # Phân tích khám phá dữ liệu (EDA)
├── src/                        # Mã nguồn chính
│   ├── api/                    # Tầng Web API (FastAPI)
│   │   ├── main.py             # Khởi tạo ứng dụng, routing & lifespan management
│   │   ├── schemas.py          # Pydantic data schemas & validation rules
│   │   └── security.py         # Lớp xác thực API Key
│   ├── ml/                     # Xử lý Machine Learning
│   │   ├── pipeline.py         # Pipeline tiền xử lý & cấu hình mô hình
│   │   └── predictor.py        # Logic load model & suy luận (inference)
│   ├── config.py               # Quản lý cấu hình & biến môi trường (Pydantic Settings)
│   ├── database.py             # Quản lý kết nối & Session SQLAlchemy
│   ├── models.py               # SQLAlchemy ORM models (Entity bảng CSDL)
│   └── train.py                # Script huấn luyện với GridSearchCV (5-Fold CV)
├── tests/                      # Bộ kiểm thử tự động (Pytest)
│   ├── conftest.py             # Test fixtures & cấu hình SQLite in-memory
│   └── test_api.py             # Test cases: Auth, Validation, Database & History
├── Dockerfile                  # Cấu hình containerization cho API
├── docker-compose.yml          # Điều phối hệ thống (FastAPI Service + PostgreSQL Service)
├── run_pipeline.sh             # Script CI/CD tự động: Test -> Build -> Deploy
├── pyproject.toml              # Khai báo dependencies dự án (uv)
└── uv.lock                     # Khóa phiên bản dependencies
```
 
---
 
## 📊 Kết quả đánh giá mô hình
 
Mô hình được đánh giá trên tập kiểm thử độc lập (Test Set - 20%):
 
| Mô hình | Siêu tham số tối ưu (Best Params) | R2 Score | MAE | RMSE | Trạng thái |
| :--- | :--- | :---: | ---: | ---: | :--- |
| Linear Regression | Default | 0.6529 | 970,043 | 1,324,507 | ✅ Được chọn (Production) |
| Random Forest (Tuned) | `max_depth: 10`, `n_estimators: 150` | 0.6016 | 1,032,068 | 1,419,013 | ❌ Loại (Candidate) |
 
> Toàn bộ thông số huấn luyện được tự động lưu vết tại `artifacts/model_metadata.json`.
 
---
 
## 🛠 Yêu cầu môi trường & Cài đặt
 
### 1. Chuẩn bị biến môi trường
 
Tạo file `.env` tại thư mục gốc của dự án:
 
```env
API_KEY=mlops_phase2_secret_key_2026
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/house_db
RAW_DATA_PATH=data/raw/Housing.csv
MODEL_PATH=artifacts/model.pkl
```
 
### 2. Cài đặt môi trường Local (với `uv`)
 
```bash
# Đồng bộ môi trường ảo và cài đặt dependencies
uv sync
 
# Kích hoạt môi trường ảo
source .venv/bin/activate
```
 
---
 
## 🚦 Hướng dẫn vận hành
 
### 1. Huấn luyện lại mô hình (Retraining Pipeline)
 
```bash
uv run python -m src.train
```
 
### 2. Thực thi kiểm thử tự động (Pytest)
 
Hệ thống sử dụng SQLite ảo trong RAM, kiểm tra toàn bộ 6 kịch bản kiểm thử:
 
```bash
uv run pytest tests/ -v
```
 
### 3. Khởi chạy bằng Docker Compose (Khuyên dùng)
 
Khởi động đồng thời cả API Service và PostgreSQL Database chỉ với một lệnh:
 
```bash
docker compose up -d --build
```
 
- **API Endpoint:** <http://localhost:8000>
- **Swagger UI (tài liệu tương tác tự động sinh):** <http://localhost:8000/docs>
---
 
## 📡 API Reference & Ví dụ gọi API
 
### 1. Dự đoán giá nhà (`POST /predict`)
 
Yêu cầu bắt buộc phải có header `X-API-KEY`.
 
**cURL Request mẫu:**
 
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: mlops_phase2_secret_key_2026" \
  -d '{
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
  }'
```
 
**JSON Response (`200 OK`):**
 
```json
{
  "predicted_price": 7968276.13,
  "message": "Success"
}
```
 
### 2. Truy vấn lịch sử (`GET /history`)
 
Hỗ trợ phân trang để tối ưu bộ nhớ:
 
```bash
curl -X GET "http://localhost:8000/history?limit=10&offset=0" \
  -H "X-API-KEY: mlops_phase2_secret_key_2026"
```
 
**JSON Response (`200 OK`):**
 
```json
{
  "total": 1,
  "limit": 10,
  "offset": 0,
  "data": [
    {
      "id": 1,
      "area": 7420.0,
      "bedrooms": 4,
      "bathrooms": 2,
      "stories": 3,
      "parking": 2,
      "mainroad": true,
      "guestroom": false,
      "basement": false,
      "hotwaterheating": false,
      "airconditioning": true,
      "prefarea": true,
      "is_semi_furnished": false,
      "is_unfurnished": false,
      "predicted_price": 7968276.13,
      "created_at": "2026-10-04T04:15:00Z"
    }
  ]
}
```
 