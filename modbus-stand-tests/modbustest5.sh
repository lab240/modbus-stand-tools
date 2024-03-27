#!/bin/bash

verbose=false
# Задержки для кругов 1 и 2 в сек
delay1=1
delay2=0.2
port="/dev/ttyS3"
speed=115200
first_address=1
registers_to_read=5
unlimited=false
sensors_amount=10
mode=rtu
tcp_address=127.0.0.1

echo "Modbus stand test"
echo "-m (rtu|tcp) -p <uart_port> -P <tcp_address> -v (verbose) -u (infinity circle)"
echo "default params: -m mtu -p /dev/ttyS3 -P 127.0.0.1"
echo "default options: noverbose, one cycle"


while getopts ":u:D:m:P::p:v:" opt; do
  case $opt in
    u) unlimited=true ;;
    u) verbose=true ;;
    D) port=$OPTARG ;;
    m) mode=$OPTARG ;;
    P) tcp_address=$OPTARG ;;
    p) port=$OPTARG ;;
    \?) echo "Неверный параметр: -$OPTARG" >&2; exit 1 ;;
  esac
done


run_cycle(){
    echo "*********** READ MODBUS STAND ****************"
    # Начало цикла
    last_address=$((first_address+sensors_amount-1))
    for i in $(seq $first_address $last_address)
    do
        echo "Read sensor # $i"
        # Запуск modpoll с текущим значением $i в качестве параметра -a и анализ вывода с помощью awk
        start_time=$(date +%s%N)
	if [ "$mode" == "rtu" ]; then
		output=$(modpoll -m rtu -b $speed -r 1 -a $i -c $registers_to_read -1 $port 2>&1)
		if $verbose; then
			echo "$output"
		fi
	elif [ "$mode" == "tcp" ]; then
		output=$(modpoll -m tcp -r 1 -a $i -c $registers_to_read -1 $tcp_address 2>&1)
		if $verbose; then
			echo "$output"
		fi
	else	
		echo "Bad parameter: $mode -m <rtu|tcp>"
	fi
	end_time=$(date +%s%N)
	duration=$((end_time - start_time)) # Длительность в наносекундах
        duration_ms=$((duration / 1000000)) # Длительность в миллисекундах
        echo $output | awk '/\[1\]\:/ {print "Status:OK"; found=1}
        /time.+out/ {print "Status:Error"; found=1}
        END {if (!found) print "No data or unexpected response"}'
	echo "Duration of mbpoll command: ${duration_ms}ms"
        sleep $delay2

    done
    echo "************************************************"
}

if $unlimited; then
  echo "Universe mode"
  while true; do
    run_cycle
    sleep $delay1
  done
else
  run_cycle
fi

