from __future__ import annotations

import httpx
import pytest
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
def test_app_update_sends_build_stack(client: CapawesomeCloud) -> None:
    route = respx.patch(f"{BASE_URL}/v1/apps/app1").mock(
        return_value=httpx.Response(200, json={"id": "app1", "buildStack": "macos-tahoe"})
    )
    app = client.apps.update("app1", build_stack="macos-tahoe")
    assert route.calls.last.request.read() == b'{"buildStack":"macos-tahoe"}'
    assert app.build_stack == "macos-tahoe"


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


@respx.mock
def test_deployment_sends_release_notes(client: CapawesomeCloud) -> None:
    release_notes = {"default": "Bug fixes.", "de-DE": "Fehlerbehebungen."}
    route = respx.post(f"{BASE_URL}/v1/apps/app1/deployments").mock(
        return_value=httpx.Response(201, json={"id": "dep1", "releaseNotes": release_notes})
    )
    deployment = client.apps.deployments.create(
        "app1", app_build_id="b1", app_destination_name="App Store", release_notes=release_notes
    )
    body = route.calls.last.request.read()
    assert b'"releaseNotes":{"default":"Bug fixes.","de-DE":"Fehlerbehebungen."}' in body
    assert deployment.release_notes == release_notes


@respx.mock
def test_build_sends_channel_ids_as_list(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/builds").mock(
        return_value=httpx.Response(201, json={"id": "b1"})
    )
    client.apps.builds.create("app1", app_channel_ids=("ch1", "ch2"))
    assert route.calls.last.request.read() == b'{"appChannelIds":["ch1","ch2"]}'


@respx.mock
def test_automation_create_sends_channel_ids_and_parses(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/automations").mock(
        return_value=httpx.Response(201, json={"id": "a1", "appChannelIds": ["ch1", "ch2"]})
    )
    automation = client.apps.automations.create(
        "app1", name="Web", trigger_type="branch", app_channel_ids=["ch1", "ch2"]
    )
    assert route.calls.last.request.read() == (
        b'{"name":"Web","triggerType":"branch","appChannelIds":["ch1","ch2"]}'
    )
    assert automation.app_channel_ids == ["ch1", "ch2"]


@respx.mock
def test_automation_update_clears_channels_with_empty_list(client: CapawesomeCloud) -> None:
    route = respx.patch(f"{BASE_URL}/v1/apps/app1/automations/a1").mock(
        return_value=httpx.Response(200, json={"id": "a1", "appChannelIds": []})
    )
    client.apps.automations.update("app1", "a1", app_channel_ids=[])
    assert route.calls.last.request.read() == b'{"appChannelIds":[]}'


@respx.mock
def test_destination_create_sends_type_and_new_fields(client: CapawesomeCloud) -> None:
    route = respx.post(f"{BASE_URL}/v1/apps/app1/destinations").mock(
        return_value=httpx.Response(201, json={"id": "d1", "type": "apple-app-store-connect"})
    )
    destination = client.apps.destinations.create(
        "app1",
        name="App Store",
        type="apple-app-store-connect",
        apple_submit_for_review=True,
        apple_beta_groups=["QA"],
    )
    assert route.calls.last.request.read() == (
        b'{"type":"apple-app-store-connect","name":"App Store",'
        b'"appleSubmitForReview":true,"appleBetaGroups":["QA"]}'
    )
    assert destination.type == "apple-app-store-connect"


def test_destination_update_rejects_type(client: CapawesomeCloud) -> None:
    with pytest.raises(TypeError, match="type"):
        client.apps.destinations.update("app1", "d1", type="google-play")


@respx.mock
def test_delete_by_id_ignores_name_filters(client: CapawesomeCloud) -> None:
    route = respx.delete(f"{BASE_URL}/v1/apps/app1/certificates/cert1").mock(
        return_value=httpx.Response(204)
    )
    client.apps.certificates.delete("app1", "cert1", name="Prod", platform="ios")
    assert route.calls.last.request.url.params == httpx.QueryParams()


@respx.mock
def test_delete_by_name_sends_filters(client: CapawesomeCloud) -> None:
    route = respx.delete(f"{BASE_URL}/v1/apps/app1/certificates").mock(
        return_value=httpx.Response(204)
    )
    client.apps.certificates.delete("app1", name="Prod", platform="ios")
    assert route.calls.last.request.url.params == httpx.QueryParams(
        {"platform": "ios", "name": "Prod"}
    )


def test_delete_requires_id_or_name(client: CapawesomeCloud) -> None:
    with pytest.raises(ValueError, match="id or a name"):
        client.apps.channels.delete("app1")


@respx.mock
def test_set_repository(client: CapawesomeCloud) -> None:
    route = respx.put(f"{BASE_URL}/v1/apps/app1/repository").mock(
        return_value=httpx.Response(200, json={"id": "app1"})
    )
    app = client.apps.repository.set("app1", git_connection_id="gc1", path="owner/name")
    assert route.calls.last.request.read() == b'{"gitConnectionId":"gc1","path":"owner/name"}'
    assert app.id == "app1"


@respx.mock
def test_users_me(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/users/me").mock(
        return_value=httpx.Response(200, json={"id": "u1", "email": "jane@example.com"})
    )
    assert client.users.me().email == "jane@example.com"
