# Chọn Base Image
FROM python:3.12-slim

# Thiết lập thư mục làm việc mặc định trong container
WORKDIR /app

# Cài đặt công cụ uv
RUN pip install uv

# Chuẩn bị môi trường (Tận dụng cache)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Khai báo biến môi trường hệ thống để sử dụng trực tiếp các thư viện đã cài
# /app/.venv/bin là thư mcuj chứa các thư viện và lệnh chạy mà công cụ uv vừa cài đặt vào môi trường ảo
ENV PATH="/app/.venv/bin:$PATH"

# Chuyển mã nguồn và mô hình (Tuyệt đối không copy .env)
COPY src/ ./src/
COPY artifacts/ ./artifacts/

# Mở cổng giao tiếp
EXPOSE 8000

# Lệnh khởi động
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]