import json
import os
from typing import Optional, Dict, Any
from datetime import datetime, timezone


class InMemoryPersistence:
    def __init__(self):
        self._state: Optional[Dict[str, Any]] = None

    def load_state(self, app_id: str) -> Optional[Dict[str, Any]]:
        return self._state

    def save_state(self, app_id: str, state: Dict[str, Any]) -> None:
        # Deep copy to prevent reference issues
        self._state = json.loads(json.dumps(state))


class DynamoDBPersistence:
    def __init__(self, table_name: str):
        import boto3  # type: ignore

        self._table_name = table_name
        self._ddb = boto3.resource("dynamodb")
        self._table = self._ddb.Table(table_name)

    def load_state(self, app_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self._table.get_item(Key={"pk": f"queue_state#{app_id}"})
            item = response.get("Item")
            if not item:
                return None

            state_json = item.get("state_json", "{}")
            if not state_json:
                return None

            state = json.loads(state_json)

            # Validate state structure
            if not self._validate_state(state):
                print(f"Warning: Invalid state loaded for {app_id}, using defaults")
                return None

            return state

        except Exception as e:
            print(f"Error loading state for {app_id}: {e}")
            return None

    def save_state(self, app_id: str, state: Dict[str, Any]) -> None:
        try:
            # Validate state before saving
            if not self._validate_state(state):
                print(f"Warning: Invalid state not saved for {app_id}")
                return

            # Add metadata for debugging
            state_with_metadata = {
                "state_json": json.dumps(state),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "app_id": app_id,
            }

            self._table.put_item(
                Item={"pk": f"queue_state#{app_id}", **state_with_metadata}
            )

        except Exception as e:
            print(f"Error saving state for {app_id}: {e}")

    def _validate_state(self, state: Dict[str, Any]) -> bool:
        """Validate that the state has the expected structure"""
        required_keys = [
            "queue",
            "is_open",
            "premium_limit",
            "one_shot_price",
            "venue_mode_enabled",
            "venue_capacity",
            "guests_in_venue",
            "ready_pool_limit",
        ]

        # Check all required keys exist
        if not all(key in state for key in required_keys):
            return False

        # Validate queue is a list
        if not isinstance(state.get("queue"), list):
            return False

        # Validate other fields have correct types
        if not isinstance(state.get("is_open"), bool):
            return False

        if not isinstance(state.get("premium_limit"), int):
            return False

        if not isinstance(state.get("one_shot_price"), (int, float)):
            return False

        if not isinstance(state.get("venue_mode_enabled"), bool):
            return False

        if not isinstance(state.get("venue_capacity"), int):
            return False

        if not isinstance(state.get("guests_in_venue"), int):
            return False

        if not isinstance(state.get("ready_pool_limit"), int):
            return False

        return True
