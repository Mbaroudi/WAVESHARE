#!/usr/bin/env python3
"""
Advanced Waveshare RS232 to CAN Device Test
Try different baud rates and command formats
"""

import serial
import time
import sys

def test_multiple_baud_rates(port):
    """Test connection with different baud rates"""
    baud_rates = [9600, 19200, 38400, 57600, 115200, 230400, 460800]
    
    for baud in baud_rates:
        print(f"\nTesting baud rate: {baud}")
        try:
            ser = serial.Serial(port, baud, timeout=2)
            
            # Try different command formats
            commands = [
                b'AT\r\n',
                b'AT\r',
                b'AT\n',
                b'AT',
                b'+++',
                b'AT+VER\r\n',
                b'AT+INFO\r\n'
            ]
            
            for cmd in commands:
                ser.write(cmd)
                time.sleep(0.5)
                response = ser.read(1000)
                if response:
                    print(f"✓ Response at {baud} baud with '{cmd}': {response}")
                    ser.close()
                    return baud, cmd
            
            ser.close()
        except Exception as e:
            print(f"Error at {baud} baud: {e}")
    
    return None, None

def scan_for_device_info(port, baud=115200):
    """Scan for device information"""
    try:
        ser = serial.Serial(port, baud, timeout=2)
        
        # Try to get device information
        info_commands = [
            b'AT+VER\r\n',
            b'AT+INFO\r\n', 
            b'AT+STATUS\r\n',
            b'AT+HELP\r\n',
            b'AT+?\r\n',
            b'?\r\n',
            b'help\r\n'
        ]
        
        for cmd in info_commands:
            print(f"Trying: {cmd.decode('utf-8').strip()}")
            ser.write(cmd)
            time.sleep(1)
            response = ser.read(1000)
            if response:
                print(f"Response: {response.decode('utf-8', errors='ignore')}")
                print("-" * 40)
        
        ser.close()
    except Exception as e:
        print(f"Error scanning device: {e}")

def main():
    device_port = '/dev/tty.usbserial-1140'
    
    print("Advanced Waveshare RS232 to CAN Device Test")
    print("=" * 50)
    
    # Test multiple baud rates
    working_baud, working_cmd = test_multiple_baud_rates(device_port)
    
    if working_baud:
        print(f"\n✓ Found working configuration: {working_baud} baud, command: {working_cmd}")
        scan_for_device_info(device_port, working_baud)
    else:
        print("\n⚠ No response from device at any baud rate")
        print("This could mean:")
        print("1. Device is in a different mode (CAN mode vs AT command mode)")
        print("2. Device requires hardware reset")
        print("3. Device uses different command protocol")
        print("4. Hardware connection issue")
        
        # Try scanning anyway at default baud
        print("\nScanning at default 115200 baud...")
        scan_for_device_info(device_port)

if __name__ == "__main__":
    main()