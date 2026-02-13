from fastapi import Header, HTTPException
from app.database import db
from app.utils.security import hash_api_key

async def authenticate_device(x_api_key: str = Header(...)):
    hashed = hash_api_key(x_api_key)

    device = await db.devices.find_one({
        "api_key_hash": hashed,
        "status": "active"
    })

    if not device:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return device
