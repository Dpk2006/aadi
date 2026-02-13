import csv
from io import StringIO

def logs_to_csv(logs: list[dict]) -> str:
    if not logs:
        return ""

    # flatten payload keys dynamically
    fieldnames = {"timestamp", "device_id", "device_name", "category", "branch_id"}
    for log in logs:
        fieldnames.update(log.get("payload", {}).keys())

    fieldnames = list(fieldnames)

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()

    for log in logs:
        row = {
            "timestamp": log["timestamp"].isoformat(),
            "device_id": log["device_id"],
            "device_name": log["device_name"],
            "category": log["category"],
            "branch_id": log["branch_id"],
        }
        row.update(log.get("payload", {}))
        writer.writerow(row)

    return buffer.getvalue()
