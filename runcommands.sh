#!/bin/bash
# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export DATABASE_URL="postgres://localhost/$USER"
export DEBUG=1
export SECRET_KEY="I_AM_SO_SECRET_OMG_OMG_OMG_OMG_123!@ENTROPY_YO"

[ -f runcommands.local.sh ] && source runcommands.local.sh || true

unset root
