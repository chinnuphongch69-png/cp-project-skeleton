"""หน้า 3: สรุปสถิติจากเวลาที่บันทึก"""
from datetime import date, timedelta

import models
import storage

TITLE = "สถิติเวลา"
PERIODS = {
    "all": "ทั้งหมด",
    "today": "วันนี้",
    "week": "7 วันล่าสุด",
    "month": "เดือนนี้",
}


def build(query=None):
    period = (query or {}).get("period", "all")
    if period not in PERIODS:
        period = "all"

    today = date.today()
    start_date = None
    if period == "today":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=6)
    elif period == "month":
        start_date = today.replace(day=1)

    items = storage.load()
    if start_date is not None:
        filtered_items = []
        for item in items:
            try:
                item_date = date.fromisoformat(item["date"])
            except (KeyError, TypeError, ValueError):
                continue
            if start_date <= item_date <= today:
                filtered_items.append(item)
        items = filtered_items

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
    return {
        "count": len(items),
        "total": total,
        "average": average,
        "completed": completed,
        "longest": longest,
        "summary": summary,
        "bars": bars,
        "period": period,
        "periods": PERIODS,
    }
