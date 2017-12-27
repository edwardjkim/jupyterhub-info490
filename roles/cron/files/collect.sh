#!/bin/bash

if [[ $# -eq 0 ]]
then
  echo 'Usage: ./collect.sh [WEEK NUMBER]'
  exit 0
fi

N=$1

CURRENT_TIME=$(date +\%Y\%m\%d\%H\%M\%S)

SAVE_DIR="/export/submitted"
ASSIGN_OUTFILE="$SAVE_DIR/week$N.$CURRENT_TIME.tar.gz"

if [ ! -d "$SAVE_DIR" ]
then
  mkdir -p "$SAVE_DIR"
fi

find /export/home -type f -name core.* -delete
find /export/exchange -type f -name core.* -delete

(cd /export && tar cvzf $ASSIGN_OUTFILE exchange/*/info490-fa17-assignments/inbound/data_scientist+week$N*)
