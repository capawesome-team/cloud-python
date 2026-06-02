"""List all apps of an organization.

Run with:
    CAPAWESOME_CLOUD_TOKEN=cap_... python examples/list_apps.py <organization_id>
"""

from __future__ import annotations

import sys

from capawesome_cloud import CapawesomeCloud


def main(organization_id: str) -> None:
    with CapawesomeCloud() as client:
        count = 0
        # `list` transparently pages through every app of the organization.
        for app in client.apps.list(organization_id=organization_id):
            count += 1
            print(f"{app.id}  {app.type or '-':<10}  {app.name}")
        print(f"\n{count} app(s) found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: list_apps.py <organization_id>")
    main(sys.argv[1])
