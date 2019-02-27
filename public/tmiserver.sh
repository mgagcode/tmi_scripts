#!/bin/bash

if [[ $1 == "--help" ]] || [[ $1 == "" ]] ; then

  echo "Usage: tmiserver.sh <restart_always_or_no>"
  echo ""
  echo "Notes"
  echo "1. Restart 'always' will start tmi EVERY time the computer is booted."
  echo "   To disable restart, use 'docker update --restart=no tmistation'"
  echo "   and then 'docker ps', 'docker stop <id>', to stop tmistation"
  exit 0

fi

RESTART=$1
HOSTNAME=$(hostname)

docker run -d \
    --net tminet \
    --hostname=${HOSTNAME} \
    --restart=${RESTART} \
    -p 6600:6600 \
    -v $(pwd):/app/public \
    --name tmiserver \
    mgagcode/tmiserver
