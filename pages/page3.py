"""หน้า 3: สรุปสถิติจากเวลาที่บันทึก"""
import models
import storage

TITLE = "สถิติเวลา"


def build():
    items = storage.load()
    total = 0
    completed = 0
    longest = None
    per_category = {}

    for item in items:
        total = total + item["duration"]
        if item["status"] == "เสร็จสิ้น":
            completed = completed + 1
        if longest is None or item["duration"] > longest["duration"]:
            longest = item
        category = item["category"]
        per_category[category] = per_category.get(category, 0) + item["duration"]

    average = total / len(items) if items else 0
    biggest = max(per_category.values()) if per_category else 0
    bars = []
    for category, minutes in per_category.items():
        percent = int(minutes * 100 / biggest) if biggest else 0
        bars.append({"label": category, "minutes": minutes, "percent": percent})

    summary = "ยังไม่มีข้อมูล"
    if longest:
        activity = models.Activity(longest["activity"], longest["category"], longest["duration"], longest["date"], longest["status"], longest["note"])
        summary = activity.describe()
    return {"count": len(items), "total": total, "average": average, "completed": completed, "longest": longest, "summary": summary, "bars": bars}
