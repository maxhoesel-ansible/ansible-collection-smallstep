#!/usr/bin/env bash
set -eu
set -o pipefail

# use a tmpdir to install collections for doc builds
mkdir -p tmp/collections
rm -rf tmp/*.tar.gz
export ANSIBLE_COLLECTIONS_PATH=./tmp/collections
(
    cd ..
    ansible-galaxy collection build --output-path docs/tmp
)
ansible-galaxy collection install --force tmp/*.tar.gz -p $ANSIBLE_COLLECTIONS_PATH

# delete old generated docs
rm -rf rst/collections
chmod og-w rst  # antsibull-docs wants that directory only readable by itself

antsibull-docs \
    --config-file antsibull-docs.cfg \
    collection \
    --use-current \
    --dest-dir rst \
    maxhoesel.smallstep

# Build Sphinx site
cd rst && sphinx-build -M html ./ ../build -c . -W --keep-going
