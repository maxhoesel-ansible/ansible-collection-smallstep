#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ca_certificate
author: Max Hösel (@maxhoesel)
short_description: Manage a step-ca-signed certificate on the target system
version_added: '0.3.0'
description: >
    Creates, updates, revokes or deletes a CA-issued certificate on the target system.
    This module exposes mostly the same parameters as the upstream
    L(step ca certificate,https://smallstep.com/docs/step-cli/reference/ca/certificate),
    L(step ca renew/rekey,https://smallstep.com/docs/step-cli/reference/ca/renew)
    and L(step ca revoke,https://smallstep.com/docs/step-cli/reference/ca/revoke/) commands, depending on the selected
    certificate I(state).
notes:
  - Check mode is supported.
  - >
      This module attempts to detect when a certificates parameters have changed, but may not detect all changes.
      Currently, the following parameters are checked for changes: I(san, kty, curve, size).
      Note that the key parameters are only checked if I(kty) is set
options:
  acme:
    description: >
      ACME directory url to be used for requesting certificates via the ACME protocol.
      Use this parameter to define an ACME server other than the Step CA.
      If this flag is absent and an ACME provisioner has been selected then the I(ca_url) parameter must be defined.
    type: str
  attestation_ca_root:
    description: The path to the PEM file with trusted roots when connecting to the Attestation CA.
    type: path
  attestation_ca_url:
    description: The base url of the Attestation CA to use.
    type: str
  attestation_uri:
    description: The KMS uri used for attestation.
    type: str
  console:
    description: Complete the flow while remaining inside the terminal
    type: bool
  contact:
    description: >
      The email-address used for contact as part of the ACME protocol.
      These contacts may be used to warn of certificate expiration or other certificate lifetime events.
      Must be a list
    type: list
    elements: str
  crt_file:
    description: File to write the certificate (PEM format).
    type: path
    required: yes
  curve:
    aliases:
      - crv
    description: >
      The elliptic curve to use for EC and OKP key types. Corresponds to the "crv" JWK parameter.
      Valid curves are defined in JWA RFC7518. If unset, default is P-256 for EC keys and Ed25519 for OKP keys.
    type: str
    choices:
      - P-256
      - P-384
      - P-521
      - Ed25519
  force:
    description: >
        If I(true) and I(state=present), a new certificate will be generated each time this module is executed,
        regardless of existing certificates.
    type: bool
  http_listen:
    description: >
      Use a non-standard http address, behind a reverse proxy or load balancer, for serving ACME challenges.
      The default address is :80, which requires super user (sudo) privileges.
      This flag must be used in conjunction with the I(standalone) param.
    type: str
  k8ssa_token_path:
    description: Configure the file from which to read the kubernetes service account token.
    type: path
  key_file:
    description: File to write the private key (PEM format).
    type: path
    required: yes
  kms:
    description: The uri to configure a Cloud KMS or an HSM.
    type: str
  kty:
    description: >
      The kty to build the certificate upon. If unset, default is EC. I(kty) is a case-sensitive string.
    type: str
    choices:
      - EC
      - OKP
      - RSA
  name:
    aliases:
      - subject
    description: >
      The Common Name, DNS Name, or IP address that will be set as the Subject Common Name for the certificate.
      If no Subject Alternative Names (SANs) are configured (via the san parameter) then the subject will be set as the only SAN.
      Required if I(state=present).
    type: str
  nebula_cert:
    description: Certificate file in PEM format to store in the 'nebula' header of a JWT.
    type: path
  nebula_key:
    description: >
      Private key file, used to sign a JWT,
      corresponding to the certificate that will be stored in the 'nebula' header.
    type: path
  not_after:
    description: >
      The time/duration when the certificate validity period ends. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  not_before:
    description: >
      The time/duration when the certificate validity period starts. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  provisioner:
    aliases:
      - issuer
    description: The provisioner name to use. Required if I(state=present).
    type: str
  provisioner_password_file:
    description: The path to the file containing the password to decrypt the one-time token generating key.
    type: path
  revoke_on_delete:
    description: If I(state=absent), attempt to revoke the certificate before deleting it
    type: bool
    default: true
  revoke_reason:
    description: >
        The string representing the reason for which the cert is being revoked.
        Only has an effect if I(state=revoked) or I(state=absent) and I(revoke_on_delete=True)
    type: str
  revoke_reason_code:
    description: >
        The reasonCode specifies the reason for revocation - chose from a list of common revocation reasons.
        If unset, the default is Unspecified.
        See U(https://smallstep.com/docs/step-cli/reference/ca/revoke) for a list of codes
    type: str
  san:
    description: >
      Add dns/ip/email/uri Subject Alternative Name(s) (SANs) that should be authorized.
      The I(san) parameter and the I(token) parameter are mutually exclusive. Must be a list.
    type: list
    elements: str
  set:
    description: The key=value pair with template data variables to send to the CA. Must be a list.
    type: list
    elements: str
  set_file:
    description: The path of a JSON file with the template data to send to the CA.
    type: path
  size:
    description: >
      The size (in bits) of the key for RSA and oct key types. RSA keys require a minimum key size of 2048 bits.
      If unset, default is 2048 bits for RSA keys and 128 bits for oct keys.
    type: int
  standalone:
    description: >
      Get a certificate using the ACME protocol and standalone mode for validation.
      Standalone is a mode in which the step process will run a server that will will respond to ACME challenge validation requests.
      Standalone is the default mode for serving challenge validation requests.
    type: bool
  state:
    description: >
        State that the certificate should be in.
        If I(state=present), the certificate will be (re-)issued if it doesn't exist, is invalid/expired or if its SAN/private key parameters change.
        If I(state=revoked), the certificate will be revoked with the CA
        If I(state=absent), the certificate will be removed from the host (and optionally revoked with the CA beforehand, see I(revoke_on_delete).
    type: str
    choices:
      - present
      - revoked
      - absent
    default: present
  token:
    description: The one-time token used to authenticate with the CA in order to create the certificate.
    type: str
  tpm_storage_directory:
    description: The directory where TPM keys and certificates will be stored
    type: path
  verify_roots:
    description: >
        Root certificates to use when checking an existing certificates validity.
        Only required if your CA root is not in the system truststore.
        Case-sensitive string, may be one of:
        Relative or full path to a file - All certificates in the file will be used for path validation.
        Comma-separated list of relative or full file paths - Every PEM encoded certificate from each file will be used for path validation.
        Relative or full path to a directory - Every PEM encoded certificate from each file in the directory will be used for path validation.
    type: str
  webroot:
    description: >
      Specify a path to use as a 'web root' for validation in the ACME protocol.
      Webroot is a mode in which the step process will write a challenge file to a location being
      served by an existing fileserver in order to respond to ACME challenge validation requests.
    type: path
  x5c_cert:
    description: Certificate (chain) in PEM format to store in the 'x5c' header of a JWT.
    type: str
  x5c_key:
    description: Private key path, used to sign a JWT, corresponding to the certificate that will be stored in the 'x5c' header.
    type: path

extends_documentation_fragment:
  - maxhoesel.smallstep.cli_executable
  - maxhoesel.smallstep.ca_connection
"""

EXAMPLES = r"""
# See https://smallstep.com/docs/step-cli/reference/ca/certificate for more examples
- name: Ensure valid certificate exists
  maxhoesel.smallstep.step_ca_certificate:
    name: "{{ ansible_fqdn }}"
    crt_file: "/etc/ssl/my.cert"
    key_file: "/etc/ssl/my.key"
    provisioner: "jwk"
    provisioner_password_file: "/path/to/password_file"
    san:
    - foo.bar
    kty: EC
    crv: P-256
    not_after: 24h

- name: Use custom root to verify existing cert
  maxhoesel.smallstep.step_ca_certificate:
    name: "{{ ansible_fqdn }}"
    crt_file: "/etc/ssl/my.cert"
    key_file: "/etc/ssl/my.key"
    provisioner: "jwk"
    provisioner_password_file: "/path/to/password_file"
    san:
    - foo.bar
    kty: EC
    crv: P-256
    not_after: 24h
    # If the certificate already exists, this certificate will be used to validate it.
    # If the validation fails, a new certificate will be created.
    # Only required if your CA root is not in the system truststore
    verify_roots: "/path/to/custom/root_ca.crt"

- name: Ensure cert is revoked
  maxhoesel.smallstep.step_ca_certificate:
    name: "{{ ansible_fqdn }}"
    crt_file: "/etc/ssl/my.cert"
    key_file: "/etc/ssl/my.key"
    state: revoked

- name: Ensure cert is absent (and revoke if first if it isn't)
  maxhoesel.smallstep.step_ca_certificate:
    name: "{{ ansible_fqdn }}"
    crt_file: "/etc/ssl/my.cert"
    key_file: "/etc/ssl/my.key"
    state: absent
    revoke_on_delete: true
"""
from pathlib import Path
from typing import cast, Dict, Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import check_required_if

from ..module_utils.params.ca_connection import CaConnectionParams
from ..module_utils.cli_wrapper import CliCommand, StepCliExecutable
from ..module_utils import helpers
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE

# maps the kty cli parameter to inspect outputs subject_key_info.key_algorithm.name
CERTINFO_KEY_TYPES = {
    "RSA": "RSA",
    "EC": "ECDSA",
    "OKP": "Ed25519"
}
CERTINFO_KEYINFO_KEY = {
    "RSA": "rsa_public_key",
    "ECDSA": "ecdsa_public_key"
}


def create_certificate(executable: StepCliExecutable, module: AnsibleModule, force: bool = False) -> Dict[str, Any]:
    module_params = cast(Dict, module.params)
    # step ca certificate arguments
    cert_cliargs = ["acme", "attestation_ca_url", "attestation_ca_root", "console", "contact", "curve",
                    "http_listen", "k8ssa_token_path", "kms", "kty", "nebula_cert", "nebula_key", "not_after",
                    "not_before", "provisioner", "provisioner_password_file", "san", "set", "set_file", "size",
                    "standalone", "token", "tpm_storage_directory", "webroot", "x5c_cert", "x5c_key"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    cert_cliarg_map = {arg: f"--{arg.replace('_', '-')}" for arg in cert_cliargs}

    args = ["ca", "certificate", module_params["name"], module_params["crt_file"], module_params["key_file"]]
    if force:
        args.append("--force")

    create_cmd = CliCommand(executable, args, {
        **cert_cliarg_map,
        **CaConnectionParams.cliarg_map
    })
    create_cmd.run(module)
    return {"changed": True}


def cert_needs_recreation(executable: StepCliExecutable, module: AnsibleModule) -> str:
    """Check whether a certificate needs to be recreated based on its validity and module parameters

    Returns:
        str: Reason for certificate recreation, or empty string if no recreation is needed
    """
    module_params = cast(Dict, module.params)

    cert_info = helpers.get_certificate_info(
        executable, module, module_params["crt_file"], roots=module_params["verify_roots"])

    # certificate is invalid
    if not cert_info.valid:
        return cert_info.invalid_reason

    key_info = cert_info.data["subject_key_info"]
    current_kty = key_info["key_algorithm"]["name"]

    # ensure SANs match
    if module_params["san"]:
        desired_sans = sorted(list(set([module_params["name"]] + module_params["san"])))
        current_sans = sorted(cert_info.data["names"])
        if current_sans != desired_sans:
            return f"Certificate names have changed from {cert_info.data['names']} to {desired_sans}"

    # Ensure key type matches
    if module_params["kty"]:
        if current_kty != CERTINFO_KEY_TYPES[module_params["kty"]]:
            return f"Key type has changed from {current_kty} to {CERTINFO_KEY_TYPES[module_params['kty']]}"
        if module_params["curve"] and current_kty == "ECDSA":
            current_curve = key_info["ecdsa_public_key"]["curve"]
            if current_curve != module_params["curve"]:
                return f"ECDSA key curve has changed from {current_curve} to {module_params['curve']}"

    # key type matches or is not specified, we can assume the current type is correct
    if module_params["size"] and current_kty in ["RSA", "ECDSA"]:
        current_length = key_info[CERTINFO_KEYINFO_KEY[current_kty]]["length"]
        if current_length != module_params["size"]:
            return f"Key size has changed from {current_length} to {module_params['size']}"
    return ""


def revoke_certificate(executable: StepCliExecutable, module: AnsibleModule) -> Dict[str, Any]:  # pylint: disable=unused-argument
    revoke_cliarg_map = {
        "crt_file": "--cert",
        "key_file": "--key",
        "revoke_reason": "--reason",
        "revoke_reason_code": "--reasonCode",
        "token": "--token"
    }
    revoke_cmd = CliCommand(executable, ["ca", "revoke"], {
        **revoke_cliarg_map,
        **CaConnectionParams.cliarg_map
    }, fail_on_error=False)
    res = revoke_cmd.run(module)

    if res.rc != 0 and "is already revoked" in res.stderr:
        return {}
    elif res.rc != 0:
        module.fail_json(f"Error revoking certificate: {res.stderr}")
        return {"changed": True}  # only here to satisfy the type checker, fail_json never returns
    else:
        # ran successfully => revoked
        return {"changed": True}


def delete_certificate(executable: StepCliExecutable, module: AnsibleModule, revoke: bool) -> Dict[str, Any]:
    module_params = cast(Dict, module.params)
    result = {}
    if revoke:
        result = revoke_certificate(executable, module)

    for file in [Path(module_params["crt_file"]), Path(module_params["key_file"])]:
        if file.exists():
            try:
                file.unlink()
            except FileNotFoundError:
                pass
            except OSError as e:
                module.fail_json(f"Could not delete file: {e}")
            result["changed"] = True
    return result


def run_module():
    argument_spec = dict(
        acme=dict(type="str"),
        attestation_ca_url=dict(type="str"),
        attestation_ca_root=dict(type="path"),
        attestation_uri=dict(type="str"),
        console=dict(type="bool"),
        contact=dict(type="list", elements="str"),
        crt_file=dict(type="path", required=True),
        curve=dict(type="str", choices=[
                   "P-256", "P-384", "P-521", "Ed25519"], aliases=["crv"]),
        force=dict(type="bool"),
        http_listen=dict(type="str"),
        k8ssa_token_path=dict(type="path"),
        key_file=dict(type="path", required=True),
        kms=dict(type="str"),
        kty=dict(type="str", choices=["EC", "OKP", "RSA"]),
        name=dict(type="str", aliases=["subject"]),
        nebula_cert=dict(type="path"),
        nebula_key=dict(type="path"),
        not_after=dict(type="str"),
        not_before=dict(type="str"),
        provisioner=dict(type="str", aliases=["issuer"]),
        provisioner_password_file=dict(type="path", no_log=False),
        revoke_on_delete=dict(type="bool", default=True),
        revoke_reason=dict(type="str"),
        revoke_reason_code=dict(type="str"),
        san=dict(type="list", elements="str"),
        set=dict(type="list", elements="str"),
        set_file=dict(type="path"),
        size=dict(type="int"),
        standalone=dict(type="bool"),
        state=dict(type="str", choices=["present", "revoked", "absent"], default="present"),
        token=dict(type="str", no_log=True),
        tpm_storage_directory=dict(type="path"),
        verify_roots=dict(type="str"),
        webroot=dict(type="path"),
        x5c_cert=dict(type="str"),
        x5c_key=dict(type="path"),
        step_cli_executable=dict(type="path", default=DEFAULT_STEP_CLI_EXECUTABLE)
    )
    result: Dict[str, Any] = dict(changed=False)
    module = AnsibleModule(argument_spec={
        **CaConnectionParams.argument_spec,
        **argument_spec,
    }, supports_check_mode=True)
    CaConnectionParams(module).check()
    module_params = cast(Dict, module.params)
    check_required_if([
        ["state", "present", ["name", "provisioner"], True],
    ], module_params)
    executable = StepCliExecutable(module, module_params["step_cli_executable"])

    crt_exists = Path(module_params["crt_file"]).exists()
    if module_params["state"] == "present":
        if not crt_exists:
            result.update(create_certificate(executable, module))
        else:
            if module_params["force"]:
                recreate_reason = "force parameter enabled"
            else:
                recreate_reason = cert_needs_recreation(executable, module)
            if recreate_reason:
                result["recreate_reason"] = recreate_reason
                result.update(create_certificate(executable, module, force=True))
    elif module_params["state"] == "revoked":
        if crt_exists:
            result.update(revoke_certificate(executable, module))
        else:
            module.fail_json("Cannot revoke certificate as it does not exist")
    elif module_params["state"] == "absent" and crt_exists:
        result.update(delete_certificate(executable, module, module_params["revoke_on_delete"]))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
