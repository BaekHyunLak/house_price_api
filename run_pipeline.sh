#!/bin/bash
# Shebang: run the script using Bash interpreter

set -e
# Stop the script immediately if any command fails

CONTAINER_NAME="house_api_container"
IMAGE_NAME="house-price-api:v1"
PORT=8000

echo "=== 1. Chạy Unit Test với Pytest ==="
uv run pytest tests/ -v

echo "=== 2. Build Docker Image ==="
docker build -t "$IMAGE_NAME" .

echo "=== 3. Xóa container cũ (nếu có) và chạy container mới ==="
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true 
docker run -d -p "$PORT:$PORT" --env-file .env --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "=== 4. Chờ dịch vụ khởi động và kiểm tra trạng thái ==="
sleep 2

# Kiểm tra xem container có đang ở trạng thái 'running' hay không
if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null)" != "true" ]; then
    echo "❌ Lỗi: Container khởi động thất bại hoặc bị crash ngay sau khi chạy!"
    echo "--- LOGS CONTAINER ---"
    docker logs "$CONTAINER_NAME"
    exit 1
fi

echo "=== Pipeline hoàn tất! API đang chạy tại http://localhost:$PORT ==="