# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
    requirements:
      - C(step-cli) must be installed on the remote host. You can set the executable name/path with I(step_cli_executable).
    options:
      step_cli_executable:
        description: Name (or absolute path) of the C(step-cli) executable to use
        default: step-cli
        type: path
    '''
