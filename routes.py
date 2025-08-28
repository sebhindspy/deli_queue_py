from fastapi import APIRouter
from models import Guest

# from queue_controller import QueueController
from queue_instance import queue


router = APIRouter()
# queue = QueueController()


@router.post("/join")
def join_queue(guest: Guest):
    queue.join_queue(guest.email)
    return {"message": "Joined queue", "position": queue.get_position(guest.email)}


@router.get("/position/{email}")
def get_position(email: str):
    return {"position": queue.get_position(email)}


@router.post("/advance")
def advance_queue():
    queue.advance_queue()
    return {"message": "Queue advanced"}


@router.post("/leave")
def leave_queue(guest: Guest):
    queue.leave_queue(guest.email)
    return {"message": "Left queue"}


@router.post("/reset")
def reset_queue():
    queue.reset_queue()
    return {"message": "Queue reset"}


@router.post("/mock-guests/{count}")
def mock_guests(count: int):
    queue.mock_guests(count)
    return {"message": f"{count} mock guests added"}


@router.post("/reset-mock-counter")
def reset_mock_counter():
    queue.reset_mock_counter()
    return {"message": "Mock guest counter reset to 0"}


@router.get("/status")
def get_status():
    status = queue.get_status()
    return {
        **status,
        "total_guests": len(status["queue"]),
        "next_guest": status["queue"][0] if status["queue"] else None,
        "venue_mode_enabled": status.get("venue_mode_enabled", False),
        "guests_in_venue": status.get("guests_in_venue", 0),
    }


@router.post("/open")
def open_queue():
    queue.open_queue()
    return {"message": "Queue opened"}


@router.post("/close")
def close_queue():
    queue.close_queue()
    return {"message": "Queue closed"}


@router.post("/set-venue-mode")
def set_venue_mode(payload: dict):
    queue.set_venue_mode(payload["enabled"])
    return {"message": f"Venue mode {'enabled' if payload['enabled'] else 'disabled'}"}


@router.post("/set-venue-capacity")
def set_venue_capacity(payload: dict):
    queue.set_venue_capacity(payload["capacity"])
    return {"message": f"Venue capacity set to {payload['capacity']}"}


@router.post("/decrement-venue")
def decrement_venue():
    queue.decrement_guests_in_venue()
    return {"message": "Guest removed from venue"}
