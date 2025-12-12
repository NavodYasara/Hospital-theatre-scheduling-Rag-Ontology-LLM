from datetime import datetime, time
from typing import Tuple

def validate_time_format(time_str: str) -> Tuple[bool, str]:
    """Validate time string format (HH:MM)"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True, ""
    except ValueError:
        return False, "Invalid time format. Use HH:MM (e.g., 09:00)"

def validate_date_format(date_str: str) -> Tuple[bool, str]:
    """Validate date string format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2025-01-15)"

def validate_duration(duration: int) -> Tuple[bool, str]:
    """Validate surgery duration"""
    if duration < 30:
        return False, "Duration too short. Minimum 30 minutes"
    if duration > 600:
        return False, "Duration too long. Maximum 10 hours (600 minutes)"
    return True, ""

def validate_name(name: str) -> Tuple[bool, str]:
    """Validate entity name"""
    if not name or len(name.strip()) == 0:
        return False, "Name cannot be empty"
    if len(name) > 100:
        return False, "Name too long. Maximum 100 characters"
    return True, ""