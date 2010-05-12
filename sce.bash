#!/bin/bash

set -e -u -o pipefail || exit 1

sources="$( dirname "$( readlink -f "${0}" )" )"

test -f "${sources}/sce.py"

if test "${#}" -eq 0
then
	exec "${sources}/python" -E -O -O -u "${sources}/sce.py"
else
	exec "${sources}/python" -E -O -O -u "${sources}/sce.py" "${@}"
fi

exit 1
