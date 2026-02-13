def serialize_mongo(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


def serialize_many(docs: list[dict]) -> list[dict]:
    return [serialize_mongo(doc) for doc in docs]
