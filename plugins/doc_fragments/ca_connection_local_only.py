# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Connection parameters for modules that only interact with a local CA, such as ca_provisioner(_claims)
    DOCUMENTATION = r'''
    requirements:
      - A local initialized step-ca server
      - This module should run as the same user that the step-ca process is running as to prevent permission issues
    options:
      ca_config:
        description: The path to the certificate authority configuration file on the host.
        type: path
        default: CI($STEPPATH)/config/ca.json
    '''
