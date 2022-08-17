#!/bin/bash -eu

set -o errexit # abort on nonzero exitstatus
set -o nounset # abort on unbound variable
set -o pipefail # don't hide errors within pipes

function main()
{
  readonly template="$1"; shift
  # shellcheck disable=2155
  readonly content="$(cat "$template")"

  eval "echo \"$content\""
}

main "$@"
