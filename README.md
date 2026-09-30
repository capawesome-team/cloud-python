# capawesome-cloud

[![PyPI version](https://img.shields.io/pypi/v/capawesome-cloud)](https://pypi.org/project/capawesome-cloud/)
[![PyPI downloads](https://img.shields.io/pypi/dm/capawesome-cloud)](https://pypi.org/project/capawesome-cloud/)
[![license](https://img.shields.io/pypi/l/capawesome-cloud)](https://github.com/capawesome-team/cloud-python/blob/main/LICENSE)

Python SDK for the [Capawesome Cloud](https://capawesome.io/cloud/) API.

It provides a fully typed, synchronous interface for managing apps, live update channels and deployments, native builds, app store destinations, and more.

> **Note:** The Capawesome Cloud API is still in development and may change without notice. Response types intentionally expose only the most relevant properties to minimize breaking changes.

## SDKs

Official SDKs for the Capawesome Cloud API:

| Language | Package                                                                        | Repository                                                      |
| -------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Node.js  | [`@capawesome/cloud-sdk`](https://www.npmjs.com/package/@capawesome/cloud-sdk) | [cloud-node](https://github.com/capawesome-team/cloud-node)     |
| Python   | [`capawesome-cloud`](https://pypi.org/project/capawesome-cloud/)               | [cloud-python](https://github.com/capawesome-team/cloud-python) |

## Installation

```bash
pip install capawesome-cloud
```

**Requirements:** Python 3.9 or later.

## Getting started

Create an API token in the [Capawesome Cloud Console](https://console.cloud.capawesome.io/settings/tokens) and pass it to the client (or set the `CAPAWESOME_CLOUD_TOKEN` environment variable, with `CAPAWESOME_TOKEN` accepted as a fallback):

```python
from capawesome_cloud import CapawesomeCloud

client = CapawesomeCloud(token="cap_...")

for app in client.apps.list():
    print(app.id, app.name)
```

The client holds a connection pool, so reuse a single instance. Use it as a context manager (or call `client.close()`) to release connections when done:

```python
with CapawesomeCloud(token="cap_...") as client:
    ...
```

### Configuration

| Option           | Type            | Default                           | Description                                                |
| ---------------- | --------------- | --------------------------------- | ---------------------------------------------------------- |
| `token`          | `str`           | `CAPAWESOME_CLOUD_TOKEN` env var  | API token used to authenticate.                            |
| `base_url`       | `str`           | `https://api.cloud.capawesome.io` | Base URL of the API (for self-hosting/testing).            |
| `timeout`        | `float`         | `30.0`                            | Request timeout in seconds.                                |
| `max_retries`    | `int`           | `2`                               | Retries with exponential backoff. `429` is retried for any request; network/`5xx` failures are retried only for idempotent methods (GET/PUT/DELETE), never `POST`/`PATCH`. |
| `backoff_factor` | `float`         | `0.5`                             | Base delay for the retry backoff.                          |
| `http_client`    | `httpx.Client`  | `None`                            | Bring your own pre-configured `httpx.Client`.              |

## Usage

Resources mirror the API's path hierarchy. App-scoped resources are nested under `client.apps.*`; organization-scoped resources are on the client directly (e.g. `client.jobs`). Every app-scoped method takes `app_id` as its first argument.

### Apps

```python
apps = client.apps.list()
app = client.apps.get(app_id)
created = client.apps.create(name="My App", type="capacitor")
client.apps.update(app_id, name="Renamed App")
client.apps.delete(app_id)
```

### Live updates

```python
# Create a channel
channel = client.apps.channels.create(app_id, name="production")

# Pause / resume a channel
client.apps.channels.pause(app_id, channel.id)
client.apps.channels.resume(app_id, channel.id)
```

### Deployments

Promote a build to a channel (live updates) or a destination (app store publishing):

```python
# Roll out a live update to half of the devices on a channel
client.apps.deployments.create(
    app_id,
    app_build_id=app_build_id,
    app_channel_name="production",
    rollout_percentage=0.5,
)

# Publish a native build to an app store with localized release notes
client.apps.deployments.create(
    app_id,
    app_build_id=app_build_id,
    app_destination_name="Google Play",
    release_notes={
        "default": "Bug fixes and performance improvements.",
        "de-DE": "Fehlerbehebungen und Leistungsverbesserungen.",
    },
)
```

### Native builds

```python
build = client.apps.builds.create(app_id, platform="ios", git_ref="main")

# Poll the job that processes the build until it finishes
job = client.jobs.wait(build.job_id)
print(job.status)

logs = client.jobs.logs(job.id)

# Explain a failure
if job.status == "failed":
    print(client.jobs.get_failure_summary(job.id).summary)
```

#### Build artifacts

Binary downloads return `bytes`:

```python
data = client.apps.builds.artifacts.download(app_id, build_id, artifact_id)
with open("artifact.ipa", "wb") as file:
    file.write(data)
```

You can also obtain a signed, time-limited download URL:

```python
result = client.apps.builds.artifacts.get_download_url(app_id, build_id, artifact_id)
print(result["url"])
```

#### Certificates

`file` may be a path, raw `bytes`, or an open binary file object:

```python
import os

certificate = client.apps.certificates.create(
    app_id,
    name="Distribution Certificate",
    platform="ios",
    type="production",
    file="distribution.p12",
    password=os.environ["CERT_PASSWORD"],
)
```

#### Environments, secrets & variables

```python
environment = client.apps.environments.create(app_id, name="production")

client.apps.environments.secrets.create(
    app_id,
    environment.id,
    key="API_KEY",
    value=os.environ["API_KEY"],
)

client.apps.environments.variables.create(
    app_id,
    environment.id,
    key="API_URL",
    value="https://api.example.com",
)
```

### Pagination

List methods return an iterator that lazily pages through **all** results:

```python
for device in client.apps.devices.list(app_id):
    print(device.id, device.app_version_name)

# Collect everything into a list
channels = client.apps.channels.list(app_id).to_list()
```

To fetch a single page (for manual offset control), use `list_page()`:

```python
page = client.apps.channels.list_page(app_id, limit=20, offset=0)
```

### Responses

Responses are typed [Pydantic](https://docs.pydantic.dev) models. App-scoped models are prefixed with `App` (`AppChannel`, `AppWebhook`, `AppBuild`, ...) to match the API's entity names. Only the most relevant fields are declared; any additional fields the API returns are still accessible (e.g. via `model_dump()`) but are **not part of the public contract** and should not be relied upon.

```python
channel = client.apps.channels.get(app_id, channel_id)
print(channel.name, channel.created_at)   # documented fields
print(channel.model_dump())               # full raw payload, incl. extra fields
```

### Clearing fields

Update methods only send the arguments you pass. To **clear** a nullable field, pass `None`; omit the argument to leave it unchanged.

```python
# Pin a device to a channel
client.apps.devices.update(app_id, device_id, forced_app_channel_id="ch_123")

# Unpin it again (sends null)
client.apps.devices.update(app_id, device_id, forced_app_channel_id=None)
```

## Available resources

| Resource                            | Description                                         |
| ----------------------------------- | --------------------------------------------------- |
| `client.apps`                       | Create, read, update, delete and transfer apps.     |
| `client.apps.channels`              | Manage live update channels (incl. pause/resume).   |
| `client.apps.deployments`           | Promote builds to channels or destinations.         |
| `client.apps.builds`                | Trigger and manage native builds.                   |
| `client.apps.builds.artifacts`      | List and download build artifacts.                  |
| `client.apps.build_sources`         | Register and download native build sources.         |
| `client.apps.certificates`          | Manage signing certificates.                        |
| `client.apps.destinations`          | Manage app store publishing destinations.           |
| `client.apps.environments`          | Manage environments, secrets and variables.         |
| `client.apps.automations`           | Manage build automations.                           |
| `client.apps.devices`               | Manage registered devices.                          |
| `client.apps.webhooks`              | Manage app webhooks.                                |
| `client.apps.configurations`        | Manage native app configurations.                   |
| `client.apps.repository`            | Link an app to a Git repository.                    |
| `client.jobs`                       | Inspect background jobs and their logs.             |
| `client.users`                      | Access the authenticated user.                      |

## Error handling

Any non-2xx response is raised as a `CapawesomeCloudError`, carrying the HTTP `status`, the `message` from the API, and the raw `body`:

```python
from capawesome_cloud import CapawesomeCloud, CapawesomeCloudError

client = CapawesomeCloud(token="cap_...")

try:
    client.apps.get("unknown")
except CapawesomeCloudError as error:
    print(error.status)       # 404
    print(error.status_text)  # "Not Found"
    print(error.message)      # "App not found."
    print(error.body)         # {"message": "App not found."}
```

Network failures raise `APIConnectionError` / `APITimeoutError`, which also derive from `CapawesomeCloudError` — so a single `except CapawesomeCloudError` catches every error the SDK can raise. For those, `status` is `None`.

## Development

### Setup

Clone the repository, then create a virtual environment and install the package with its development dependencies:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org), enforced by [Commitizen](https://commitizen-tools.github.io/commitizen/) — run `cz commit` for a guided prompt. Common commands during development:

| Command                                    | Description                            |
| ------------------------------------------ | -------------------------------------- |
| `python -m build`                          | Build the package into `dist/`.        |
| `ruff check src tests examples`            | Run the linter.                        |
| `ruff format src tests examples`           | Auto-format the code.                  |
| `ruff format --check src tests examples`   | Check formatting without writing.      |
| `mypy`                                     | Type-check the package.                |
| `cz commit`                                | Create a Conventional Commit.          |

### Testing

Tests are written with [pytest](https://docs.pytest.org) and live in the `tests/` directory. HTTP is mocked with [RESPX](https://lundberg.github.io/respx/), so the suite makes no network calls:

```bash
pytest                          # run the suite once
pytest --cov=capawesome_cloud   # run with a coverage report
```

### Publishing

Releases are driven by [Commitizen](https://commitizen-tools.github.io/commitizen/), which derives the next version and changelog entries from [Conventional Commits](https://www.conventionalcommits.org).

1. Make sure `main` is up to date and CI is green.
2. Run `cz bump`. This bumps the version (in `[tool.commitizen]` and `src/capawesome_cloud/_version.py`), regenerates `CHANGELOG.md`, and creates a release commit plus a matching `vX.Y.Z` tag — all locally, nothing is pushed yet. Pass `--dry-run` first if you want to preview the result.
3. Review the generated commit and changelog, then push everything: `git push --follow-tags origin main`.
4. Build the distributions with `python -m build`, then publish to PyPI with `python -m twine upload dist/*` (requires `pip install build twine`).

## License

See [LICENSE](./LICENSE).
