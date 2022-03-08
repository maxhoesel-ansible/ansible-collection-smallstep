
<a name="v0.4.10"></a>
## [v0.4.10] - 2022-03-08
### Bug Fixes
- **step_ca:** properly escape params during init ([36861f2](https://github.com/maxhoesel/ansible-collection-smallstep/commit/36861f2)) [Max Hösel]
- **step_ca:** always create intermediate password file ([13cbf10](https://github.com/maxhoesel/ansible-collection-smallstep/commit/13cbf10)) [Max Hösel]

### Documentation
- update README shields ([0902c65](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0902c65)) [Max Hösel]


<a name="v0.4.9"></a>
## [v0.4.9] - 2021-08-27
### Bug Fixes
- **step_ca_provisioner:** catch non-existent authority ([#118](https://github.com/maxhoesel/ansible-collection-smallstep/issues/118)) ([3f0d41c](https://github.com/maxhoesel/ansible-collection-smallstep/commit/3f0d41c)) [Max Hösel]

### Documentation
- update contribution docs ([21e19d0](https://github.com/maxhoesel/ansible-collection-smallstep/commit/21e19d0)) [Max Hösel]
- add author names to changelog ([#112](https://github.com/maxhoesel/ansible-collection-smallstep/issues/112)) ([fe33240](https://github.com/maxhoesel/ansible-collection-smallstep/commit/fe33240)) [Max Hösel]


<a name="v0.4.8"></a>
## [v0.4.8] - 2021-08-25
### Bug Fixes
- eliminate "expected errors" when looking for step-cli/certs ([#103](https://github.com/maxhoesel/ansible-collection-smallstep/issues/103)) ([d488e6e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d488e6e)) [Max Hösel]
- **step_acme_cert:** don't fail when the user doesn't proide a path ([#104](https://github.com/maxhoesel/ansible-collection-smallstep/issues/104)) ([4fc153e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/4fc153e)) [Max Hösel]

### Documentation
- fix incorrect backticks in README.md ([#101](https://github.com/maxhoesel/ansible-collection-smallstep/issues/101)) ([3820904](https://github.com/maxhoesel/ansible-collection-smallstep/commit/3820904)) [Max Hösel]

### Features
- add support for debian 11 ([250dca0](https://github.com/maxhoesel/ansible-collection-smallstep/commit/250dca0)) [Max Hösel]


<a name="v0.4.7"></a>
## [v0.4.7] - 2021-07-20
### Bug Fixes
- **step_bootstrap_host:** support STEPPATH ENV VAR ([#89](https://github.com/maxhoesel/ansible-collection-smallstep/issues/89)) ([371041a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/371041a)) [Eric Engstrom]
- **step_bootstrap_host:** properly support non-default STEPPATH  ([#87](https://github.com/maxhoesel/ansible-collection-smallstep/issues/87)) ([3252c66](https://github.com/maxhoesel/ansible-collection-smallstep/commit/3252c66)) [Max Hösel]
- **step_ca:** make unset defaults actually undefined instead of "" ([02176ca](https://github.com/maxhoesel/ansible-collection-smallstep/commit/02176ca)) [Max Hösel]
- **step_ca:** eliminate spurious Ansible "password" warnings ([#86](https://github.com/maxhoesel/ansible-collection-smallstep/issues/86)) ([c66a9f4](https://github.com/maxhoesel/ansible-collection-smallstep/commit/c66a9f4)) [Eric Engstrom]
- **utils:** capture step_cli attempt to open tty ([#77](https://github.com/maxhoesel/ansible-collection-smallstep/issues/77)) ([cc9f5a1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/cc9f5a1)) [Eric Engstrom]

### Documentation
- fix link in readme ([2788028](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2788028)) [Max Hösel]
- rework docs and add STEPPATH info ([368e592](https://github.com/maxhoesel/ansible-collection-smallstep/commit/368e592)) [Max Hösel]
- update main README and module doc strings ([#80](https://github.com/maxhoesel/ansible-collection-smallstep/issues/80)) ([3203563](https://github.com/maxhoesel/ansible-collection-smallstep/commit/3203563)) [Eric Engstrom]
- **step_acme_cert:** fix outdated readme ([8c9143e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/8c9143e)) [Max Hösel]

### Features
- add STEPPATH support to bootstrap_host and acme_cert ([4e4e0a3](https://github.com/maxhoesel/ansible-collection-smallstep/commit/4e4e0a3)) [Max Hösel]
- **step_acme_cert:** better default value support for cert gen ([#81](https://github.com/maxhoesel/ansible-collection-smallstep/issues/81)) ([#82](https://github.com/maxhoesel/ansible-collection-smallstep/issues/82)) ([b448272](https://github.com/maxhoesel/ansible-collection-smallstep/commit/b448272)) [Eric Engstrom]
- **step_boostrap_host:** pass `force` to underlying module ([#73](https://github.com/maxhoesel/ansible-collection-smallstep/issues/73)) ([#79](https://github.com/maxhoesel/ansible-collection-smallstep/issues/79)) ([86b8470](https://github.com/maxhoesel/ansible-collection-smallstep/commit/86b8470)) [Eric Engstrom]
- **step_ca_bootstrap:** fail bootstrap if fingerprint mismatch ([#78](https://github.com/maxhoesel/ansible-collection-smallstep/issues/78)) ([8534061](https://github.com/maxhoesel/ansible-collection-smallstep/commit/8534061)) [Eric Engstrom]


<a name="v0.4.6"></a>
## [v0.4.6] - 2021-06-22

<a name="v0.4.5"></a>
## [v0.4.5] - 2021-06-04
### Bug Fixes
- **step_ca:** prevent error when overwriting step-ca executable ([#68](https://github.com/maxhoesel/ansible-collection-smallstep/issues/68)) ([bdca736](https://github.com/maxhoesel/ansible-collection-smallstep/commit/bdca736)) [Max Hösel]


<a name="v0.4.4"></a>
## [v0.4.4] - 2021-05-25
### Bug Fixes
- allow roles to run with --check once configured ([262f25d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/262f25d)) [Max Hösel]


<a name="v0.4.3"></a>
## [v0.4.3] - 2021-05-24
### Bug Fixes
- **step_ca_boostrap:** don't fail on ubuntu 18.04 ([#64](https://github.com/maxhoesel/ansible-collection-smallstep/issues/64)) ([67331de](https://github.com/maxhoesel/ansible-collection-smallstep/commit/67331de)) [Max Hösel]


<a name="v0.4.2"></a>
## [v0.4.2] - 2021-05-20
### Bug Fixes
- don't use privilege escalation when delegating locally ([#62](https://github.com/maxhoesel/ansible-collection-smallstep/issues/62)) ([60e1d44](https://github.com/maxhoesel/ansible-collection-smallstep/commit/60e1d44)) [Jesse Roland]

### Documentation
- change author notice in readme ([fbcc807](https://github.com/maxhoesel/ansible-collection-smallstep/commit/fbcc807)) [Max Hösel]


<a name="v0.4.1"></a>
## [v0.4.1] - 2021-05-07
### Bug Fixes
- **step_acme_cert:** remove community.cryto dep ([#59](https://github.com/maxhoesel/ansible-collection-smallstep/issues/59)) ([0802b09](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0802b09)) [Max Hösel]

### Documentation
- **step_acme_cert:** remove user permission bit ([baf9d04](https://github.com/maxhoesel/ansible-collection-smallstep/commit/baf9d04)) [Max Hösel]


<a name="v0.4.0"></a>
## [v0.4.0] - 2021-05-07
### Bug Fixes
- **step_acme_cert:** ensure daemon is enabled ([56d041d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/56d041d)) [Max Hösel]
- **step_acme_cert:** try to renew expired certs ([195eafe](https://github.com/maxhoesel/ansible-collection-smallstep/commit/195eafe)) [Max Hösel]

### Features
- use root user for step-cli bootstrapping ([12672c9](https://github.com/maxhoesel/ansible-collection-smallstep/commit/12672c9)) [Max Hösel]
- **step_acme_cert:** automatically get renew time ([a3fe8f6](https://github.com/maxhoesel/ansible-collection-smallstep/commit/a3fe8f6)) [Max Hösel]


<a name="v0.3.2"></a>
## [v0.3.2] - 2021-04-16
### Bug Fixes
- **step_acme_cert:** fix validation errors on sudo change ([c030373](https://github.com/maxhoesel/ansible-collection-smallstep/commit/c030373)) [Max Hösel]
- **step_acme_cert:** restart reneww service when config changes ([6a95388](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6a95388)) [Max Hösel]
- **step_acme_cert:** restart sytemd units with sudo ([e4a8af3](https://github.com/maxhoesel/ansible-collection-smallstep/commit/e4a8af3)) [Max Hösel]

### Documentation
- include repo url in changelog commits ([7f3658e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7f3658e)) [Max Hösel]
- remove devel branch from documentation ([#52](https://github.com/maxhoesel/ansible-collection-smallstep/issues/52)) ([a4202bc](https://github.com/maxhoesel/ansible-collection-smallstep/commit/a4202bc)) [Max Hösel]
- updated changelog for v0.3.1 ([51dc381](https://github.com/maxhoesel/ansible-collection-smallstep/commit/51dc381)) [GitHub Actions]

### Features
- Allow step-cli binary to bind to ports <1024 ([#55](https://github.com/maxhoesel/ansible-collection-smallstep/issues/55)) ([7c13c1d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7c13c1d)) [Max Hösel]
- Allow step-cli binary to bind to ports <1024 ([#55](https://github.com/maxhoesel/ansible-collection-smallstep/issues/55)) ([dcbfc45](https://github.com/maxhoesel/ansible-collection-smallstep/commit/dcbfc45)) [Max Hösel]


<a name="v0.3.1"></a>
## [v0.3.1] - 2021-03-30
### Bug Fixes
- hide password during initialization ([56fb923](https://github.com/maxhoesel/ansible-collection-smallstep/commit/56fb923)) [Max Hösel]
- use step-cli name for step executable ([d2e8126](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d2e8126)) [Max Hösel]
- **step_ca:** adjust archive name to upstream ([76d7828](https://github.com/maxhoesel/ansible-collection-smallstep/commit/76d7828)) [Max Hösel]
- **step_ca_provisioner:** actually use ca_path ([f6f45f8](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f6f45f8)) [Max Hösel]
- **step_cli:** update deb file name to follow upstream ([35862f6](https://github.com/maxhoesel/ansible-collection-smallstep/commit/35862f6)) [Max Hösel]

### Documentation
- minor formatting fixes in README ([2dc48be](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2dc48be)) [Max Hösel]
- updated changelog ([d6e2fde](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d6e2fde)) [Max Hösel]
- updated git-chlog config ([a37ac2d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/a37ac2d)) [Max Hösel]
- update module vevelopment information ([05177ed](https://github.com/maxhoesel/ansible-collection-smallstep/commit/05177ed)) [Max Hösel]
- update contribution information ([0801fa8](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0801fa8)) [Max Hösel]
- **step_ca_provisioner:** update documentation ([e508707](https://github.com/maxhoesel/ansible-collection-smallstep/commit/e508707)) [Max Hösel]
- **step_cli:** fix invalid distro tags ([9b7325f](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9b7325f)) [Max Hösel]
- **step_cli:** minor corrections and fixes ([d11367d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d11367d)) [Max Hösel]
- **step_cli:** fix readme errors ([5d98139](https://github.com/maxhoesel/ansible-collection-smallstep/commit/5d98139)) [Max Hösel]
- **step_client:** add deprecation warning ([fad0039](https://github.com/maxhoesel/ansible-collection-smallstep/commit/fad0039)) [Max Hösel]

### Features
- add arm64 support to step_ca and step_cli ([#49](https://github.com/maxhoesel/ansible-collection-smallstep/issues/49)) ([9133d7b](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9133d7b)) [Max Hösel]
- add step_ca_certificate and _token modules ([9aaf5ab](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9aaf5ab)) [Max Hösel]
- **step_acme_cert:** add acme_cert role ([aab5cd9](https://github.com/maxhoesel/ansible-collection-smallstep/commit/aab5cd9)) [Max Hösel]
- **step_bootstrap_host:** add bootstrap_host role ([82ba298](https://github.com/maxhoesel/ansible-collection-smallstep/commit/82ba298)) [Max Hösel]
- **step_ca:** install step-cli if missing ([6c2e78c](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6c2e78c)) [Max Hösel]
- **step_ca:** add reworked step_ca role ([539d8b1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/539d8b1)) [Max Hösel]
- **step_ca_bootstrap:** add bootstrap module ([43c2b91](https://github.com/maxhoesel/ansible-collection-smallstep/commit/43c2b91)) [Max Hösel]
- **step_ca_renew:** add ca_renew module ([#42](https://github.com/maxhoesel/ansible-collection-smallstep/issues/42)) ([16c6d7c](https://github.com/maxhoesel/ansible-collection-smallstep/commit/16c6d7c)) [Max Hösel]
- **step_ca_revoke:** add ca_revoke module ([#43](https://github.com/maxhoesel/ansible-collection-smallstep/issues/43)) ([46c2007](https://github.com/maxhoesel/ansible-collection-smallstep/commit/46c2007)) [Max Hösel]
- **step_cli:** add reworked step_cli role to replace step_client ([65c25c5](https://github.com/maxhoesel/ansible-collection-smallstep/commit/65c25c5)) [Max Hösel]


<a name="v0.3.0"></a>
## [v0.3.0] - 2021-03-29
### Bug Fixes
- hide password during initialization ([02b9211](https://github.com/maxhoesel/ansible-collection-smallstep/commit/02b9211)) [Max Hösel]
- use step-cli name for step executable ([7bfb28f](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7bfb28f)) [Max Hösel]
- **step_ca:** adjust archive name to upstream ([6dbdb03](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6dbdb03)) [Max Hösel]
- **step_ca_provisioner:** actually use ca_path ([8243cfd](https://github.com/maxhoesel/ansible-collection-smallstep/commit/8243cfd)) [Max Hösel]
- **step_cli:** update deb file name to follow upstream ([f08f26e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f08f26e)) [Max Hösel]

### Documentation
- updated changelog for v0.3.0 ([9c46512](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9c46512)) [GitHub Actions]
- minor formatting fixes in README ([7a8feab](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7a8feab)) [Max Hösel]
- updated changelog ([9308387](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9308387)) [Max Hösel]
- updated git-chlog config ([0e8e2cd](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0e8e2cd)) [Max Hösel]
- update module vevelopment information ([f8a9b60](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f8a9b60)) [Max Hösel]
- update contribution information ([9770b6a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9770b6a)) [Max Hösel]
- **step_ca_provisioner:** update documentation ([7bf388d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7bf388d)) [Max Hösel]
- **step_cli:** fix invalid distro tags ([00d8db1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/00d8db1)) [Max Hösel]
- **step_cli:** minor corrections and fixes ([2da11bd](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2da11bd)) [Max Hösel]
- **step_cli:** fix readme errors ([817a46d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/817a46d)) [Max Hösel]
- **step_client:** add deprecation warning ([5c8e382](https://github.com/maxhoesel/ansible-collection-smallstep/commit/5c8e382)) [Max Hösel]

### Features
- add step_ca_certificate and _token modules ([6a1bac0](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6a1bac0)) [Max Hösel]
- **step_acme_cert:** add acme_cert role ([1f4b0e1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/1f4b0e1)) [Max Hösel]
- **step_bootstrap_host:** add bootstrap_host role ([5601e95](https://github.com/maxhoesel/ansible-collection-smallstep/commit/5601e95)) [Max Hösel]
- **step_ca:** install step-cli if missing ([459695a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/459695a)) [Max Hösel]
- **step_ca:** add reworked step_ca role ([490ca6a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/490ca6a)) [Max Hösel]
- **step_ca_bootstrap:** add bootstrap module ([c3bddad](https://github.com/maxhoesel/ansible-collection-smallstep/commit/c3bddad)) [Max Hösel]
- **step_ca_renew:** add ca_renew module ([#42](https://github.com/maxhoesel/ansible-collection-smallstep/issues/42)) ([6c6be57](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6c6be57)) [Max Hösel]
- **step_ca_revoke:** add ca_revoke module ([#43](https://github.com/maxhoesel/ansible-collection-smallstep/issues/43)) ([287b26a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/287b26a)) [Max Hösel]
- **step_cli:** add reworked step_cli role to replace step_client ([06d7b58](https://github.com/maxhoesel/ansible-collection-smallstep/commit/06d7b58)) [Max Hösel]


<a name="v0.2.1"></a>
## [v0.2.1] - 2020-11-25
### Bug Fixes
- **step_client:** role is now idempotent ([f212aed](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f212aed)) [Max Hösel]

### Documentation
- fix typo in CA_SERVER.md ([0229360](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0229360)) [Max Hösel]
- **step_client:** add documentation ([2a4983a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2a4983a)) [Max Hösel]


<a name="v0.2.0"></a>
## [v0.2.0] - 2020-11-23
### Bug Fixes
- **ca_provisioner:** catch more erros when loading ca.json ([e6bfcfe](https://github.com/maxhoesel/ansible-collection-smallstep/commit/e6bfcfe)) [Max Hösel]

### Documentation
- add step_client to README.md ([2af7013](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2af7013)) [Max Hösel]
- add testing matrix info ([54602f1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/54602f1)) [Max Hösel]
- removed debian 9 compatibility ([82b3358](https://github.com/maxhoesel/ansible-collection-smallstep/commit/82b3358)) [Max Hösel]
- add ca_claims to README.md ([90d51fa](https://github.com/maxhoesel/ansible-collection-smallstep/commit/90d51fa)) [Max Hösel]
- added commit format documentation ([7b4c952](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7b4c952)) [Max Hösel]

### Features
- **ca_claims:** add module ([189a08b](https://github.com/maxhoesel/ansible-collection-smallstep/commit/189a08b)) [Max Hösel]
- **step_client:** added step_client role ([817d16f](https://github.com/maxhoesel/ansible-collection-smallstep/commit/817d16f)) [Max Hösel]


<a name="v0.1.0"></a>
## v0.1.0 - 2020-11-13

[v0.4.10]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.9...v0.4.10
[v0.4.9]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.8...v0.4.9
[v0.4.8]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.7...v0.4.8
[v0.4.7]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.6...v0.4.7
[v0.4.6]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.5...v0.4.6
[v0.4.5]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.4...v0.4.5
[v0.4.4]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.3...v0.4.4
[v0.4.3]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.2...v0.4.3
[v0.4.2]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.1...v0.4.2
[v0.4.1]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.4.0...v0.4.1
[v0.4.0]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.3.2...v0.4.0
[v0.3.2]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.3.1...v0.3.2
[v0.3.1]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.3.0...v0.3.1
[v0.3.0]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.2.1...v0.3.0
[v0.2.1]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/maxhoesel/ansible-collection-smallstep/compare/v0.1.0...v0.2.0
