from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import Response
from datetime import datetime
from app.database import db
from app.models import GenericLogPayload
from app.dependencies.auth import authenticate_device
from app.dependencies.payload_guard import payload_size_guard
from app.utils.csv_export import logs_to_csv
from app.utils.mongo import serialize_mongo, serialize_many

router = APIRouter()

@router.post("/logs/{category}/{device_name}")
async def ingest_log(
    category: str,
    device_name: str,
    payload: GenericLogPayload = ...,
    device=Depends(authenticate_device),
    _=Depends(payload_size_guard)
):
    if device_name != device["device_name"]:
        raise HTTPException(400, f"Device name mismatch. Registered name is '{device['device_name']}'")

    log_doc = {
        "timestamp": datetime.now(),
        "category": category,
        "device_name": device_name,
        "device_id": device["_id"],
        "branch_id": device["branch_id"],
        "payload": payload.data
    }

    await db.logs.insert_one(log_doc)

    return {"status": "ok"}


@router.get("/logs/{category}/{device_name}")
async def get_logs(
    category: str,
    device_name: str,
    mode: str = Query("latest", enum=["latest", "json", "csv"]),
    limit: int = Query(10, le=1000),
    device=Depends(authenticate_device)
):
    base_query = {
        "category": category,
        "device_name": device_name,
        "device_id": device["_id"],
    }

    if mode == "latest":
        log = await db.logs.find_one(
            base_query,
            sort=[("timestamp", -1)]
        )
        if not log:
            raise HTTPException(404, "No data found")
        
        return serialize_mongo(log)

    cursor = (
        db.logs.find(base_query)
        .sort("timestamp", -1)
        .limit(limit)
    )
    logs = await cursor.to_list(length=limit)

    if not logs:
        raise HTTPException(404, "No data found")

    if mode == "json":
        return serialize_many(logs)

    if mode == "csv":
        csv_data = logs_to_csv(logs)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={device_name}_logs.csv"
            }
        )
