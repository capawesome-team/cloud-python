# Breaking Changes

This is a comprehensive list of the breaking changes introduced in the major version releases. Until version 1.0.0, breaking changes are introduced in minor version releases.

## Versions

- [Version 0.2.x](#version-02x)

## Version 0.2.x

### Job Logs

`jobs.logs()` now returns a list of `JobLog` models (with `number`, `payload` and `timestamp`) instead of the raw response text.

```diff
- print(client.jobs.logs(job_id))
+ for log in client.jobs.logs(job_id):
+     print(log.payload)
```

### Removed `git_repository_url` Parameter

The `git_repository_url` parameter has been removed from `apps.update()` as the API no longer supports it and ignored the value. Use `apps.repository.set()` to link an app to a Git repository instead.

```diff
- client.apps.update(app_id, git_repository_url="https://github.com/owner/name")
+ client.apps.repository.set(app_id, git_connection_id=git_connection_id, path="owner/name")
```
