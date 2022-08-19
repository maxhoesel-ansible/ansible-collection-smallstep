# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# This file only contains a selection of the most common options. For a full list see the
# documentation:
# http://www.sphinx-doc.org/en/master/config

# pylint: skip-file

# Yes, this is a horrendous way to extract our collection version.
# Yes, it works.
# If you'd like to figure out how to import that module, be my guest!
with open("../../plugins/module_utils/constants.py") as f:
    exec(f.read())

version = COLLECTION_VERSION
release = version

project = 'Ansible collections'
copyright = 'Ansible contributors'

title = 'maxhoesel.smallstep Collection Documentation'
html_short_title = 'maxhoesel.smallstep docs'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx_antsibull_ext']

pygments_style = 'ansible'

highlight_language = 'YAML+Jinja'

html_theme = 'sphinx_ansible_theme'
html_show_sphinx = False

display_version = False

html_use_smartypants = True
html_use_modindex = False
html_use_index = False
html_copy_source = False

intersphinx_mapping = {
    'python': ('https://docs.python.org/2/', (None, '../python2.inv')),
    'python3': ('https://docs.python.org/3/', (None, '../python3.inv')),
    'jinja2': ('http://jinja.palletsprojects.com/', (None, '../jinja2.inv')),
    'ansible_devel': ('https://docs.ansible.com/ansible/devel/', (None, '../ansible_devel.inv')),
    # If you want references to resolve to a released Ansible version (say, `5`), uncomment and replace X by this version:
    # 'ansibleX': ('https://docs.ansible.com/ansible/X/', (None, '../ansibleX.inv')),
}

default_role = 'any'

nitpicky = True
