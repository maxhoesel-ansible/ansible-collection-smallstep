#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

# Create collection documentation into temporary directory
rm -rf temp-rst
mkdir -p temp-rst

# Temporarily create and install collection
rm -rf ./ansible_collections
mkdir -p ./ansible_collections
export ANSIBLE_COLLECTIONS_PATHS=./docs:$ANSIBLE_COLLECTIONS_PATHS
(
    cd ..
    ansible-galaxy collection build --output-path ./docs --force
    ansible-galaxy collection install -p ./docs docs/maxhoesel-smallstep-*.tar.gz --force
)

antsibull-docs collection \
    --use-current \
    --no-use-html-blobs \
    --breadcrumbs \
    --indexes \
    --dest-dir temp-rst \
    maxhoesel.smallstep

# Copy collection documentation into source directory
rsync -cprv --delete-after temp-rst/collections/ rst/collections/

# Build Sphinx site
cd rst && sphinx-build -M html ./ ../build -c . -W --keep-going
