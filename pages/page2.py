"""หน้า 2: ฟอร์มเพิ่มและลบกิจกรรม"""
import calendar
from datetime import date

import storage

TITLE = "บันทึกกิจกรรม"
ALLOWED_CATEGORIES = ["การเรียน", "ออกกำลังกาย", "งานบ้าน", "อื่น ๆ"]
ALLOWED_STATUSES = ["กำลังทำ", "เสร็จสิ้น"]


def build(query=None):
    items = storage.load()
    rows = []
    for position, item in enumerate(items):
        row = dict(item)
        row["no"] = position
        rows.append(row)

    today = date.today()
    first_month = date(today.year - 3, 1, 1)
    last_month = date(today.year + 3, 12, 1)
    selected_text = (query or {}).get("date", today.isoformat())
    try:
        selected = date.fromisoformat(selected_text)
    except ValueError:
        selected = today
    if selected < first_month or selected > date(today.year + 3, 12, 31):
        selected = today

    month_text = (query or {}).get("month", selected.strftime("%Y-%m"))
    try:
        current_month = date.fromisoformat(month_text + "-01")
    except ValueError:
        current_month = date(selected.year, selected.month, 1)
    if current_month < first_month:
        current_month = first_month
    if current_month > last_month:
        current_month = last_month

    activities_by_date = {}
    selected_activities = []
    for item in rows:
        activities_by_date[item.get("date", "")] = activities_by_date.get(item.get("date", ""), 0) + 1
        if item.get("date", "") == selected.isoformat():
            selected_activities.append(item)

    weeks = calendar.monthcalendar(current_month.year, current_month.month)
    calendar_weeks = []
    for week in weeks:
        days = []
        for day_number in week:
            day = None
            if day_number != 0:
                day = date(current_month.year, current_month.month, day_number).isoformat()
            days.append({
                "number": day_number,
                "date": day,
                "count": activities_by_date.get(day, 0),
                "is_today": day == today.isoformat(),
                "is_selected": day == selected.isoformat(),
            })
        calendar_weeks.append(days)

    previous = current_month.month - 1
    previous_year = current_month.year
    if previous == 0:
        previous = 12
        previous_year = previous_year - 1
    next_month = current_month.month + 1
    next_year = current_month.year
    if next_month == 13:
        next_month = 1
        next_year = next_year + 1
    previous_date = date(previous_year, previous, 1)
    next_date = date(next_year, next_month, 1)

    return {
        "items": rows,
        "count": len(rows),
        "calendar_weeks": calendar_weeks,
        "month_label": current_month.strftime("%B %Y"),
        "month_thai": str(current_month.month) + "/" + str(current_month.year + 543),
        "previous_month": previous_date.strftime("%Y-%m"),
        "next_month": next_date.strftime("%Y-%m"),
        "can_go_previous": current_month > first_month,
        "can_go_next": current_month < last_month,
        "selected_date": selected.isoformat(),
        "selected_activities": selected_activities,
        "today_text": today.isoformat(),
        "range_text": str(today.year - 3) + " - " + str(today.year + 3),
    }


def check(form):
    if form.get("activity", "").strip() == "":
        return "กรุณากรอกชื่อกิจกรรม"
    if form.get("category", "") not in ALLOWED_CATEGORIES:
        return "กรุณาเลือกประเภทกิจกรรม"
    if not form.get("duration", "").isdigit() or int(form["duration"]) <= 0:
        return "เวลาต้องเป็นเลขจำนวนเต็มที่มากกว่า 0 นาที"
    if form.get("date", "").strip() == "":
        return "กรุณาเลือกวันที่"
    if form.get("status", "") not in ALLOWED_STATUSES:
        return "กรุณาเลือกสถานะ"
    return ""


def handle(form):
    items = storage.load()
    if "delete" in form:
        position = form.get("delete", "")
        if position.isdigit() and int(position) < len(items):
            removed = items.pop(int(position))
            storage.save(items)
            return "ลบกิจกรรม " + removed["activity"] + " แล้ว"
        return "ไม่พบกิจกรรมที่ต้องการลบ"

    error = check(form)
    if error != "":
        return error

    next_id = 1
    for item in items:
        if item["id"] >= next_id:
            next_id = item["id"] + 1
    items.append({
        "id": next_id,
        "activity": form["activity"].strip(),
        "category": form["category"],
        "duration": int(form["duration"]),
        "date": form["date"],
        "status": form["status"],
        "note": form.get("note", "").strip(),
    })
    storage.save(items)
    return "บันทึกกิจกรรม " + form["activity"].strip() + " แล้ว"
