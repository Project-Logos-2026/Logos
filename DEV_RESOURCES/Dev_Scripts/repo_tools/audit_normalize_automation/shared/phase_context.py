from pathlib import Path
from datetime import datetime, timezone


def reports_root() -> Path:
	return Path("_Reports/Audit_Normalize")


def timestamp() -> str:
	return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
