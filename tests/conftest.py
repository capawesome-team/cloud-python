from __future__ import annotations

import pytest

from capawesome_cloud import CapawesomeCloud
from capawesome_cloud._http import DEFAULT_BASE_URL

BASE_URL = DEFAULT_BASE_URL


@pytest.fixture
def client() -> CapawesomeCloud:
    return CapawesomeCloud(
        token="test-token",
        max_retries=0,
        backoff_factor=0.0,
    )
