
<a name="v0.4.6"></a>
## [v0.4.6] - 2021-06-22

<a name="v0.4.5"></a>
## [v0.4.5] - 2021-06-04
### Bug Fixes
- **step_ca:** prevent error when overwriting step-ca executable ([#68](https://github.com/maxhoesel/ansible-collection-smallstep/issues/68)) ([bdca736](https://github.com/maxhoesel/ansible-collection-smallstep/commit/bdca736))


<a name="v0.4.4"></a>
## [v0.4.4] - 2021-05-25
### Bug Fixes
- allow roles to run with --check once configured ([262f25d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/262f25d))


<a name="v0.4.3"></a>
## [v0.4.3] - 2021-05-24
### Bug Fixes
- **step_ca_boostrap:** don't fail on ubuntu 18.04 ([#64](https://github.com/maxhoesel/ansible-collection-smallstep/issues/64)) ([67331de](https://github.com/maxhoesel/ansible-collection-smallstep/commit/67331de))


<a name="v0.4.2"></a>
## [v0.4.2] - 2021-05-20
### Bug Fixes
- don't use privilege escalation when delegating locally ([#62](https://github.com/maxhoesel/ansible-collection-smallstep/issues/62)) ([60e1d44](https://github.com/maxhoesel/ansible-collection-smallstep/commit/60e1d44))

### Documentation
- change author notice in readme ([fbcc807](https://github.com/maxhoesel/ansible-collection-smallstep/commit/fbcc807))


<a name="v0.4.1"></a>
## [v0.4.1] - 2021-05-07
### Bug Fixes
- **step_acme_cert:** remove community.cryto dep ([#59](https://github.com/maxhoesel/ansible-collection-smallstep/issues/59)) ([0802b09](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0802b09))

### Documentation
- **step_acme_cert:** remove user permission bit ([baf9d04](https://github.com/maxhoesel/ansible-collection-smallstep/commit/baf9d04))


<a name="v0.4.0"></a>
## [v0.4.0] - 2021-05-07
### Bug Fixes
- **step_acme_cert:** ensure daemon is enabled ([56d041d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/56d041d))
- **step_acme_cert:** try to renew expired certs ([195eafe](https://github.com/maxhoesel/ansible-collection-smallstep/commit/195eafe))

### Features
- use root user for step-cli bootstrapping ([12672c9](https://github.com/maxhoesel/ansible-collection-smallstep/commit/12672c9))
- **step_acme_cert:** automatically get renew time ([a3fe8f6](https://github.com/maxhoesel/ansible-collection-smallstep/commit/a3fe8f6))


<a name="v0.3.2"></a>
## [v0.3.2] - 2021-04-16
### Bug Fixes
- **step_acme_cert:** fix validation errors on sudo change ([c030373](https://github.com/maxhoesel/ansible-collection-smallstep/commit/c030373))
- **step_acme_cert:** restart reneww service when config changes ([6a95388](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6a95388))
- **step_acme_cert:** restart sytemd units with sudo ([e4a8af3](https://github.com/maxhoesel/ansible-collection-smallstep/commit/e4a8af3))

### Documentation
- include repo url in changelog commits ([7f3658e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7f3658e))
- remove devel branch from documentation ([#52](https://github.com/maxhoesel/ansible-collection-smallstep/issues/52)) ([a4202bc](https://github.com/maxhoesel/ansible-collection-smallstep/commit/a4202bc))
- updated changelog for v0.3.1 ([51dc381](https://github.com/maxhoesel/ansible-collection-smallstep/commit/51dc381))

### Features
- Allow step-cli binary to bind to ports <1024 ([#55](https://github.com/maxhoesel/ansible-collection-smallstep/issues/55)) ([7c13c1d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7c13c1d))
- Allow step-cli binary to bind to ports <1024 ([#55](https://github.com/maxhoesel/ansible-collection-smallstep/issues/55)) ([dcbfc45](https://github.com/maxhoesel/ansible-collection-smallstep/commit/dcbfc45))


<a name="v0.3.1"></a>
## [v0.3.1] - 2021-03-30
### Bug Fixes
- hide password during initialization ([56fb923](https://github.com/maxhoesel/ansible-collection-smallstep/commit/56fb923))
- use step-cli name for step executable ([d2e8126](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d2e8126))
- **step_ca:** adjust archive name to upstream ([76d7828](https://github.com/maxhoesel/ansible-collection-smallstep/commit/76d7828))
- **step_ca_provisioner:** actually use ca_path ([f6f45f8](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f6f45f8))
- **step_cli:** update deb file name to follow upstream ([35862f6](https://github.com/maxhoesel/ansible-collection-smallstep/commit/35862f6))

### Documentation
- minor formatting fixes in README ([2dc48be](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2dc48be))
- updated changelog ([d6e2fde](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d6e2fde))
- updated git-chlog config ([a37ac2d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/a37ac2d))
- update module vevelopment information ([05177ed](https://github.com/maxhoesel/ansible-collection-smallstep/commit/05177ed))
- update contribution information ([0801fa8](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0801fa8))
- **step_ca_provisioner:** update documentation ([e508707](https://github.com/maxhoesel/ansible-collection-smallstep/commit/e508707))
- **step_cli:** fix invalid distro tags ([9b7325f](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9b7325f))
- **step_cli:** minor corrections and fixes ([d11367d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/d11367d))
- **step_cli:** fix readme errors ([5d98139](https://github.com/maxhoesel/ansible-collection-smallstep/commit/5d98139))
- **step_client:** add deprecation warning ([fad0039](https://github.com/maxhoesel/ansible-collection-smallstep/commit/fad0039))

### Features
- add arm64 support to step_ca and step_cli ([#49](https://github.com/maxhoesel/ansible-collection-smallstep/issues/49)) ([9133d7b](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9133d7b))
- add step_ca_certificate and _token modules ([9aaf5ab](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9aaf5ab))
- **step_acme_cert:** add acme_cert role ([aab5cd9](https://github.com/maxhoesel/ansible-collection-smallstep/commit/aab5cd9))
- **step_bootstrap_host:** add bootstrap_host role ([82ba298](https://github.com/maxhoesel/ansible-collection-smallstep/commit/82ba298))
- **step_ca:** install step-cli if missing ([6c2e78c](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6c2e78c))
- **step_ca:** add reworked step_ca role ([539d8b1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/539d8b1))
- **step_ca_bootstrap:** add bootstrap module ([43c2b91](https://github.com/maxhoesel/ansible-collection-smallstep/commit/43c2b91))
- **step_ca_renew:** add ca_renew module ([#42](https://github.com/maxhoesel/ansible-collection-smallstep/issues/42)) ([16c6d7c](https://github.com/maxhoesel/ansible-collection-smallstep/commit/16c6d7c))
- **step_ca_revoke:** add ca_revoke module ([#43](https://github.com/maxhoesel/ansible-collection-smallstep/issues/43)) ([46c2007](https://github.com/maxhoesel/ansible-collection-smallstep/commit/46c2007))
- **step_cli:** add reworked step_cli role to replace step_client ([65c25c5](https://github.com/maxhoesel/ansible-collection-smallstep/commit/65c25c5))


<a name="v0.3.0"></a>
## [v0.3.0] - 2021-03-29
### Bug Fixes
- hide password during initialization ([02b9211](https://github.com/maxhoesel/ansible-collection-smallstep/commit/02b9211))
- use step-cli name for step executable ([7bfb28f](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7bfb28f))
- **step_ca:** adjust archive name to upstream ([6dbdb03](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6dbdb03))
- **step_ca_provisioner:** actually use ca_path ([8243cfd](https://github.com/maxhoesel/ansible-collection-smallstep/commit/8243cfd))
- **step_cli:** update deb file name to follow upstream ([f08f26e](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f08f26e))

### Documentation
- updated changelog for v0.3.0 ([9c46512](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9c46512))
- minor formatting fixes in README ([7a8feab](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7a8feab))
- updated changelog ([9308387](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9308387))
- updated git-chlog config ([0e8e2cd](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0e8e2cd))
- update module vevelopment information ([f8a9b60](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f8a9b60))
- update contribution information ([9770b6a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/9770b6a))
- **step_ca_provisioner:** update documentation ([7bf388d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7bf388d))
- **step_cli:** fix invalid distro tags ([00d8db1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/00d8db1))
- **step_cli:** minor corrections and fixes ([2da11bd](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2da11bd))
- **step_cli:** fix readme errors ([817a46d](https://github.com/maxhoesel/ansible-collection-smallstep/commit/817a46d))
- **step_client:** add deprecation warning ([5c8e382](https://github.com/maxhoesel/ansible-collection-smallstep/commit/5c8e382))

### Features
- add step_ca_certificate and _token modules ([6a1bac0](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6a1bac0))
- **step_acme_cert:** add acme_cert role ([1f4b0e1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/1f4b0e1))
- **step_bootstrap_host:** add bootstrap_host role ([5601e95](https://github.com/maxhoesel/ansible-collection-smallstep/commit/5601e95))
- **step_ca:** install step-cli if missing ([459695a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/459695a))
- **step_ca:** add reworked step_ca role ([490ca6a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/490ca6a))
- **step_ca_bootstrap:** add bootstrap module ([c3bddad](https://github.com/maxhoesel/ansible-collection-smallstep/commit/c3bddad))
- **step_ca_renew:** add ca_renew module ([#42](https://github.com/maxhoesel/ansible-collection-smallstep/issues/42)) ([6c6be57](https://github.com/maxhoesel/ansible-collection-smallstep/commit/6c6be57))
- **step_ca_revoke:** add ca_revoke module ([#43](https://github.com/maxhoesel/ansible-collection-smallstep/issues/43)) ([287b26a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/287b26a))
- **step_cli:** add reworked step_cli role to replace step_client ([06d7b58](https://github.com/maxhoesel/ansible-collection-smallstep/commit/06d7b58))


<a name="v0.2.1"></a>
## [v0.2.1] - 2020-11-25
### Bug Fixes
- **step_client:** role is now idempotent ([f212aed](https://github.com/maxhoesel/ansible-collection-smallstep/commit/f212aed))

### Documentation
- fix typo in CA_SERVER.md ([0229360](https://github.com/maxhoesel/ansible-collection-smallstep/commit/0229360))
- **step_client:** add documentation ([2a4983a](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2a4983a))


<a name="v0.2.0"></a>
## [v0.2.0] - 2020-11-23
### Bug Fixes
- **ca_provisioner:** catch more erros when loading ca.json ([e6bfcfe](https://github.com/maxhoesel/ansible-collection-smallstep/commit/e6bfcfe))

### Documentation
- add step_client to README.md ([2af7013](https://github.com/maxhoesel/ansible-collection-smallstep/commit/2af7013))
- add testing matrix info ([54602f1](https://github.com/maxhoesel/ansible-collection-smallstep/commit/54602f1))
- removed debian 9 compatibility ([82b3358](https://github.com/maxhoesel/ansible-collection-smallstep/commit/82b3358))
- add ca_claims to README.md ([90d51fa](https://github.com/maxhoesel/ansible-collection-smallstep/commit/90d51fa))
- added commit format documentation ([7b4c952](https://github.com/maxhoesel/ansible-collection-smallstep/commit/7b4c952))

### Features
- **ca_claims:** add module ([189a08b](https://github.com/maxhoesel/ansible-collection-smallstep/commit/189a08b))
- **step_client:** added step_client role ([817d16f](https://github.com/maxhoesel/ansible-collection-smallstep/commit/817d16f))


<a name="v0.1.0"></a>
## v0.1.0 - 2020-11-13

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
