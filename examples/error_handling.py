"""Demonstrates error handling by requesting a non-existent app.

Run with:
    CAPAWESOME_CLOUD_TOKEN=cap_... python examples/error_handling.py
"""

from __future__ import annotations

from capawesome_cloud import CapawesomeCloud, CapawesomeCloudError


def main() -> None:
    # CapawesomeCloud() reads the token from the CAPAWESOME_CLOUD_TOKEN
    # environment variable and raises if it is missing.
    with CapawesomeCloud() as client:
        try:
            client.apps.get("00000000-0000-0000-0000-000000000000")
            print("Unexpected success — the app should not exist.")
        except CapawesomeCloudError as error:
            # Non-2xx responses carry the HTTP status and the API's message.
            # (Network failures raise APIConnectionError / APITimeoutError,
            # which also derive from CapawesomeCloudError.)
            print(f"Request failed as expected: {error.status} {error.message}")


if __name__ == "__main__":
    main()
