# Examples

Runnable scripts to try the SDK against the live Capawesome Cloud API.

## Prerequisites

- Python 3.9 or later
- The SDK installed — from the repository root run `pip install -e .` (or `pip install capawesome-cloud`)
- An API token from the [Capawesome Cloud Console](https://console.cloud.capawesome.io/settings/tokens)

## Running

Set your token, then run any script with Python:

```bash
export CAPAWESOME_CLOUD_TOKEN=<your-token>
python examples/list_apps.py <organization-id>
```

Each script takes the id it operates on as its argument (see the table below).

| Script                     | Description                                                          | Argument            |
| -------------------------- | ------------------------------------------------------------------- | ------------------- |
| `list_apps.py`             | Lists all apps of an organization.                                  | `<organization-id>` |
| `manage_live_updates.py`   | Creates a live update channel, pauses/resumes it, and lists devices. | `<app-id>`          |
| `trigger_native_build.py`  | Triggers a native build, waits for it, and downloads its artifacts. | `<app-id>`          |
| `error_handling.py`        | Shows how `CapawesomeCloudError` is raised for a failed request.    | —                   |

> `list_apps.py` and `error_handling.py` are read-only. `manage_live_updates.py` and `trigger_native_build.py` perform real, billable operations (creating a channel, starting a native build).

> These scripts import the installed `capawesome_cloud` package. An editable install (`pip install -e .`) runs them against the local source, so changes are picked up without reinstalling.
