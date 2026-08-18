# Project's Folder

house_price_api/
├── .venv/                   # Môi trường ảo (uv tự tạo, KHÔNG push lên Git)
├── .gitignore               # Khai báo file/folder cần bỏ qua khi commit Git
├── pyproject.toml           # File quản lý cấu hình & thư viện của uv
├── uv.lock                  # Lockfile phiên bản thư viện của uv
├── README.md                # Tài liệu hướng dẫn chạy dự án
│
├── artifacts/               # Lưu trữ file mô hình ML đã train
│   └── model.pkl            # (Hoặc model.joblib) File model sau khi train
│
├── data/                    # Thư mục chứa dữ liệu (Gợi ý: Thêm vào .gitignore)
│   ├── raw/                 # Dữ liệu thô ban đầu (data.csv)
│   └── processed/           # Dữ liệu đã qua làm sạch
│
├── notebooks/               # Nơi chứa các file Jupyter Notebook để EDA & thử nghiệm
│   └── eda_and_training.ipynb
│
└── src/                     # Source code chính của ứng dụng
    ├── __init__.py
    ├── config.py            # Cấu hình biến môi trường (.env)
    ├── train.py             # Script chạy huấn luyện mô hình ML từ CLI
    │
    ├── ml/                  # Module quản lý xử lý Machine Learning
    │   ├── __init__.py
    │   ├── pipeline.py      # Tiền xử lý dữ liệu (Preprocessing / Feature Engineering)
    │   └── predictor.py     # Class load model.pkl và thực hiện hàm predict()
    │
    └── api/                 # Module Web Server (FastAPI)
        ├── __init__.py
        ├── main.py          # Entrypoint chạy FastAPI app
        ├── schemas.py       # Pydantic Schemas (Định dạng dữ liệu Input/Output)
        └── routes.py        # Các đường dẫn API endpoints (ví dụ: /predict, /health)