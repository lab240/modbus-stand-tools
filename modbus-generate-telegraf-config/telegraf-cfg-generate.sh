#!/bin/bash

#ip=192.168.16.199
ip=127.0.0.1
first_dev_num=1
last_dev_num=30
timeout="10s"

for i in $(seq $first_dev_num $last_dev_num)
do

	echo "
[[inputs.modbus]]
  name = \"modbusstand_dev$i\"
  slave_id = $i
  timeout = \"$timeout\"
  controller = \"tcp://$ip:502\"
"
echo '  holding_registers = [
    { name = "num", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [0]},
    { name = "hours", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [1]},
    { name = "min", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [2]},
    { name = "sec", byte_order = "AB",   data_type = "INT16", scale=1.0,  address = [3]},
  ]
'
done
