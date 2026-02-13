from fastapi import Request, HTTPException

MAX_PAYLOAD_BYTES = 256 * 1024  # 256 KB

async def payload_size_guard(request: Request):
    body = await request.body()
    if len(body) > MAX_PAYLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Payload too large"
        )
