from datetime import datetime
from typing import Any

cache: dict[str, tuple[datetime, Any]] = {}