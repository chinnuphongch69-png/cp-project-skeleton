"""หน้า 1: จับเวลาและแสดงตารางกิจกรรมที่บันทึกไว้"""
import storage

TITLE = "รายการกิจกรรม"
ALLOWED_CATEGORIES = ["การเรียน", "ออกกำลังกาย", "งานบ้าน", "อื่น ๆ"]


def build():
    items = storage.load()
    rows = []
    categories = {}

    for item in items:
        row = dict(item)
        row["status_class"] = "good" if item["status"] == "เสร็จสิ้น" else "gold"
        rows.append(row)
        category = item["category"]
        categories[category] = categories.get(category, 0) + 1

    return {"items": rows, "count": len(rows), "categories": categories}


def handle(form):
    """บันทึกเวลาที่ JavaScript นับได้จากตัวจับเวลา"""
    activity = form.get("activity", "").strip()
    duration_text = form.get("duration", "")
    category = form.get("category", "")
    date = form.get("date", "").strip()
    mode = form.get("mode", "stopwatch")

    if activity == "":
        return "กรุณากรอกชื่อกิจกรรมก่อนบันทึก"
    if category not in ALLOWED_CATEGORIES:
        return "กรุณาเลือกประเภทกิจกรรม"
    if date == "":
        return "กรุณาเลือกวันที่ก่อนบันทึก"
    if mode not in ("stopwatch", "countdown"):
        return "ไม่พบโหมดจับเวลาที่เลือก"
    if not duration_text.isdigit() or int(duration_text) <= 0:
        return "กรุณาเริ่มจับเวลาอย่างน้อย 1 นาที"

    items = storage.load()
    next_id = 1
    for item in items:
        if item["id"] >= next_id:
            next_id = item["id"] + 1
    items.append({
        "id": next_id,
        "activity": activity,
        "category": category,
        "duration": int(duration_text),
        "date": date,
        "status": "เสร็จสิ้น",
        "note": form.get("note", "").strip(),
    })
    storage.save(items)
    return "บันทึกเวลา " + activity + " แล้ว"
