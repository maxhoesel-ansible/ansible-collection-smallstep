# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

args = dict(
    ca_url=dict(type="str"),
    root=dict(type="path"),
    ca_config=dict(type="path"),
    offline=dict(type="bool"),
)

# Mapping of connection parameters to step-cli arguments
param_spec = {key: f"--{key.replace('_', '-')}" for key in args}


def check_argspec(module, result):
    if module.params["offline"] and (module.params["ca_url"] or module.params["root"]):
        result["msg"] = "ca_config/offline and root/ca_url are mutually exclusive"
        module.fail_json(**result)


def is_local(module):
    return True if module.params["offline"] or module.params["ca_config"] else False


def is_remote(module):
    return not is_local(module)
