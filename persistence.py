import json
import os
from typing import Optional, Dict, Any


class InMemoryPersistence:
    def __init__(self):
        self._state: Optional[Dict[str, Any]] = None

    def load_state(self, app_id: str) -> Optional[Dict[str, Any]]:
        return self._state

    def save_state(self, app_id: str, state: Dict[str, Any]) -> None:
        self._state = json.loads(json.dumps(state))


class DynamoDBPersistence:
    def __init__(self, table_name: str):
        import boto3  # type: ignore

        self._table_name = table_name
        self._ddb = boto3.resource("dynamodb")
        self._table = self._ddb.Table(table_name)

    def load_state(self, app_id: str) -> Optional[Dict[str, Any]]:
        response = self._table.get_item(Key={"pk": f"queue_state#{app_id}"})
        item = response.get("Item")
        if not item:
            return None
        return json.loads(item.get("state_json", "{}"))

    def save_state(self, app_id: str, state: Dict[str, Any]) -> None:
        self._table.put_item(
            Item={
                "pk": f"queue_state#{app_id}",
                "state_json": json.dumps(state),
            }
        )
