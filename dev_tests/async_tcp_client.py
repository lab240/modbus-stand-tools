#!/usr/bin/env python3
"""Pymodbus asynchronous client example.

An example of a single threaded synchronous client.

usage: simple_client_async.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import asyncio
import time

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    ModbusException,
    pymodbus_apply_logging_config,
)

IP="192.168.16.146"
PORT=502
LOOP_COUNT_A = 300
REGISTER_COUNT = 4
#ADDRESSES = [1,2,3,4,5,6,7,8,9,10]
ADDRESSES = list(range(1, 31))
LOOP_COUNT=LOOP_COUNT_A//len(ADDRESSES)

async def run_async_simple_client(comm, host, port):
    """Run async client."""
    # activate debugging
    #pymodbus_apply_logging_config("DEBUG")

    print("get client")
    if comm == "tcp":
        client = ModbusClient.AsyncModbusTcpClient(
            host,
            port=port,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # source_address=("localhost", 0),
        )
    else:
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    await client.connect()
    # test client is connected
    assert client.connected

    start_time = time.time()

    for _i in range(LOOP_COUNT):
        for addr in ADDRESSES:
            rr = await client.read_holding_registers(0, REGISTER_COUNT, slave=addr)
            if rr.isError():
              print(f"Received Modbus library error({rr})")
              break
            print(f"{_i+1}\{LOOP_COUNT}: {rr.registers}")
    print("get and verify data")

    client.close()

    run_time = time.time() - start_time
    avg_call = (run_time / LOOP_COUNT) * 1000
    avg_call_device=avg_call / len(ADDRESSES)
    avg_register = avg_call_device / REGISTER_COUNT
    print(
        f"running {LOOP_COUNT} call (each {len(ADDRESSES)} devs with {REGISTER_COUNT} registers), took {run_time:.2f} seconds"
    )
    print(f"Averages all devs:{avg_call:.2f} ms pr call; {avg_call_device:.2f} ms pr device; {avg_register:.2f} ms pr register.")




if __name__ == "__main__":
    print(f"LOOP_COUNT={LOOP_COUNT}")
    asyncio.run(
        run_async_simple_client("tcp", IP, PORT), debug=False
    )