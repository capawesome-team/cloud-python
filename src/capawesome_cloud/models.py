"""Response models.

The Capawesome Cloud API does not publish response schemas and is still evolving,
so these models intentionally declare only the **important, stable** fields. Every
model is configured with ``extra="allow"``: any additional (including internal)
fields the API returns are preserved and accessible as attributes, but they are
**not part of the SDK's public contract** and may change or disappear without
notice -- do not rely on them.

App-scoped resources are prefixed with ``App`` (``AppChannel``, ``AppWebhook``,
...) to mirror the API's entity names and avoid clashes with organization-scoped
resources. Field names are exposed in Pythonic
``snake_case`` while the API's ``camelCase`` keys are accepted transparently.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

__all__ = [
    "CapawesomeModel",
    "App",
    "AppChannel",
    "AppBuild",
    "AppBuildArtifact",
    "AppBuildSource",
    "AppDeployment",
    "AppDestination",
    "AppDevice",
    "AppEnvironment",
    "AppEnvironmentVariable",
    "AppEnvironmentSecret",
    "AppCertificate",
    "AppWebhook",
    "AppAutomation",
    "AppConfiguration",
    "AppGitRepository",
    "Job",
    "JobFailureSummary",
    "JobLog",
    "User",
    "Organization",
    "OrganizationMember",
    "OrganizationInvitation",
    "LicenseKey",
    "Team",
    "TeamApp",
    "TeamMember",
    "GitConnection",
    "GitRepository",
    "GitNamespace",
]


class CapawesomeModel(BaseModel):
    """Base model: maps ``camelCase`` API keys and keeps unknown fields."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
    )

    id: Optional[str] = None


class App(CapawesomeModel):
    name: Optional[str] = None
    type: Optional[str] = None
    build_stack: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppChannel(CapawesomeModel):
    name: Optional[str] = None
    app_id: Optional[str] = None
    paused_at: Optional[datetime] = None
    protected_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppBuild(CapawesomeModel):
    number_as_string: Optional[str] = None
    platform: Optional[str] = None
    type: Optional[str] = None
    display_name: Optional[str] = None
    app_id: Optional[str] = None
    job_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppBuildArtifact(CapawesomeModel):
    type: Optional[str] = None
    status: Optional[str] = None
    form_factor: Optional[str] = None
    app_build_id: Optional[str] = None
    total_size_in_bytes: Optional[int] = None
    download_url: Optional[str] = None
    created_at: Optional[datetime] = None


class AppBuildSource(CapawesomeModel):
    type: Optional[str] = None
    status: Optional[str] = None
    file_url: Optional[str] = None
    file_size_in_bytes: Optional[int] = None
    created_at: Optional[datetime] = None


class AppDeployment(CapawesomeModel):
    app_build_id: Optional[str] = None
    app_channel_id: Optional[str] = None
    app_destination_id: Optional[str] = None
    app_id: Optional[str] = None
    job_id: Optional[str] = None
    rollout_percentage: Optional[float] = None
    release_notes: Optional[dict[str, str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppDestination(CapawesomeModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    type: Optional[str] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppDevice(CapawesomeModel):
    app_id: Optional[str] = None
    app_version_code: Optional[str] = None
    app_version_name: Optional[str] = None
    os_version: Optional[str] = None
    plugin_version: Optional[str] = None
    custom_id: Optional[str] = None
    last_seen_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppEnvironment(CapawesomeModel):
    name: Optional[str] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppEnvironmentVariable(CapawesomeModel):
    key: Optional[str] = None
    value: Optional[str] = None
    app_environment_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppEnvironmentSecret(CapawesomeModel):
    # The secret ``value`` is encrypted and not returned by the API.
    key: Optional[str] = None
    app_environment_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppCertificate(CapawesomeModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    type: Optional[str] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppWebhook(CapawesomeModel):
    name: Optional[str] = None
    url: Optional[str] = None
    events: Optional[list[str]] = None
    format: Optional[str] = None
    enabled: Optional[bool] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppAutomation(CapawesomeModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    trigger_type: Optional[str] = None
    enabled: Optional[bool] = None
    app_channel_ids: Optional[list[str]] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppConfiguration(CapawesomeModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    package_name: Optional[str] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppGitRepository(CapawesomeModel):
    name: Optional[str] = None
    path: Optional[str] = None
    provider: Optional[str] = None
    web_url: Optional[str] = None
    app_id: Optional[str] = None
    git_connection_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Job(CapawesomeModel):
    status: Optional[str] = None
    app_id: Optional[str] = None
    app_build_id: Optional[str] = None
    app_deployment_id: Optional[str] = None
    finished_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class JobLog(CapawesomeModel):
    job_id: Optional[str] = None
    number: Optional[int] = None
    payload: Optional[str] = None
    timestamp: Optional[datetime] = None


class JobFailureSummary(CapawesomeModel):
    summary: Optional[str] = None


class User(CapawesomeModel):
    email: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Organization(CapawesomeModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrganizationMember(CapawesomeModel):
    role: Optional[str] = None
    user: Optional[User] = None
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrganizationInvitation(CapawesomeModel):
    email: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    organization_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LicenseKey(CapawesomeModel):
    name: Optional[str] = None
    key: Optional[str] = None
    organization_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class Team(CapawesomeModel):
    name: Optional[str] = None
    description: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TeamApp(CapawesomeModel):
    team_id: Optional[str] = None
    app_id: Optional[str] = None
    created_at: Optional[datetime] = None


class TeamMember(CapawesomeModel):
    team_id: Optional[str] = None
    member_id: Optional[str] = None
    created_at: Optional[datetime] = None


class GitConnection(CapawesomeModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    auth_kind: Optional[str] = None
    base_url: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GitRepository(CapawesomeModel):
    name: Optional[str] = None
    namespace: Optional[str] = None
    path: Optional[str] = None
    private: Optional[bool] = None
    web_url: Optional[str] = None
    default_branch: Optional[str] = None


class GitNamespace(CapawesomeModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    kind: Optional[str] = None
