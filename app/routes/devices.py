from fastapi import APIRouter
from datetime import datetime
from app.database import db
from app.utils.security import generate_api_key, hash_api_key

router = APIRouter(prefix="/devices")

@router.post("/register")
async def register_device(
    device_id: str,
    device_name: str,
    category: str,
    branch_id: str
):
    api_key = generate_api_key()
    hashed = hash_api_key(api_key)

    device_doc = {
        "_id": device_id,
        "device_name": device_name,
        "category": category,
        "branch_id": branch_id,
        "api_key_hash": hashed,
        "status": "active",
        "created_at": datetime.utcnow()
    }

    await db.devices.insert_one(device_doc)

    return {
        "device_id": device_id,
        "api_key": api_key  # SHOW ONCE
    }
