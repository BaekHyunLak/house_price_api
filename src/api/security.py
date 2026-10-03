import os
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

# Khai báo FastAPI sẽ đọc thẻ căn cước từ phần Header có tên "X-API-KEY"
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

# Kéo chìa khóa thật từ file .env lên để đối chiếu
EXPECTED_API_KEY = os.getenv("API_KEY_SECRET")

def get_api_key(api_key: str = Security(api_key_header)):
    if not EXPECTED_API_KEY or api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Denied access: Invalid or missing API Key"
        )
    return api_key
