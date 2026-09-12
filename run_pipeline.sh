#!/bin/bash
# To tell linux know this is bash script

set -e
# Stop the script immediately if any command fails

echo "=== 1. Chạy Unit Test với Pytest ==="
uv run pytest tests/ -v

echo "=== 2. Build Docker Image ==="
docker build -t house-price-api:v1 .

echo "=== 3. Xóa container cũ (nếu có) và chạy container mới ==="
# || true để lệnh không bị lỗi set -e nếu container chưa tồn tại
docker rm -f house_api_container || true 
docker run -d -p 8000:8000 --name house_api_container house-price-api:v1

echo "=== Pipeline hoàn tất! API đang chạy tại http://localhost:8000 ==="

