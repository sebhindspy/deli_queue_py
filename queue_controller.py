from typing import List, Dict, Optional
from fastapi import HTTPException
from persistence import InMemoryPersistence, DynamoDBPersistence
import os
from datetime import datetime, timezone


class QueueController:
    def __init__(self):
        self.queue: List[
            Dict[str, any]
        ] = []  # Each guest is a dict: {"email": str, "premium": bool}
        self.is_open = True
        self.premium_limit = 3  # Default limit, can be changed via admin
        self.one_shot_price = 5  # Default price in dollars
        self.venue_mode_enabled = False
        self.venue_capacity = 0
        self.guests_in_venue = 0
        self.ready_pool_limit = (
            0  # 0 means disabled; when >0, top N guests are considered "ready"
        )
        # persistence
        self._app_id = os.getenv("APP_ID", "default")
        table_name = os.getenv("DDB_TABLE_NAME")
        self._store = (
            DynamoDBPersistence(table_name) if table_name else InMemoryPersistence()
        )
        self._last_load_time = None
        self._load()

    def _ensure_fresh_state(self):
        """Ensure we have fresh state for each operation"""
        # Load fresh state if we haven't loaded recently or if this is a new request
        if (
            not self._last_load_time
            or (datetime.now(timezone.utc) - self._last_load_time).seconds > 5
        ):
            self._load()

    ### system status

    def get_status(self):
        self._ensure_fresh_state()

        # Check if daily reset is needed
        self.auto_daily_reset_if_needed()

        if self.ready_pool_limit and self.ready_pool_limit > 0:
            ready_count = min(self.ready_pool_limit, len(self.queue))
        else:
            ready_count = 1 if len(self.queue) > 0 else 0

        queue_with_location: List[Dict[str, any]] = []
        for index, guest in enumerate(self.queue):
            queue_with_location.append(
                {
                    "email": guest.get("email"),
                    "premium": guest.get("premium", False),
                    "guest_location": "ready" if index < ready_count else "in queue",
                }
            )

        return {
            "is_open": self.is_open,
            "queue": queue_with_location,
            "premium_limit": self.premium_limit,
            "one_shot_price": self.one_shot_price,
            "venue_mode_enabled": self.venue_mode_enabled,
            "venue_capacity": self.venue_capacity,
            "guests_in_venue": self.guests_in_venue,
            "ready_pool_limit": self.ready_pool_limit,
            "ready_pool": self.get_ready_pool(),
        }

    ### joining and leaving the queue

    def join_queue(self, email: str):
        if not self.is_open:
            raise HTTPException(status_code=403, detail="Queue is closed.")
        if not any(g["email"] == email for g in self.queue):
            self.queue.append({"email": email, "premium": False})
            self._save()

    def join_premium_queue(self, email: str):
        if not self.is_open:
            raise HTTPException(status_code=403, detail="Queue is closed.")

        # Remove guest if already in queue
        existing_guest = None
        for i, guest in enumerate(self.queue):
            if guest["email"] == email:
                if guest.get("premium"):
                    raise HTTPException(
                        status_code=400, detail="Guest already in premium queue."
                    )
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

        self.queue.insert(insert_index, {"email": email, "premium": True})
        self._save()

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
            self._save()

    def leave_queue(self, email: str):
        for i, guest in enumerate(self.queue):
            if guest["email"] == email:
                self.queue.pop(i)
                if self.venue_mode_enabled:
                    self.increment_guests_in_venue()
                self._save()
                return

    ### basic queue settings

    def open_queue(self):
        self.is_open = True

    def close_queue(self):
        self.is_open = False

    def reset_queue(self):
        self.queue.clear()
        self._save()

    def mock_guests(self, count: int):
        for i in range(count):
            self.queue.append({"email": f"mock{i}@example.com", "premium": False})

    ### premuim queue bits

    def set_premium_limit(self, limit: int):
        self.premium_limit = limit
        self._save()

    def set_one_shot_price(self, price: int):
        self.one_shot_price = price
        self._save()

    def is_premium(self, email: str) -> bool:
        for guest in self.queue:
            if guest["email"] == email:
                return guest["premium"]
        raise HTTPException(status_code=404, detail="Guest not in queue.")

    ### venue mode functionality

    def set_venue_mode(self, enabled: bool):
        self._ensure_fresh_state()
        # Only change venue mode, don't affect queue contents
        self.venue_mode_enabled = enabled
        # Reset venue guest count when mode changes
        if not enabled:
            self.guests_in_venue = 0
        self._save()

    def set_venue_capacity(self, capacity: int):
        self._ensure_fresh_state()
        self.venue_capacity = capacity
        self._save()

    def is_venue_full(self) -> bool:
        return (
            self.guests_in_venue >= self.venue_capacity
            if self.venue_mode_enabled
            else False
        )

    def increment_guests_in_venue(self):
        if self.venue_mode_enabled and self.guests_in_venue < self.venue_capacity:
            self.guests_in_venue += 1
        else:
            raise HTTPException(status_code=403, detail="Venue is full.")
        self._save()

    def decrement_guests_in_venue(self):
        if self.venue_mode_enabled and self.guests_in_venue > 0:
            self.guests_in_venue -= 1
        else:
            raise HTTPException(status_code=400, detail="No guests in venue to remove.")
        self._save()

    ### daily reset functionality

    def daily_reset(self):
        """Reset queue for new business day while preserving configuration"""
        self._ensure_fresh_state()

        # Clear queue contents but preserve configuration
        old_queue = self.queue.copy()
        self.queue.clear()
        self.guests_in_venue = 0

        # Save the reset state
        self._save()

        print(
            f"Daily reset completed at {datetime.now(timezone.utc)}. Cleared {len(old_queue)} guests from queue."
        )
        return {
            "message": f"Daily reset completed. Cleared {len(old_queue)} guests from queue.",
            "guests_cleared": len(old_queue),
            "reset_time": datetime.now(timezone.utc).isoformat(),
        }

    def should_daily_reset(self) -> bool:
        """Check if daily reset should be performed based on business hours"""
        # Default to 6 AM UTC (adjustable via config)
        reset_hour = 9
        current_time = datetime.now(timezone.utc)

        # Check if it's around reset time (within 1 hour)
        if current_time.hour == reset_hour:
            return True
        return False

    def auto_daily_reset_if_needed(self):
        """Automatically perform daily reset if needed"""
        if self.should_daily_reset():
            # Check if we've already reset today
            today = datetime.now(timezone.utc).date()
            if not hasattr(self, "_last_reset_date") or self._last_reset_date != today:
                self.daily_reset()
                self._last_reset_date = today

    ### ready pool functionality

    def set_ready_pool_limit(self, limit: int):
        if limit < 0:
            raise HTTPException(
                status_code=400, detail="Ready pool limit must be non-negative."
            )
        self.ready_pool_limit = limit
        self._save()

    def get_ready_pool(self) -> List[Dict[str, any]]:
        if self.ready_pool_limit and self.ready_pool_limit > 0:
            return self.queue[: min(self.ready_pool_limit, len(self.queue))]
        return []

    def scan_guest(self, email: str):
        if self.venue_mode_enabled and self.is_venue_full():
            raise HTTPException(status_code=403, detail="Venue is full.")
        for i, guest in enumerate(self.queue):
            if guest["email"] == email:
                # Enforce readiness
                if self.ready_pool_limit and self.ready_pool_limit > 0:
                    if i >= min(self.ready_pool_limit, len(self.queue)):
                        raise HTTPException(
                            status_code=403, detail="Guest is not in the ready pool."
                        )
                else:
                    if i != 0:
                        raise HTTPException(
                            status_code=403, detail="Guest is not ready."
                        )

                self.queue.pop(i)
                if self.venue_mode_enabled:
                    self.increment_guests_in_venue()
                self._save()
                return
        raise HTTPException(status_code=404, detail="Guest not in queue.")

    def _serialize(self) -> Dict[str, any]:
        return {
            "queue": self.queue,
            "is_open": self.is_open,
            "premium_limit": self.premium_limit,
            "one_shot_price": self.one_shot_price,
            "venue_mode_enabled": self.venue_mode_enabled,
            "venue_capacity": self.venue_capacity,
            "guests_in_venue": self.guests_in_venue,
            "ready_pool_limit": self.ready_pool_limit,
        }

    def _hydrate(self, state: Dict[str, any]):
        self.queue = state.get("queue", [])
        self.is_open = state.get("is_open", True)
        self.premium_limit = state.get("premium_limit", 0)
        self.one_shot_price = state.get("one_shot_price", 5)
        self.venue_mode_enabled = state.get("venue_mode_enabled", False)
        self.venue_capacity = state.get("venue_capacity", 0)
        self.guests_in_venue = state.get("guests_in_venue", 0)
        self.ready_pool_limit = state.get("ready_pool_limit", 0)

    def _load(self):
        try:
            state = self._store.load_state(self._app_id)
            if state:
                self._hydrate(state)
            self._last_load_time = datetime.now(timezone.utc)
        except Exception:
            # best-effort load; remain with defaults on error
            pass

    def _save(self):
        try:
            self._store.save_state(self._app_id, self._serialize())
        except Exception:
            # best-effort save; ignore errors in stateless/local mode
            pass
