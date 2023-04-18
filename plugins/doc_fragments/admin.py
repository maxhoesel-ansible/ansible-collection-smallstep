# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class ModuleDocFragment:
    DOCUMENTATION = r'''
    options:
      admin_cert:
        description: Admin certificate (chain) in PEM format to store in the 'x5c' header of a JWT.
        type: path
      admin_key:
        description: Private key file, used to sign a JWT,corresponding to the admin certificate that will be stored in the 'x5c' header.
        type: path
      admin_provisioner:
        description: The provisioner name to use for generating admin credentials.
        type: str
        aliases:
          - admin_issuer
      admin_subject:
        description: The admin subject to use for generating admin credentials.
        type: str
        aliases:
          - admin_name
      admin_password_file:
        description: The path to the file containing the password to encrypt or decrypt the private key.
        type: path
    '''
