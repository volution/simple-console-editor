#!/bin/bash

export PYTHONPATH="$( dirname "$( realpath "${0}" )" )" || exit 1
exec python2.5 -m sce - "${@}" || exit 1
exit 1
