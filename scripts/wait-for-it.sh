# scripts/wait-for-it.sh
#!/usr/bin/env bash
# Скрипт для проверки доступности хоста и порта
# Использование: ./wait-for-it.sh host:port [-t timeout] [-- command args]

cmdname=$(basename $0)

# Использование
echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $cmdname host:port [-t timeout] [-- command args]
    -t TIMEOUT                      Timeout in seconds, zero for no timeout
    -- COMMAND ARGS                 Command with args to run after the test finishes
USAGE
    exit 1
}

wait_for()
{
    local wait_host=$1
    local wait_port=$2
    local timeout=$3
    
    if [[ $TIMEOUT -gt 0 ]]; then
        echoerr "$cmdname: waiting $TIMEOUT seconds for $wait_host:$wait_port"
    else
        echoerr "$cmdname: waiting for $wait_host:$wait_port without a timeout"
    fi
    
    start_ts=$(date +%s)
    while :
    do
        (echo > /dev/tcp/$wait_host/$wait_port) >/dev/null 2>&1
        result=$?
        if [[ $result -eq 0 ]]; then
            end_ts=$(date +%s)
            echoerr "$cmdname: $wait_host:$wait_port is available after $((end_ts - start_ts)) seconds"
            break
        fi
        sleep 1
    done
    return $result
}

# Процесс проверки
TIMEOUT=15
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        hostport=(${1//:/ })
        HOST=${hostport[0]}
        PORT=${hostport[1]}
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [[ $TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --)
        shift
        break
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done

wait_for "$HOST" "$PORT" "$TIMEOUT"