#!/usr/bin/env python3

import time
import pymodbus

from pymodbus.client import ModbusSerialClient


LOOP_COUNT = 500
REGISTER_COUNT = 4
ADDRESSES = [1,2]
SERIAL_PORT="/dev/ttyUSB0"
BAUDRATE=115200
PARITY="E"

def run_sync_client_test():
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
            if rr.isError():
              print(f"Received Modbus library error({rr})")
              break
            #print(rr.registers)
    client.close()
    run_time = time.time() - start_time
    avg_call = (run_time / LOOP_COUNT) /len(ADDRESSES) * 1000
    avg_register = avg_call / REGISTER_COUNT
    print(
        f"running {LOOP_COUNT} call (each {REGISTER_COUNT} registers), took {run_time:.2f} seconds"
    )
    print(f"Averages {avg_call:.2f} ms pr call and {avg_register:.2f} ms pr register.")

if __name__ == "__main__":
    run_sync_client_test()
    