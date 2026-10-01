"""Capawesome Cloud Python SDK.

A typed, synchronous client for the Capawesome Cloud API.
"""

from ._version import __version__
from .client import CapawesomeCloud
from .exceptions import (
    APIConnectionError,
    APITimeoutError,
    CapawesomeCloudError,
)
from .models import (
    App,
    AppAutomation,
    AppBuild,
    AppBuildArtifact,
    AppBuildSource,
    AppCertificate,
    AppChannel,
    AppConfiguration,
    AppDeployment,
    AppDestination,
    AppDevice,
    AppEnvironment,
    AppEnvironmentSecret,
    AppEnvironmentVariable,
    AppGitRepository,
    AppWebhook,
    CapawesomeModel,
    GitConnection,
    GitNamespace,
    GitRepository,
    Job,
    JobFailureSummary,
    JobLog,
    LicenseKey,
    Organization,
    OrganizationInvitation,
    OrganizationMember,
    Team,
    TeamApp,
    TeamMember,
    User,
)
from .resources.jobs import JobTimeoutError

__all__ = [
    "__version__",
    "CapawesomeCloud",
    # Exceptions
    "CapawesomeCloudError",
    "APIConnectionError",
    "APITimeoutError",
    "JobTimeoutError",
    # Models
    "CapawesomeModel",
    "App",
    "AppAutomation",
    "AppBuild",
    "AppBuildArtifact",
    "AppBuildSource",
    "AppCertificate",
    "AppChannel",
    "AppConfiguration",
    "AppDeployment",
    "AppDestination",
    "AppDevice",
    "AppEnvironment",
    "AppEnvironmentSecret",
    "AppEnvironmentVariable",
    "AppGitRepository",
    "AppWebhook",
    "GitConnection",
    "GitNamespace",
    "GitRepository",
    "Job",
    "JobFailureSummary",
    "JobLog",
    "LicenseKey",
    "Organization",
    "OrganizationInvitation",
    "OrganizationMember",
    "Team",
    "TeamApp",
    "TeamMember",
    "User",
]
