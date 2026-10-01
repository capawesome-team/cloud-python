from __future__ import annotations

import httpx
import respx

from capawesome_cloud import CapawesomeCloud
from capawesome_cloud._http import DEFAULT_BASE_URL as BASE_URL

ORG_URL = f"{BASE_URL}/v1/organizations/org1"


@respx.mock
def test_list_organizations_is_not_paginated(client: CapawesomeCloud) -> None:
    route = respx.get(f"{BASE_URL}/v1/organizations").mock(
        return_value=httpx.Response(200, json=[{"id": "org1", "name": "Acme"}])
    )
    organizations = client.organizations.list()
    assert route.calls.last.request.url.params == httpx.QueryParams()
    assert organizations[0].name == "Acme"


@respx.mock
def test_update_organization_sends_lists_and_null(client: CapawesomeCloud) -> None:
    route = respx.patch(ORG_URL).mock(return_value=httpx.Response(200, json={"id": "org1"}))
    client.organizations.update("org1", country_allowlist=("DE", "AT"), ip_allowlist=None)
    assert route.calls.last.request.read() == b'{"countryAllowlist":["DE","AT"],"ipAllowlist":null}'


@respx.mock
def test_list_members_parses_user(client: CapawesomeCloud) -> None:
    route = respx.get(f"{ORG_URL}/members").mock(
        return_value=httpx.Response(
            200, json=[{"id": "m1", "role": "admin", "user": {"email": "jane@example.com"}}]
        )
    )
    members = client.organizations.members.list_page("org1", role="admin")
    assert route.calls.last.request.url.params["role"] == "admin"
    assert members[0].user is not None
    assert members[0].user.email == "jane@example.com"


@respx.mock
def test_create_license_key_sends_package_ids_as_list(client: CapawesomeCloud) -> None:
    route = respx.post(f"{ORG_URL}/license-keys").mock(
        return_value=httpx.Response(201, json={"id": "lk1"})
    )
    client.organizations.license_keys.create("org1", name="CI", package_ids=("p1",))
    assert route.calls.last.request.read() == b'{"name":"CI","packageIds":["p1"]}'


@respx.mock
def test_rotate_license_key(client: CapawesomeCloud) -> None:
    respx.post(f"{ORG_URL}/license-keys/lk1/rotate").mock(
        return_value=httpx.Response(200, json={"id": "lk1", "key": "new-key"})
    )
    assert client.organizations.license_keys.rotate("org1", "lk1").key == "new-key"


@respx.mock
def test_get_team_sends_relations(client: CapawesomeCloud) -> None:
    route = respx.get(f"{ORG_URL}/teams/t1").mock(
        return_value=httpx.Response(200, json={"id": "t1", "teamApps": []})
    )
    client.organizations.teams.get("org1", "t1", relations="apps,members")
    assert route.calls.last.request.url.params["relations"] == "apps,members"


@respx.mock
def test_update_team_returns_none(client: CapawesomeCloud) -> None:
    route = respx.patch(f"{ORG_URL}/teams/t1").mock(return_value=httpx.Response(204))
    assert client.organizations.teams.update("org1", "t1", description=None) is None
    assert route.calls.last.request.read() == b'{"description":null}'


@respx.mock
def test_assign_app_to_team(client: CapawesomeCloud) -> None:
    route = respx.post(f"{ORG_URL}/teams/t1/apps").mock(
        return_value=httpx.Response(201, json={"id": "ta1", "appId": "app1"})
    )
    team_app = client.organizations.teams.apps.create("org1", "t1", app_id="app1")
    assert route.calls.last.request.read() == b'{"appId":"app1"}'
    assert team_app.app_id == "app1"


@respx.mock
def test_list_git_connections_sends_boolean_filter(client: CapawesomeCloud) -> None:
    route = respx.get(f"{ORG_URL}/git-connections").mock(return_value=httpx.Response(200, json=[]))
    client.organizations.git_connections.list_page("org1", restricted=False)
    assert route.calls.last.request.url.params["restricted"] == "false"


@respx.mock
def test_list_git_repositories(client: CapawesomeCloud) -> None:
    route = respx.get(f"{ORG_URL}/git-connections/gc1/repositories").mock(
        return_value=httpx.Response(200, json=[{"id": "r1", "path": "owner/name"}])
    )
    repositories = client.organizations.git_connections.list_repositories(
        "org1", "gc1", namespace="owner"
    )
    assert route.calls.last.request.url.params["namespace"] == "owner"
    assert repositories[0].path == "owner/name"
