# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Connection parameters for modules that can interact both with a local and remote CA, such as ca_certificate
    DOCUMENTATION = r'''
    requirements:
      - A C(step-ca) server, either remote or local
      - If running locally, this module should run as the same user that the step-ca process is running as to prevent permission issues
    options:
      ca_config:
        description: >
          The path to the certificate authority configuration file on the host.
          Used if the module is run with I(offline) set (local mode).
        type: path
      ca_url:
        description: >
          URI of the targeted Step Certificate Authority.
          Used if the module is run in online mode (default) and the hosts C(step-cli) is not configured to trust the CA.
        type: str
      offline:
        description: >
          Don't contact the CA. Offline mode uses the configuration, certificates, and keys created with step ca init,
          but can accept a different configuration file using the I(ca_config) flag.
        type: bool
      root:
        description: >
          The path to the PEM file used as the root certificate authority.
          Used if the module is run in online mode (default) and the hosts C(step-cli) is not configured to trust the CA.
        type: path
    '''
