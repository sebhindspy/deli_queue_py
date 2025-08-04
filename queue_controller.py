from typing import List, Dict, Optional
from fastapi import HTTPException

class QueueController:
    def __init__(self):
        self.queue: List[Dict[str, any]] = []  # Each guest is a dict: {"email": str, "premium": bool}
        self.is_open = True
        self.premium_limit = 3  # Default limit, can be changed via admin
        self.one_shot_price = 5  # Default price in dollars
        self.venue_mode_enabled = False
        self.venue_capacity = 0
        self.guests_in_venue = 0

    ### system status

    def get_status(self):
        return {
            "is_open": self.is_open,
            "queue": self.queue,
            "premium_limit": self.premium_limit,
            "one_shot_price": self.one_shot_price,
            "venue_mode_enabled": self.venue_mode_enabled,
            "venue_capacity": self.venue_capacity,
            "guests_in_venue": self.guests_in_venue
        }

    ### joining and leaving the queue

    def join_queue(self, email: str):
        if not self.is_open:
            raise HTTPException(status_code=403, detail="Queue is closed.")
        if not any(g["email"] == email for g in self.queue):
            self.queue.append({"email": email, "premium": False})
    
    def join_premium_queue(self, email: str):
        if not self.is_open:
            raise HTTPException(status_code=403, detail="Queue is closed.")

        # Remove guest if already in queue
        existing_guest = None
        for i, guest in enumerate(self.queue):
            if guest["email"] == email:
                if guest.get("premium"):
                    raise HTTPException(status_code=400, detail="Guest already in premium queue.")
                existing_guest = self.queue.pop(i)
                break

        # Check premium slot availability
        premium_count = sum(1 for g in self.queue[1:] if g["premium"])
        if premium_count >= self.premium_limit:
            raise HTTPException(status_code=403, detail="No premium slots available.")

        # Insert at next available premium position (starting at index 1)
        insert_index = 1
        while insert_index < len(self.queue) and self.queue[insert_index]["premium"]:
            insert_index += 1

        self.queue.insert(insert_index, {
            "email": email,
            "premium": True
        })

    
    """
    def join_premium_queue(self, email: str):
        if not self.is_open:
            raise HTTPException(status_code=403, detail="Queue is closed.")

        # Check if guest is already in the queue
        for guest in self.queue:
            if guest["email"] == email:
                if guest.get("premium"):
                    raise HTTPException(status_code=400, detail="Guest already in premium queue.")
                else:
                    guest["premium"] = True  # Upgrade to premium
                    return

        # Check premium slot availability
        premium_count = sum(1 for g in self.queue[1:] if g["premium"])
        if premium_count >= self.premium_limit:
            raise HTTPException(status_code=403, detail="No premium slots available.")

        # Insert at next available premium position (starting at index 1)
        insert_index = 1
        while insert_index < len(self.queue) and self.queue[insert_index]["premium"]:
            insert_index += 1

        self.queue.insert(insert_index, {"email": email, "premium": True})
        """

    def get_position(self, email: str) -> int:
        for i, guest in enumerate(self.queue):
            if guest["email"] == email:
                return i
        raise HTTPException(status_code=404, detail="Guest not in queue.")

    def advance_queue(self):
        if self.venue_mode_enabled and self.is_venue_full():
            raise HTTPException(status_code=403, detail="Venue is full.")
        if self.queue:
            self.queue.pop(0)
            if self.venue_mode_enabled:
                self.increment_guests_in_venue()

    def leave_queue(self, email: str):
        for i, guest in enumerate(self.queue):
            if guest["email"] == email:
                self.queue.pop(i)
                if self.venue_mode_enabled:
                    self.increment_guests_in_venue()
                return


    ### basic queue settings

    def open_queue(self):
        self.is_open = True

    def close_queue(self):
        self.is_open = False

    def reset_queue(self):
        self.queue.clear()

    def mock_guests(self, count: int):
        for i in range(count):
            self.queue.append({"email": f"mock{i}@example.com", "premium": False})


    ### premuim queue bits

    def set_premium_limit(self, limit: int):
        self.premium_limit = limit

    def set_one_shot_price(self, price: int):
        self.one_shot_price = price

    def is_premium(self, email: str) -> bool:
        for guest in self.queue:
            if guest["email"] == email:
                return guest["premium"]
        raise HTTPException(status_code=404, detail="Guest not in queue.")


    ### venue mode functionality

    def set_venue_mode(self, enabled: bool):
        self.venue_mode_enabled = enabled

    def set_venue_capacity(self, capacity: int):
        self.venue_capacity = capacity

    def is_venue_full(self) -> bool:
        return self.guests_in_venue >= self.venue_capacity if self.venue_mode_enabled else False

    def increment_guests_in_venue(self):
        if self.guests_in_venue < self.venue_capacity:
            self.guests_in_venue += 1
        else:
            raise HTTPException(status_code=403, detail="Venue is full.")

    def decrement_guests_in_venue(self):
        if self.guests_in_venue > 0:
            self.guests_in_venue -= 1
        else:
            raise HTTPException(status_code=400, detail="No guests in venue to remove.")



