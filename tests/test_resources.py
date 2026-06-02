from __future__ import annotations

import httpx
import respx

from capawesome_cloud import CapawesomeCloud
from capawesome_cloud._http import DEFAULT_BASE_URL as BASE_URL


@respx.mock
def test_create_channel_sends_body_and_parses(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/channels").mock(
        return_value=httpx.Response(201, json={"id": "ch1", "name": "production", "appId": "app1"})
    )
    channel = client.apps.channels.create("app1", name="production", protected=True)
    assert route.calls.last.request.read() == b'{"name":"production","protected":true}'
    assert channel.id == "ch1"
    assert channel.name == "production"
    assert channel.app_id == "app1"


@respx.mock
def test_not_given_fields_are_omitted_but_none_is_sent(client: CapawesomeCloud) -> None:
    route = respx.patch(f"{BASE_URL}/v1/apps/app1/devices/dev1").mock(
        return_value=httpx.Response(200, json={"id": "dev1", "appId": "app1"})
    )
    # Explicit None must be sent (to clear the field).
    client.apps.devices.update("app1", "dev1", forced_app_channel_id=None)
    assert route.calls.last.request.read() == b'{"forcedAppChannelId":null}'


@respx.mock
def test_update_with_no_args_sends_empty_body(client: CapawesomeCloud) -> None:
    route = respx.patch(f"{BASE_URL}/v1/apps/app1/devices/dev1").mock(
        return_value=httpx.Response(200, json={"id": "dev1"})
    )
    client.apps.devices.update("app1", "dev1")
    assert route.calls.last.request.read() == b"{}"


@respx.mock
def test_pause_channel_no_content(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/channels/ch1/pause").mock(
        return_value=httpx.Response(204)
    )
    assert client.apps.channels.pause("app1", "ch1") is None
    assert route.called


@respx.mock
def test_delete_returns_none(client: CapawesomeCloud) -> None:
    respx.delete(f"{BASE_URL}/v1/apps/app1").mock(return_value=httpx.Response(204))
    assert client.apps.delete("app1") is None


@respx.mock
def test_deployment_targets_channel(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/deployments").mock(
        return_value=httpx.Response(201, json={"id": "dep1", "appBuildId": "b1"})
    )
    deployment = client.apps.deployments.create(
        "app1", app_build_id="b1", app_channel_name="production"
    )
    body = route.calls.last.request.read()
    assert b'"appBuildId":"b1"' in body
    assert b'"appChannelName":"production"' in body
    assert deployment.app_build_id == "b1"


@respx.mock
def test_artifact_download_returns_bytes(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps/app1/builds/b1/artifacts/a1/download").mock(
        return_value=httpx.Response(200, content=b"BINARY")
    )
    data = client.apps.builds.artifacts.download("app1", "b1", "a1")
    assert data == b"BINARY"


@respx.mock
def test_certificate_upload_is_multipart(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/certificates").mock(
        return_value=httpx.Response(201, json={"id": "cert1", "name": "Prod"})
    )
    cert = client.apps.certificates.create(
        "app1", name="Prod", file=b"KEYSTORE", file_name="keystore.jks", type="production"
    )
    request = route.calls.last.request
    assert request.headers["content-type"].startswith("multipart/form-data")
    body = request.read()
    assert b"KEYSTORE" in body
    assert b'name="name"' in body
    assert cert.id == "cert1"
