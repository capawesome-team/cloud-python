# Changelog

## [0.2.1](https://github.com/capawesome-team/cloud-python/compare/v0.2.0...v0.2.1) (2026-10-01)


### Features

* **apps:** add `build_stack` to apps ([#8](https://github.com/capawesome-team/cloud-python/issues/8)) ([25b34a9](https://github.com/capawesome-team/cloud-python/commit/25b34a93a6302bf828ed6c97766a3c709f39ecc4))

## [0.2.0](https://github.com/capawesome-team/cloud-python/compare/v0.1.0...v0.2.0) (2026-10-01)


### ⚠ BREAKING CHANGES

* `jobs.logs()` returns `List[JobLog]` instead of `str`, and `apps.update()` no longer accepts `git_repository_url`.

### Features

* add organization resources ([#4](https://github.com/capawesome-team/cloud-python/issues/4)) ([17e0e7f](https://github.com/capawesome-team/cloud-python/commit/17e0e7fc3634fe7a6102e49ac3e52dab3be66ee2))
* sync app, job and user resources with the Node SDK ([#3](https://github.com/capawesome-team/cloud-python/issues/3)) ([11dcf07](https://github.com/capawesome-team/cloud-python/commit/11dcf07877c1631e0287b7a7152a52c176b7aa8c))


### Bug Fixes

* return parsed job logs and remove `git_repository_url` ([#5](https://github.com/capawesome-team/cloud-python/issues/5)) ([7306c46](https://github.com/capawesome-team/cloud-python/commit/7306c461e490a006a6fe0c15ee8d6f896b58686b))

## 0.1.0 (2026-06-02)

### Features

- add Capawesome Cloud Python SDK ([#1](https://github.com/capawesome-team/cloud-python/issues/1)) ([80d28ba](https://github.com/capawesome-team/cloud-python/commit/80d28ba519e5fcd98274410c3c76493768a581d3))
