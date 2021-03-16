# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
    options:
      ca_config:
        description: The path to the certificate authority configuration file.
        type: path
      ca_url:
        description: URI of the targeted Step Certificate Authority.
        type: str
      offline:
        description: >
          Don't contact the CA. Offline mode uses the configuration, certificates, and keys created with step ca init,
          but can accept a different configuration file using --ca-config flag.
        type: bool
    '''
