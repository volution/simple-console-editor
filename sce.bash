#!/bin/bash

set -e -E -u -o pipefail -o noclobber -o noglob +o braceexpand || exit 1
trap 'printf "[ee] failed: %s\n" "${BASH_COMMAND}" >&2' ERR || exit 1

sources="$( dirname -- "$( readlink -e -- "${0}" )" )"

test -f "${sources}/sce.py"

if test "${#}" -eq 0
then
	exec "${sources}/python" -E -O -O -u "${sources}/sce.py"
else
	exec "${sources}/python" -E -O -O -u "${sources}/sce.py" "${@}"
fi

exit 1
