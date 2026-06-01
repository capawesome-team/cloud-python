from __future__ import annotations

import httpx
import respx

from capawesome_cloud import CapawesomeCloud
from capawesome_cloud._http import DEFAULT_BASE_URL as BASE_URL


@respx.mock
def test_paginator_walks_all_pages(client: CapawesomeCloud) -> None:
    def responder(request: httpx.Request) -> httpx.Response:
        offset = int(request.url.params.get("offset", "0"))
        if offset == 0:
            items = [{"id": f"a{i}"} for i in range(2)]
        elif offset == 2:
            items = [{"id": "a2"}]  # short page -> last
        else:
            items = []
        return httpx.Response(200, json=items)

    respx.get(f"{BASE_URL}/v1/apps").mock(side_effect=responder)

    ids = [app.id for app in client.apps.list(page_size=2)]
    assert ids == ["a0", "a1", "a2"]


@respx.mock
def test_paginator_stops_on_empty_page(client: CapawesomeCloud) -> None:
    def responder(request: httpx.Request) -> httpx.Response:
        offset = int(request.url.params.get("offset", "0"))
        # Exactly page_size on first page, then empty -> must stop.
        items = [{"id": "a0"}, {"id": "a1"}] if offset == 0 else []
        return httpx.Response(200, json=items)

    route = respx.get(f"{BASE_URL}/v1/apps").mock(side_effect=responder)

    ids = [app.id for app in client.apps.list(page_size=2)]
    assert ids == ["a0", "a1"]
    assert route.call_count == 2


@respx.mock
def test_list_page_single_request(client: CapawesomeCloud) -> None:
    route = respx.get(f"{BASE_URL}/v1/apps").mock(
        return_value=httpx.Response(200, json=[{"id": "a0"}, {"id": "a1"}])
    )
    apps = client.apps.list_page(limit=2)
    assert [a.id for a in apps] == ["a0", "a1"]
    assert route.call_count == 1
    assert route.calls.last.request.url.params["limit"] == "2"
