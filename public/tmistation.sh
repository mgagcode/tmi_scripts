#!/bin/bash

usage () {
  echo "Usage: tmistation.sh [flags] <command>"
  echo ""
  echo "command:"
  echo "  start                     Start TMIStation"
  echo ""
  echo "    flags, --server=, -s    (REQUIRED) TMIServer IP address. Use 'none' if no TMIServer."
  echo "           --hostname=, -h  Specify an alternative hostname for this computer (default $(hostname))"
  echo "           --restart=, -r   <always|no> (default no) 'always' will start TMIStation EVERY time the"
  echo "                            computer is booted, which is typically used on a node that"
  echo "                            is in actual deployment."
  echo "                            To disable restart, use 'docker update --restart=no tmistation'"
  echo "                            and then reboot the node."
  echo ""
  echo "  update                    Update the docker image, requires internet connection."
  echo ""
}

if [[ $1 == "--help" ]] || [[ $1 == "" ]] ; then
  usage
  exit 0
fi

# set defaults here
flag_server=not_specified
flag_hostname=(hostname)


start () {
    echo start $flag_restart
    #
    # docker run --rm and --restart commands are exclusive of each other
    #
    if [[ $flag_server == "not_specified" ]]; then
        echo "TMIServer IP address is required flag (--server)"
    elif [[ $flag_server == "none" ]]; then
        TMI_SERVERIP=127.0.0.1
    fi
    if [[ $flag_restart == "always" ]]; then
        docker run -d \
            --restart=${RESTART} \
            -e TMI_SERVERIP=${TMI_SERVERIP} \
            --hostname=${flag_hostname} \
            -p 6800:6800 \
            -v $(pwd):/app/public \
            --name tmistation \
            mgagcode/tmistation
    elif [[ $flag_restart == "no" ]]; then
        docker run -d \
            -e TMI_SERVERIP=${TMI_SERVERIP} \
            --hostname=${flag_hostname} \
            -p 6800:6800 \
            -v $(pwd):/app/public \
            --name tmistation \
            --rm \
            mgagcode/tmistation
    else
      echo Unexpected restart value, must be always or no, example: --restart=always
      exit 1
    fi
}

docker_pull () {
    echo docker pull
    docker pull mgagcode/tmistation
}

handle_command () {
  echo $1
  case $1 in
    start)
      start
      ;;

    update)
      docker_pull
      ;;

    *)
      echo Unknown Command
      usage
      exit 1
      ;;

  esac
  exit 0
}

# see https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash

while [ "$#" -gt 0 ]; do
  case "$1" in
    -r) flag_restart="$2"; shift 2;;
    -h) flag_hostname="$2"; shift 2;;

    --restart=*) flag_restart="${1#*=}"; shift 1;;
    --hostname=*) flag_hostname="${1#*=}"; shift 1;;
    --restart|--hostname) echo "$1 requires an argument" >&2; exit 1;;

    -*) echo "unknown option: $1" >&2; exit 1;;
    *) handle_command "$1"; shift 1;;
  esac
done

