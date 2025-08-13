from __future__ import annotations

from typing import Dict, Any
import uuid


class MemoryStore:
    def __init__(self) -> None:
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, session_id: str | None) -> str:
        if session_id and session_id in self._sessions:
            return session_id
        new_id = str(uuid.uuid4())
        self._sessions[new_id] = self._new_state()
        return new_id

    def get_state(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self._sessions:
            self._sessions[session_id] = self._new_state()
        return self._sessions[session_id]

    def reset(self, session_id: str) -> None:
        self._sessions[session_id] = self._new_state()

    def _new_state(self) -> Dict[str, Any]:
        return {
            "stage": "greeting",
            "data": {
                "height_m": None,
                "length_m": None,
                "cell_mm": None,
                "wire_mm": None,
                "coating": None,
                "shipping_distance_km": None,
                "contact_name": None,
                "contact_phone": None
            },
            "history": []
        }


memory_store = MemoryStore()