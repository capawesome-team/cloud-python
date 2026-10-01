"""Resource clients."""

from .apps import AppsResource
from .automations import AutomationsResource
from .build_sources import BuildSourcesResource
from .builds import BuildArtifactsResource, BuildsResource
from .certificates import CertificatesResource
from .channels import ChannelsResource
from .configurations import ConfigurationsResource
from .deployments import DeploymentsResource
from .destinations import DestinationsResource
from .devices import DevicesResource
from .environments import (
    EnvironmentSecretsResource,
    EnvironmentsResource,
    EnvironmentVariablesResource,
)
from .git_connections import GitConnectionsResource
from .invitations import InvitationsResource
from .jobs import JobsResource
from .license_keys import LicenseKeysResource
from .members import MembersResource
from .organizations import OrganizationsResource
from .repository import RepositoryResource
from .teams import TeamAppsResource, TeamMembersResource, TeamsResource
from .users import UsersResource
from .webhooks import WebhooksResource

__all__ = [
    "AppsResource",
    "AutomationsResource",
    "BuildArtifactsResource",
    "BuildSourcesResource",
    "BuildsResource",
    "CertificatesResource",
    "ChannelsResource",
    "ConfigurationsResource",
    "DeploymentsResource",
    "DestinationsResource",
    "DevicesResource",
    "EnvironmentSecretsResource",
    "EnvironmentVariablesResource",
    "EnvironmentsResource",
    "GitConnectionsResource",
    "InvitationsResource",
    "JobsResource",
    "LicenseKeysResource",
    "MembersResource",
    "OrganizationsResource",
    "RepositoryResource",
    "TeamAppsResource",
    "TeamMembersResource",
    "TeamsResource",
    "UsersResource",
    "WebhooksResource",
]
