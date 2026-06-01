"""Resource clients."""

from .apps import AppsResource
from .automations import AutomationsResource
from .build_sources import BuildSourcesResource
from .builds import BuildArtifactsResource, BuildsResource
from .certificates import CertificatesResource
from .channels import ChannelsResource
from .deployments import DeploymentsResource
from .destinations import DestinationsResource
from .devices import DevicesResource
from .environments import (
    EnvironmentSecretsResource,
    EnvironmentsResource,
    EnvironmentVariablesResource,
)
from .jobs import JobsResource
from .webhooks import WebhooksResource

__all__ = [
    "AppsResource",
    "AutomationsResource",
    "BuildArtifactsResource",
    "BuildSourcesResource",
    "BuildsResource",
    "CertificatesResource",
    "ChannelsResource",
    "DeploymentsResource",
    "DestinationsResource",
    "DevicesResource",
    "EnvironmentSecretsResource",
    "EnvironmentVariablesResource",
    "EnvironmentsResource",
    "JobsResource",
    "WebhooksResource",
]
