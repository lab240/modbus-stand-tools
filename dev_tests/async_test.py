#!/usr/bin/env python3

import asyncio
import time
import pymodbus

#from pymodbus import FramerType
from pymodbus.client import AsyncModbusSerialClient, ModbusSerialClient


LOOP_COUNT = 1000
REGISTER_COUNT = 4
ADDRESSES = [1]
SERIAL_PORT="/dev/ttyUSB0"
BAUDRATE=115200
PARITY="E"

async def run_async_client_test():
    """Run async client."""
    print("--- Testing async client v3.4.1")
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
            if rr.isError():
              print(f"Received Modbus library error({rr})")
              break
            time.sleep(0.001)
            #print(rr.registers)
    client.close()
    run_time = time.time() - start_time
    avg_call = (run_time / LOOP_COUNT) / len(ADDRESSES) * 1000
    avg_register = avg_call / REGISTER_COUNT
    print(
        f"running {LOOP_COUNT} call (each {REGISTER_COUNT} registers), took {run_time:.2f} seconds"
    )
    print(f"Averages {avg_call:.2f} ms pr call and {avg_register:.2f} ms pr register.")


if __name__ == "__main__":
    asyncio.run(run_async_client_test())
