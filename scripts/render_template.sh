#!/usr/bin/env bash

set -eu
set -o pipefail

function main()
{
  readonly template="$1"; shift
  # shellcheck disable=2155
  readonly content="$(cat "$template")"

  eval "echo \"$content\""
}

main "$@"
