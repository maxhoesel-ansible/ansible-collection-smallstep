<a name="unreleased"></a>
## [Unreleased]

### Bug Fixes
- use step-cli name for step executable (d2e8126)
- **step_ca:** adjust archive name to upstream (76d7828)
- **step_cli:** update deb file name to follow upstream (35862f6)

### Documentation
- update module vevelopment information (05177ed)
- update contribution information (0801fa8)
- **step_ca_provisioner:** update documentation (e508707)
- **step_cli:** fix invalid distro tags (9b7325f)
- **step_cli:** minor corrections and fixes (d11367d)
- **step_cli:** fix readme errors (5d98139)
- **step_client:** add deprecation warning (fad0039)

### Features
- add step_ca_certificate and _token modules (9aaf5ab)
- **step_ca:** add reworked step_ca role (539d8b1)
- **step_ca_bootstrap:** add bootstrap module (43c2b91)
- **step_cli:** add reworked step_cli role to replace step_client (65c25c5)


<a name="v0.2.1"></a>
## [v0.2.1] - 2020-11-25
### Bug Fixes
- **step_client:** role is now idempotent (f212aed)

### Documentation
- fix typo in CA_SERVER.md (0229360)
- **step_client:** add documentation (2a4983a)


<a name="v0.2.0"></a>
## [v0.2.0] - 2020-11-23
### Bug Fixes
- **ca_provisioner:** catch more erros when loading ca.json (e6bfcfe)

### Documentation
- add step_client to README.md (2af7013)
- add testing matrix info (54602f1)
- removed debian 9 compatibility (82b3358)
- add ca_claims to README.md (90d51fa)
- added commit format documentation (7b4c952)

### Features
- **ca_claims:** add module (189a08b)
- **step_client:** added step_client role (817d16f)


<a name="v0.1.0"></a>
## v0.1.0 - 2020-11-13

[Unreleased]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.2.1...HEAD
[v0.2.1]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.1.0...v0.2.0
