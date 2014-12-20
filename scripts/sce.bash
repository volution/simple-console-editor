#!/bin/bash

set -e -E -u -o pipefail -o noclobber -o noglob +o braceexpand || exit 1
trap 'printf "[ee] failed: %s\n" "${BASH_COMMAND}" >&2' ERR || exit 1

_root="$( dirname -- "$( readlink -e -- "${0}/.." )" )"
_scripts="${_root}/scripts"
_sources="${_root}/sources"

test -f "${_sources}/sce.py"

if test "${#}" -eq 0 ; then
	exec "${_scripts}/python" -E -O -O -u "${_sources}/sce.py"
else
	exec "${_scripts}/python" -E -O -O -u "${_sources}/sce.py" "${@}"
fi

exit 1
