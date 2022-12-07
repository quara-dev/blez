from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def bluez_data() -> dict[str, dict[str, dict[str, Any]]]:
    """Load default Bluez data."""
    return json.loads(
        Path(__file__).parent.joinpath("data/get_all_objects.json").read_bytes()
    )
