# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os

CA_CONFIG = "{steppath}/config/ca.json".format(steppath=os.environ.get("STEPPATH", os.environ["HOME"] + "/.step"))

connection_argspec = dict(
    ca_config=dict(type="path", default=CA_CONFIG)
)

# Mapping of connection parameters to step-cli arguments
connection_run_args = {
    "ca_config": "--ca-config"
}
