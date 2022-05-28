# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os

CA_CONFIG = f"{os.environ.get('STEPPATH', os.environ['HOME'] + '/.step')}/config/ca.json"

connection_argspec = dict(
    ca_config=dict(type="path", default=CA_CONFIG)
)

# Mapping of connection parameters to step-cli arguments
connection_run_args = {
    "ca_config": "--ca-config"
}
