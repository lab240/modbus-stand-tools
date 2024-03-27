# Утилиты для работы с стендом Modbus

## Скрипт генерации конфига telegraf для стенда

>modbus-generate-telegraf-config/telegraf-cfg-generate.sh

telegraf-cfg-generate.sh - простой скрипт, который генерирует часть [input] конфига для telegraf стенда датчиков modbus tcp.

Скрипт появился, когда стало понятно, что конфиг состояит из 30 одинаковых секций вида

```toml
[[inputs.modbus]]
  name = "modbusstand_dev1"
  slave_id = 1
  timeout = "10s"
  controller = "tcp://192.168.16.199:502"

  holding_registers = [
    { name = "num", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [0]},
    { name = "hours", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [1]},
    { name = "min", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [2]},
    { name = "sec", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [3]},
  ]
```
Меняется только IP, название датчика, slave_id.

Отредактируйте скрипт, задав переменные:

```bash
ip=127.0.0.1    # ip для опроса modbus
first_dev_num=1 # генерить подряд с этого номера  устройства
last_dev_num=30 # до этого номера устройства
timeout="10s"   # таймаут опроса  (будет одинаковый для всех устройств)
```

Запустите скрипт

```bash

sh telegraf-cfg-generate.sh 

```

Проверьте тчо на жкране все веро и можно запускать с выводом в файл 

```bash

sh telegraf-cfg-generate.sh >telegraf-stand30.conf 

```

Telegraf можно запускать с параметром основного конфига и сгенерированного конфига

```bash
telegraf --config /etc/telegraf/telegraf.conf  --config ./telegraf-stand30.conf 
```





