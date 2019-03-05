#!/bin/bash

if [[ $1 == "--help" ]] || [[ $1 == "" ]] ; then

  echo "Usage: tmistation.sh <tmiserver_ip_address> <restart_always_or_no>"
  echo ""
  echo "Notes"
  echo "1. You may/should test connection to TMIServer using ping"
  echo "2. Restart 'always' will start tmi EVERY time the computer is booted."
  echo "   To disable restart, use 'docker update --restart=no tmistation'"
  echo "   and then 'docker ps', 'docker stop <id>', to stop tmistation"
  exit 0

fi

TMI_SERVERIP=$1
RESTART=$2
HOSTNAME=$(hostname)

docker run -d \
    --restart=${RESTART} \
    -e TMI_SERVERIP=${TMI_SERVERIP} \
    --hostname=${HOSTNAME} \
    -p 6800:6800 \
    -v $(pwd):/app/public \
    --name tmistation \
    --rm \
    mgagcode/tmistation
