#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

# Create collection documentation into temporary directory
rm -rf temp-rst
mkdir -p temp-rst
chmod og-w temp-rst  # antsibull-docs wants that directory only readable by itself
antsibull-docs \
    --config-file antsibull-docs.cfg \
    collection \
    --use-current \
    --dest-dir temp-rst \
    maxhoesel.smallstep

# Copy collection documentation into source directory
rsync -cprv --delete-after temp-rst/collections/ rst/collections/

# Build Sphinx site
cd rst && sphinx-build -M html ./ ../build -c . -W --keep-going
