from typing import List
from datetime import datetime, timezone

class JwtPayload:
    def __init__(self, sub: str, role: List[str], exp: str, iat: str):
        self.sub = sub
        self.role = role
        self.exp = self._convert_to_utc_datetime(exp)
        self.iat = self._convert_to_utc_datetime(iat)

    @staticmethod
    def _convert_to_utc_datetime(timestamp: str) -> datetime:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)

    def __repr__(self):
        return f"JwtPayload(sub={self.sub}, role={self.role}, exp={self.exp}, iat={self.iat})"
