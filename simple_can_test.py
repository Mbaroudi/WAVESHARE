#!/usr/bin/env python3
"""
Simple CAN device test with short timeouts
"""

import serial
import time

def quick_test(port):
    """Quick test of the device"""
    try:
        ser = serial.Serial(port, 115200, timeout=0.5)
        print(f"Connected to {port}")
        
        # Send a simple AT command
        ser.write(b'AT\r\n')
        time.sleep(0.2)
        response = ser.read(100)
        
        print(f"Raw response: {response}")
        if response:
            print(f"Decoded: {response.decode('utf-8', errors='ignore')}")
        
        ser.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    quick_test('/dev/tty.usbserial-1140')