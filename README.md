# 🏡 House Price Prediction API

API dự đoán giá nhà dựa trên mô hình Machine Learning, được xây dựng với FastAPI và đóng gói hoàn chỉnh bằng Docker.

## 🎯 Mục đích dự án
Dự án này giải quyết bài toán dự đoán giá bất động sản dựa trên các đặc trưng của căn nhà (diện tích, số phòng ngủ, phòng tắm, có/không có điều hòa,...). 
Mô hình Machine Learning (`LinearRegression`) được huấn luyện, lưu trữ và triển khai thành một dịch vụ Web API có khả năng tiếp nhận dữ liệu, kiểm duyệt chặt chẽ và phản hồi siêu tốc (< 1ms).

## 🛠 Kiến trúc công nghệ
- **Ngôn ngữ:** Python 3.12
- **Machine Learning:** `scikit-learn`, `pandas`, `joblib`
- **Backend Framework:** FastAPI, Pydantic (Data Validation)
- **Môi trường & Đóng gói:** `uv` (Package Manager), Docker, Docker Compose

## 📁 Project Structure

```text
.
├── artifacts/                  # Model artifacts & lineage metadata
│   ├── model.pkl               # Trained pipeline (Preprocessor + Model)
│   └── model_metadata.json     # Hyperparameters, evaluation metrics (R2, MAE, RMSE)
├── data/
│   ├── raw/Housing.csv         # Raw dataset
│   └── processed/Housing.csv   # Cleaned dataset
├── notebooks/
│   └── eda_and_training.ipynb  # Exploratory Data Analysis & initial experiments
├── src/                        # Main source code
│   ├── api/                    # Web API layer (FastAPI)
│   │   ├── main.py             # App initialization, routing & lifecycle management
│   │   ├── routes.py           # Additional API endpoints
│   │   ├── schemas.py          # Pydantic data schemas & request/response validation
│   │   └── security.py         # API Key authentication guardrail
│   ├── ml/                     # Machine Learning core
│   │   ├── pipeline.py         # ColumnTransformer (StandardScaler + OneHotEncoder)
│   │   └── predictor.py        # Model loading & inference logic
│   ├── config.py               # Pydantic Settings & environment variables
│   ├── database.py             # SQLAlchemy engine & session management
│   ├── models.py               # SQLAlchemy ORM database entities
│   └── train.py                # Retraining script with GridSearchCV (5-Fold CV)
├── tests/                      # Automated test suite (Pytest)
│   ├── conftest.py             # SQLite in-memory DB fixture & dependency overrides
│   └── test_api.py             # Unit tests for Auth, Validation, DB persistence & History
├── Dockerfile                  # Containerization specifications
├── docker-compose.yml          # Multi-container orchestration (FastAPI + PostgreSQL)
├── run_pipeline.sh             # Automation script: Test -> Build -> Deploy
├── pyproject.toml              # Project dependencies & build configuration (uv)
├── requirements.txt            # Exported production dependencies
└── uv.lock                     # Deterministic dependency lockfile
```

## 🚀 Hướng dẫn cài đặt và sử dụng

### Bước 1: Chuẩn bị cấu hình
Tạo file `.env` ở thư mục gốc của dự án và khai báo đường dẫn tới file mô hình đã huấn luyện:
```env
MODEL_PATH=artifacts/model.pkl
```
### Bước 2: Khởi chạy hệ thống bằng Docker
Đảm bảo máy tính của bạn đã cài đặt Docker. Mở Terminal tại thư mục gốc và chạy 2 lệnh sau:
1. Đóng gói Docker Image:
```
docker build -t house-price-api:v1 .
```
2. Khởi chạy Docker Container:
```
docker run -d -p 8000:8000 --env-file .env --name my-api-server house-price-api:v1
```


