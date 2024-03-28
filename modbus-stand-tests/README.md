# Скрипт проверки датчиков стенда

```sh modbustest5.sh```

> [!TIP]  
>Скрипт использует утилиту modpoll.
>
>Скачать можно по ссылке: https://www.modbusdriver.com/modpoll.html

Скрипт проверяет отклик всех датчиков стенда по Modbus RTU или Modbus MTU. Протестирован на Linux. 

Можно отредактировать переменные запуска в начале скрипта

```bash
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
```

Также переменные можно переопределить через параметры запуска

```bash
echo "Modbus stand test"
echo "-m (rtu|tcp) -p <uart_port> -P <tcp_address> -v (verbose) -u (infinity circle)"
echo "default params: -m mtu -p /dev/ttyS3 -P 127.0.0.1"
echo "default options: noverbose, one cycle"
```

### Параметры

- m: выбор как опрашивать стенд. 

> [!TIP]   
>Чтобы опрашивать стенд по Modbus TCP необходимо запустить шлюз mbusd для трансляции запросов из Modbus RTU в Modbus TCP. 
>
>Ссылка на mbusd: https://github.com/3cky/mbusd
>
>Как поставить mbusd на Armbian: https://napiworld.ru/software/armbian-tune#%D1%81%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D0%B8%D1%80%D1%83%D0%B5%D0%BC-mbusd

- v: выводить больше информации

- u: сделать бесконечный цикл опроса

- p: задать устройство последовательного порта

- P: задать IP адрес опроса по Modbus TCP


Если параметры на заданы, скрипт принимает значения по умолчанию в шапке скрипта.

### Пример работы скрипта

```bash
root@napi-rk3308b-s:~# sh modbustest5.sh 
Modbus stand test
-m (rtu|tcp) -p <uart_port> -P <tcp_address> -v (verbose) -u (infinity circle)
default params: -m mtu -p /dev/ttyS3 -P 127.0.0.1
default opions: noverbose,one cycle
*********** READ MODBUS STAND ****************
Read sensor # 1
Status:OK
Duration of mbpoll command: 38ms
Read sensor # 2
Status:OK
Duration of mbpoll command: 36ms
Read sensor # 3
Status:OK
Duration of mbpoll command: 32ms
Read sensor # 4
Status:OK
Duration of mbpoll command: 43ms
Read sensor # 5
Status:OK
Duration of mbpoll command: 37ms
Read sensor # 6
Status:OK
Duration of mbpoll command: 37ms
Read sensor # 7
Status:OK
Duration of mbpoll command: 38ms
Read sensor # 8
Status:OK
Duration of mbpoll command: 40ms
Read sensor # 9
Status:OK
Duration of mbpoll command: 32ms
Read sensor # 10
Status:OK
Duration of mbpoll command: 33ms
```
Для опроса датчиков также подойдет утилита mbpoll, которая находится в стандартных репозиториях Linux. Просто в теле скрипта замените `modpoll` на `mbpol`.
