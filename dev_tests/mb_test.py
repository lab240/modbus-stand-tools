#!/usr/bin/env python3

import time
import pymodbus
import array as arr
import asyncio

from pymodbus.client import AsyncModbusSerialClient, ModbusSerialClient


VERSION="0.01"

LOOP_COUNT = 1
REGISTER_COUNT = 10
PAUSE = 40 #pause in ms
ADDRESSES = arr.array('i')
SERIAL_PORT="/dev/ttyS3"
BAUDRATE=115200
PARITY="E"

FIRST_REGISTER=31
LAST_REGISTER=90

#METHOD="ASYNC"
METHOD="SYNC"

DEBUG=1

print(f"**********  Modbus test tool ver {VERSION} ********************")
print(f"PORT={SERIAL_PORT}, BAUDRATE={BAUDRATE}, PARITY={PARITY}")
print(f"PAUSE={PAUSE}ms, FIRST_ADDRESS={FIRST_REGISTER}, LAST_ADDRES={LAST_REGISTER}")
print(f"***************************************************************")


errors=0

def fill_array(first_element, last_element):
    for i in range(first_element, last_element+1):
       ADDRESSES.append(i)

def run_sync_client_test():
    global errors
    """Run sync client."""
    print("--- Testing sync reading registers by pymodbus")
    client = ModbusSerialClient(
        SERIAL_PORT,
        baudrate=BAUDRATE,
        parity=PARITY
    )
    client.connect()
    assert client.connected

    start_time = time.time()
    for _i in range(LOOP_COUNT):
        for addr in ADDRESSES:
            rr = client.read_holding_registers(0, REGISTER_COUNT, slave=addr)
            time.sleep(PAUSE/1000);
            if rr.isError():
              print(f"Received Modbus library error({rr})")
              errors+=1
            else: 
                if DEBUG: print(f"{addr}, {rr.registers}")
    
    client.close()
    run_time = time.time() - start_time
    avg_call = (run_time / LOOP_COUNT) /len(ADDRESSES) * 1000
    avg_register = avg_call / REGISTER_COUNT
    print(
        f"running {LOOP_COUNT} call (each {REGISTER_COUNT} registers), took {run_time*1000} ms"
    )
    print(f"Averages {avg_call:.2f} ms pr call and {avg_register:.2f} ms pr register.")


async def run_async_client_test():
    """Run async client."""
    print("--- Testing async client v3.4.1")
    global errors
    client = AsyncModbusSerialClient(
        SERIAL_PORT,
        baudrate=BAUDRATE,
        parity=PARITY
    )
    await client.connect()
    assert client.connected

    start_time = time.time()
    for _i in range(LOOP_COUNT):
        for addr in ADDRESSES:
            rr = await client.read_holding_registers(0, REGISTER_COUNT, slave=addr)
            time.sleep(PAUSE/1000)
            if rr.isError():
              print(f"Received Modbus library error({rr})")
              errors+=1
            else:
              # print(rr.registers)
              print(addr)
              # print('.')
    client.close()
    run_time = time.time() - start_time
    avg_call = (run_time / LOOP_COUNT) / len(ADDRESSES) * 1000
    avg_register = avg_call / REGISTER_COUNT
    print(
        f"running {LOOP_COUNT} call (each {REGISTER_COUNT} registers), took {run_time:.2f} seconds"
    )
    print(f"Averages {avg_call:.2f} ms pr call and {avg_register:.2f} ms pr register.")

if __name__ == "__main__":
    #fill_array(31,81)
    fill_array(FIRST_REGISTER,LAST_REGISTER)
    if DEBUG: print (ADDRESSES)
    if METHOD=="SYNC":
        print("Run sync test !")
        run_sync_client_test()
    if METHOD=="ASYNC":
        print("Run async test !")
        asyncio.run(run_async_client_test())
    print(f"Errors: {errors}")
    
