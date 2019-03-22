#!/usr/bin/env bash

usage () {
  echo "Usage: tmiserver.sh [flags] <command>"
  echo ""
  echo "command:"
  echo "  start                     Start TMIServer"
  echo ""
  echo "    flags, --restart=, -r   <always|no> (default no) 'always' will start TMIServer EVERY time the"
  echo "                            computer is booted, which is typically used on a node that"
  echo "                            is in actual deployment."
  echo "                            To disable restart, use 'docker update --restart=no tmiserver'"
  echo "                            and then reboot the node."
  echo ""
  echo "  update                    Update the docker images (both TMIServer & TMIStation), requires internet connection."
  echo "                            You will need to restart TMIServer with the start command."
  echo ""
  echo "  stop                      Stop TMIServer"
  echo ""
}

if [[ $1 == "--help" ]] || [[ $1 == "" ]] ; then
  usage
  exit 0
fi

# set defaults here
flag_restart=no

start () {
    echo start TMIServer: $flag_restart
    #
    # docker run --rm and --restart commands are exclusive of each other
    #
    if [[ ${flag_restart} != "always" ]] && [[ ${flag_restart} != "no" ]]; then
        echo "--restart= must be always or no"
        exit 1
    fi
    docker network create tminet 2> /dev/null
    docker stop tmiserver 2> /dev/null
    docker rm tmiserver 2> /dev/null
    if [[ $flag_restart == "always" ]]; then
        docker run -d \
            --net tminet \
            --hostname=${HOSTNAME} \
            --restart=${flag_restart} \
            -p 6600:6600 \
            -v $(pwd):/app/public \
            --name tmiserver \
            mgagcode/tmiserver
    elif [[ $flag_restart == "no" ]]; then
        docker run -d \
            --net tminet \
            --hostname=${HOSTNAME} \
            -p 6600:6600 \
            -v $(pwd):/app/public \
            --name tmiserver \
            --rm \
            mgagcode/tmiserver
    fi
}

docker_pull () {
    echo docker pull
    docker pull mgagcode/tmiserver
    docker update --restart=no tmiserver
    docker stop tmiserver
    docker container rm tmiserver
    echo
    echo Now restart tmiserver: ./tmiserver.sh --restart=always start
}

stop () {
    docker update --restart=no tmiserver
    docker stop tmiserver
    docker container rm tmiserver
}

handle_command () {
  case $1 in
    start)
      start
      ;;

    update)
      docker_pull
      ;;

    stop)
      stop
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

    --restart=*) flag_restart="${1#*=}"; shift 1;;
    --restart) echo "$1 requires an argument" >&2; exit 1;;
#    --restart|--pidfile) echo "$1 requires an argument" >&2; exit 1;;  example of adding more

    -*) echo "unknown option: $1" >&2; exit 1;;
    *) handle_command "$1"; shift 1;;
  esac
done
