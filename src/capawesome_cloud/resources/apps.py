"""Apps resource and its app-scoped sub-resources."""

from __future__ import annotations

from typing import List, Optional, Union

from .._http import HttpClient
from .._types import NOT_GIVEN, NotGiven
from ..models import App
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params
from .automations import AutomationsResource
from .build_sources import BuildSourcesResource
from .builds import BuildsResource
from .certificates import CertificatesResource
from .channels import ChannelsResource
from .configurations import ConfigurationsResource
from .deployments import DeploymentsResource
from .destinations import DestinationsResource
from .devices import DevicesResource
from .environments import EnvironmentsResource
from .repository import RepositoryResource
from .webhooks import WebhooksResource


class AppsResource(BaseResource):
    """Apps, plus all resources scoped under ``/v1/apps/{appId}/...``.

    App-scoped resources are exposed as attributes (``client.apps.channels``,
    ``client.apps.builds``, ...). Each of their methods takes ``app_id`` as the
    first argument.
    """

    _path = "/v1/apps"

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http)
        self.channels = ChannelsResource(http)
        self.builds = BuildsResource(http)
        self.build_sources = BuildSourcesResource(http)
        self.deployments = DeploymentsResource(http)
        self.destinations = DestinationsResource(http)
        self.devices = DevicesResource(http)
        self.environments = EnvironmentsResource(http)
        self.certificates = CertificatesResource(http)
        self.webhooks = WebhooksResource(http)
        self.automations = AutomationsResource(http)
        self.configurations = ConfigurationsResource(http)
        self.repository = RepositoryResource(http)

    def create(
        self,
        *,
        name: str,
        type: Union[str, NotGiven] = NOT_GIVEN,
        organization_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> App:
        """Create a new app. ``type`` is one of ``android``, ``capacitor``, ``cordova``, ``ios``."""
        body = build_body({"name": name, "type": type})
        params = build_params({"organizationId": organization_id})
        return self._request_model("POST", self._path, App, params=params, json=body)

    def list(
        self,
        *,
        organization_id: Optional[str] = None,
        name: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[App]:
        """Iterate over all apps, transparently paging through the result set."""
        params = build_params(
            {
                "organizationId": organization_id,
                "name": name,
                "query": query,
                "relations": relations,
            }
        )
        return self._paginate(self._path, App, params=params, page_size=page_size)

    def list_page(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        organization_id: Optional[str] = None,
        name: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[App]:
        """Fetch a single page of apps."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "organizationId": organization_id,
                "name": name,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._path, App, params=params)

    def get(self, app_id: str, *, relations: Optional[str] = None) -> App:
        """Retrieve a single app by id."""
        params = build_params({"relations": relations})
        return self._request_model("GET", f"{self._path}/{app_id}", App, params=params)

    def update(
        self,
        app_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        type: Union[str, NotGiven] = NOT_GIVEN,
        app_channel_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_environment_id: Union[str, None, NotGiven] = NOT_GIVEN,
        build_stack: Union[str, None, NotGiven] = NOT_GIVEN,
        app_channel_discovery_enabled: Union[bool, NotGiven] = NOT_GIVEN,
        next_app_build_number: Union[int, NotGiven] = NOT_GIVEN,
    ) -> App:
        """Update an app.

        ``build_stack`` is the default stack for builds that do not specify one. Pass
        ``None`` to use the Capawesome Cloud default.
        """
        body = build_body(
            {
                "name": name,
                "type": type,
                "appChannelId": app_channel_id,
                "appEnvironmentId": app_environment_id,
                "buildStack": build_stack,
                "appChannelDiscoveryEnabled": app_channel_discovery_enabled,
                "nextAppBuildNumber": next_app_build_number,
            }
        )
        return self._request_model("PATCH", f"{self._path}/{app_id}", App, json=body)

    def delete(self, app_id: str) -> None:
        """Delete an app."""
        self._request_none("DELETE", f"{self._path}/{app_id}")

    def transfer(self, app_id: str, *, organization_id: str) -> None:
        """Transfer an app to another organization."""
        self._request_none(
            "POST",
            f"{self._path}/{app_id}/transfer",
            json={"organizationId": organization_id},
        )
