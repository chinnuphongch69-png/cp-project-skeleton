"""Tests for statistics period filtering."""
from datetime import date, timedelta

import app as webapp
import storage


def _activity(activity, duration, activity_date, category="การเรียน", status="เสร็จสิ้น"):
    return {
        "id": activity,
        "activity": activity,
        "category": category,
        "duration": duration,
        "date": activity_date.isoformat(),
        "status": status,
        "note": "",
    }


def test_statistics_filter_applies_to_all_metrics(monkeypatch):
    today = date.today()
    monkeypatch.setattr(storage, "load", lambda: [
        _activity("today", 10, today),
        _activity("week", 20, today - timedelta(days=6), "ออกกำลังกาย", "กำลังทำ"),
        _activity("outside-week", 30, today - timedelta(days=7)),
    ])
    page, error = webapp.load_page("page3")
    assert error is None

    context = page.build({"period": "week"})

    assert context["count"] == 2
    assert context["total"] == 30
    assert context["average"] == 15
    assert context["completed"] == 1
    assert context["longest"]["activity"] == "week"
    assert {bar["label"] for bar in context["bars"]} == {"การเรียน", "ออกกำลังกาย"}


def test_statistics_month_filter_excludes_previous_month(monkeypatch):
    today = date.today()
    first_of_month = today.replace(day=1)
    previous_month = first_of_month - timedelta(days=1)
    monkeypatch.setattr(storage, "load", lambda: [
        _activity("this-month", 40, first_of_month),
        _activity("previous-month", 50, previous_month),
        _activity("future", 60, today + timedelta(days=1)),
    ])
    page, error = webapp.load_page("page3")
    assert error is None

    context = page.build({"period": "month"})

    assert context["count"] == 1
    assert context["total"] == 40
    assert context["longest"]["activity"] == "this-month"


def test_statistics_invalid_period_defaults_to_all(monkeypatch):
    today = date.today()
    monkeypatch.setattr(storage, "load", lambda: [
        _activity("old", 25, today - timedelta(days=50)),
    ])
    page, error = webapp.load_page("page3")
    assert error is None

    context = page.build({"period": "invalid"})

    assert context["period"] == "all"
    assert context["count"] == 1
    assert context["total"] == 25
