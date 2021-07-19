# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

connection_argspec = dict(
    ca_config=dict(type="path"),
    ca_url=dict(type="str"),
    offline=dict(type="bool"),
    root=dict(type="path"),
)

# Mapping of connection parameters to step-cli arguments
connection_run_args = {
    "ca_config": "--ca-config",
    "ca_url": "--ca-url",
    "offline": "--offline",
    "root": "--root",
}
