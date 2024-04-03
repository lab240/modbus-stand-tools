#!/bin/bash

verbose=false
helpme=false

# Задержки для кругов 1 и 2 в сек
delay1=1
delay2=0.2

port="/dev/ttyUSB0"
speed=115200

first_address=1
sensors_amount=2

registers_to_read=5
unlimited=false

mode="rtu"
tcp_address="127.0.0.1"
command="mbpoll"


help_m(){
  echo "default params: -m mtu -p /dev/ttyS3 -P 127.0.0.1"
  echo "default options: noverbose, one cycle"
  echo "--- Parameters ---"
  echo "-m (rtu|tcp)"
  echo "-p <uart_port>" 
  echo "-P <tcp_address>"
  echo "-v (verbose)"
  echo "-u (infinity circle)"
  echo "-c (modpoll(default)|mbpoll)"

}

echo "Modbus stand test ver 0.5"

while getopts ":u:D:m:P:p:c:hv" opt; do
  case $opt in
    u) unlimited=true ;;
    v) verbose=true ;;
    D) port=$OPTARG ;;
    m) mode=$OPTARG ;;
    P) tcp_address=$OPTARG ;;
    p) port=$OPTARG ;;
    c) command=$OPTARG ;;
    h) helpme=true ;;
    \?) echo "Неверный параметр: -$OPTARG" >&2; exit 1 ;;
  esac
done

if $helpme; then
 help_m
 exit 0
fi

echo "Curremnt Parameters: command=$command; port=$port; mode=$mode; tcp_address=$tcp_address"

if command -v "$command" > /dev/null; then
   echo "$command is founded"
else
   echo "ERROR: $command is not installed, exit"
   exit 1
fi

run_cycle(){
    echo "*********** READ MODBUS STAND ****************"
    # Начало цикла
    error_count=0
    last_address=$((first_address+sensors_amount-1))
    for i in $(seq $first_address $last_address)
    do
        echo "Read sensor # $i"
        # Запуск modpoll с текущим значением $i в качестве параметра -a и анализ вывода с помощью awk
        start_time=$(date +%s%N)
	if [ "$mode" == "rtu" ]; then
		output=$("$command" -m rtu -b $speed -r 1 -a $i -c $registers_to_read -1 $port 2>&1)
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
  echo $output | awk '/\[1\]:/ {print "Status:OK"; found=1}
        /time.+out/ {print "Status:!!!!!!! Error !!!!!!!!"; found=1; exit_code=1}
        END {if (!found) print "No data or unexpected response"; if (exit_code == 1) exit 2}'

	 
       	if [ $? -eq 2 ]; then
            ((error_count++))
        fi
	
	echo "Duration of mbpoll command: ${duration_ms}ms"
        sleep $delay2
    done
    
    echo "ERROROS: $error_count"
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

