from ansible.module_utils.common import validation

args = dict(
    admin_cert=dict(type="path"),
    admin_key=dict(type="path"),
    admin_provisioner=dict(type="str", aliases=["admin_issuer"]),
    admin_subject=dict(type="str", aliases=["admin_name"]),
    admin_password_file=dict(type="path", no_log=False)
)

param_spec = {key: f"--{key.replace('_', '-')}" for key in args}


def check_argspec(module, result):
    try:
        validation.check_required_together(["admin_cert", "admin_key"], module.params)
    except ValueError:
        result["msg"] = "admin_cert and admin_key must be specified together"
        module.fail_json(**result)


def is_present(module):
    return bool(module.params["admin_cert"])
