"""Capawesome Cloud Python SDK.

A typed, synchronous client for the Capawesome Cloud API.
"""

from ._version import __version__
from .client import CapawesomeCloud
from .exceptions import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    CapawesomeCloudError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from .models import (
    App,
    AppAutomation,
    AppBuild,
    AppBuildArtifact,
    AppBuildSource,
    AppCertificate,
    AppChannel,
    AppDeployment,
    AppDestination,
    AppDevice,
    AppEnvironment,
    AppEnvironmentSecret,
    AppEnvironmentVariable,
    AppWebhook,
    CapawesomeModel,
    Job,
)
from .resources.jobs import JobTimeoutError

__all__ = [
    "__version__",
    "CapawesomeCloud",
    # Exceptions
    "CapawesomeCloudError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
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
    "AppDeployment",
    "AppDestination",
    "AppDevice",
    "AppEnvironment",
    "AppEnvironmentSecret",
    "AppEnvironmentVariable",
    "AppWebhook",
    "Job",
]
