#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: step_ca_certificate
author: Max Hösel (@maxhoesel)
short_description: Generate a new private key and certificate signed by the root certificate
version_added: '0.3.0'
description: Calls step-cli to create new certificates from the local or remote CA.
notes:
  - Check mode is supported.
options:
  acme:
    description: >
      ACME directory url to be used for requesting certificates via the ACME protocol.
      Use this parameter to define an ACME server other than the Step CA.
      If this flag is absent and an ACME provisioner has been selected then the I(ca_url) parameter must be defined.
    type: str
  contact:
    description: >
      The email-address used for contact as part of the ACME protocol.
      These contacts may be used to warn of certificate expiration or other certificate lifetime events.
      Must be a list
    type: list
    elements: str
  crt_file:
    description: File to write the certificate (PEM format)
    type: path
    required: yes
  curve:
    aliases:
      - crv
    description: >
      The elliptic curve to use for EC and OKP key types. Corresponds to the "crv" JWK parameter.
      Valid curves are defined in JWA [RFC7518]. If unset, default is P-256 for EC keys and Ed25519 for OKP keys.
    type: str
    choices:
      - P-256
      - P-384
      - P-521
      - Ed25519
  force:
    description: Force the overwrite of files without asking.
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
    description: File to write the private key (PEM format)
    type: path
    required: yes
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
    type: str
    required: yes
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
    description: The provisioner name to use.
    type: str
    required: yes
  provisioner_password_file:
    description: The path to the file containing the password to decrypt the one-time token generating key.
    type: path
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
  token:
    description: The one-time token used to authenticate with the CA in order to create the certificate.
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
  - maxhoesel.smallstep.step_cli
  - maxhoesel.smallstep.ca_connection_hybrid
"""

EXAMPLES = r"""
# See https://smallstep.com/docs/step-cli/reference/ca/certificate for more examples

- name: Request a new certificate for a given domain
  maxhoesel.smallstep.step_ca_certificate:
    token: "{{ your_token_here }}"
    name: internal.example.com
    crt_file: /tmp/mycert.crt
    key_file: /tmp/mycert.key

- name: Request a new certificate with multiple Subject Alternative Names
  maxhoesel.smallstep.step_ca_certificate:
    name: foobar
    san:
      - hello.example.com
      - 1.1.1.1
      - 10.2.3.4
    crt_file: /tmp/mycert.crt
    key_file: /tmp/mycert.key
"""

from ..module_utils.ca_connection_hybrid import connection_argspec, connection_run_args
from ..module_utils.run import run_step_cli_command
from ..module_utils.validation import check_step_cli_install
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        acme=dict(type="str"),
        contact=dict(type="list", elements="str"),
        crt_file=dict(type="path", required=True),
        curve=dict(type="str", choices=[
                   "P-256", "P-384", "P-521", "Ed25519"], aliases=["crv"]),
        force=dict(type="bool"),
        http_listen=dict(type="str"),
        k8ssa_token_path=dict(type="path"),
        key_file=dict(type="path", required=True),
        kty=dict(type="str", choices=["EC", "OKP", "RSA"]),
        name=dict(type="str", required=True, aliases=["subject"]),
        not_after=dict(type="str"),
        not_before=dict(type="str"),
        provisioner=dict(type="str", aliases=["issuer"], required=True),
        provisioner_password_file=dict(type="path", no_log=False),
        san=dict(type="list", elements="str"),
        set=dict(type="list", elements="str"),
        set_file=dict(type="path"),
        size=dict(type="int"),
        standalone=dict(type="bool"),
        token=dict(type="str", no_log=True),
        webroot=dict(type="path"),
        x5c_cert=dict(type="str"),
        x5c_key=dict(type="path"),
        step_cli_executable=dict(type="path", default="step-cli"),
    )
    result = dict(changed=False, stdout="", stderr="", msg="")
    module = AnsibleModule(argument_spec={**module_args, **connection_argspec}, supports_check_mode=True)

    check_step_cli_install(
        module, module.params["step_cli_executable"], result)

    # Positional Parameters
    params = ["ca", "certificate", module.params["name"],
              module.params["crt_file"], module.params["key_file"]]
    # Regular args
    args = ["acme", "contact", "curve", "force", "http_listen", "k8ssa_token_path", "kty", "not_after",
            "not_before", "provisioner", "provisioner_password_file", "san", "set", "set_file", "size",
            "standalone", "token", "webroot", "x5c_cert", "x5c_key"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    args = {arg: "--{a}".format(a=arg.replace("_", "-")) for arg in args}

    result = run_step_cli_command(
        module.params["step_cli_executable"], params,
        module, result, {**args, **connection_run_args}
    )
    result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
