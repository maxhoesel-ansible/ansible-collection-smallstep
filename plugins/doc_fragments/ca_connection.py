# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class ModuleDocFragment:
    # Connection parameters for modules that only interact with a local CA, such as ca_provisioner(_claims)
    DOCUMENTATION = r'''
    options:
      ca_url:
        description: >
          URI of the targeted Step Certificate Authority.
          Used if the module is run in online mode (default) and the hosts C(step-cli) is not configured to trust the CA.
        type: str
      root:
        description: >
          The path to the PEM file used as the root certificate authority.
          Used if the module is run in online mode (default) and the hosts C(step-cli) is not configured to trust the CA.
        type: path
      ca_config:
        description: The path to the certificate authority configuration file on the host.
        type: path
      offline:
        description: >
          Don't contact the CA. Offline mode uses the configuration, certificates, and keys created with step ca init,
          but can accept a different configuration file using the I(ca_config) flag.
        type: bool
    '''
