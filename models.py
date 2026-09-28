"""ตัวแบบข้อมูลสำหรับกิจกรรมในเว็บไซต์จับเวลา"""


class Activity:
    def __init__(self, activity, category, duration, date, status, note):
        self.activity = activity
        self.category = category
        self.duration = duration
        self.date = date
        self.status = status
        self.note = note

    def describe(self):
        """คืนข้อความสรุปสั้น ๆ ของกิจกรรม"""
        return f"{self.activity} ใช้เวลา {self.duration} นาที ({self.status})"
