from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class SessionInfo:
    id: str
    user_id: int
    username: str
    device: str
    ip: str
    created_at: str
    last_active_at: str


_sessions: List[SessionInfo] = []


def list_sessions(user_id: Optional[int] = None) -> List[SessionInfo]:
    if user_id is None:
        return list(_sessions)
    return [s for s in _sessions if s.user_id == user_id]


def add_session(user_id: int, username: str, device: str, ip: str) -> SessionInfo:
    sid = f"s{int(datetime.utcnow().timestamp()*1000)}_{user_id}"
    now = datetime.utcnow().isoformat()
    s = SessionInfo(id=sid, user_id=user_id, username=username, device=device, ip=ip, created_at=now, last_active_at=now)
    _sessions.append(s)
    return s


def revoke_session(session_id: str) -> bool:
    global _sessions
    before = len(_sessions)
    _sessions = [s for s in _sessions if s.id != session_id]
    return len(_sessions) < before