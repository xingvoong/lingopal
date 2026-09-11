"""
Mock Hotel PMS (Property Management System)
Returns fake data — no real database needed.
"""

RESERVATIONS = {
    "RES001": {
        "id": "RES001",
        "guest_name": "Alice Chen",
        "room": "204",
        "room_type": "Standard King",
        "check_in": "2026-09-12",
        "check_out": "2026-09-15",
        "status": "confirmed",
    },
    "RES002": {
        "id": "RES002",
        "guest_name": "Bob Tanaka",
        "room": "510",
        "room_type": "Deluxe Queen",
        "check_in": "2026-09-10",
        "check_out": "2026-09-11",
        "status": "confirmed",
    },
}

AVAILABLE_UPGRADES = {
    "Standard King": ["Deluxe King", "Suite"],
    "Deluxe Queen": ["Suite"],
    "Deluxe King": ["Suite"],
}


def lookup_reservation(guest_name: str) -> dict:
    for res in RESERVATIONS.values():
        if res["guest_name"].lower() == guest_name.lower():
            return {"found": True, "reservation": res}
    return {"found": False, "message": f"No reservation found for '{guest_name}'."}


def request_upgrade(reservation_id: str, desired_room_type: str) -> dict:
    res = RESERVATIONS.get(reservation_id)
    if not res:
        return {"approved": False, "reason": "Reservation not found."}

    current = res["room_type"]
    available = AVAILABLE_UPGRADES.get(current, [])

    if desired_room_type in available:
        return {
            "approved": True,
            "reservation_id": reservation_id,
            "upgraded_to": desired_room_type,
            "message": f"Upgrade to {desired_room_type} confirmed at no extra charge.",
        }
    return {
        "approved": False,
        "reason": f"{desired_room_type} is not available or not an upgrade from {current}.",
        "available_upgrades": available,
    }


def request_early_late_checkout(reservation_id: str, request_type: str, requested_time: str) -> dict:
    res = RESERVATIONS.get(reservation_id)
    if not res:
        return {"approved": False, "reason": "Reservation not found."}

    # Mock availability logic: late checkout approved up to 14:00, early checkin from 11:00
    if request_type == "late_checkout":
        approved = requested_time <= "14:00"
    elif request_type == "early_checkin":
        approved = requested_time >= "11:00"
    else:
        approved = False

    if approved:
        return {
            "approved": True,
            "reservation_id": reservation_id,
            "request_type": request_type,
            "time": requested_time,
            "message": f"{request_type.replace('_', ' ').title()} at {requested_time} approved.",
        }
    return {
        "approved": False,
        "reason": f"We cannot accommodate {request_type.replace('_', ' ')} at {requested_time}.",
        "suggestion": "Please contact the front desk for alternatives.",
    }
