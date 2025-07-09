#!/usr/bin/env python3
"""
Waveshare RS232 to CAN Device Test Script
Configure and test the RS232 to CAN converter
"""

import serial
import time
import sys

def test_serial_connection(port, baudrate=115200):
    """Test basic serial connection to the device"""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud")
        
        # Test basic communication
        ser.write(b'AT\r\n')
        time.sleep(0.1)
        response = ser.read(100)
        
        if response:
            print(f"Device response: {response.decode('utf-8', errors='ignore')}")
        else:
            print("No response from device")
        
        ser.close()
        return True
    except Exception as e:
        print(f"Error connecting to {port}: {e}")
        return False

def configure_can_device(port, baudrate=115200):
    """Configure the CAN device parameters"""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print("Configuring CAN device...")
        
        # Common AT commands for CAN configuration
        commands = [
            b'AT+RST\r\n',          # Reset device
            b'AT+UART=115200,0,0\r\n',  # Set UART parameters
            b'AT+CAN=500\r\n',      # Set CAN baud rate to 500kbps
            b'AT+FILTER=0\r\n',     # Disable filter
            b'AT+WORK=1\r\n',       # Set to transparent mode
            b'AT+SAVE\r\n'          # Save configuration
        ]
        
        for cmd in commands:
            print(f"Sending: {cmd.decode('utf-8').strip()}")
            ser.write(cmd)
            time.sleep(0.5)
            response = ser.read(100)
            if response:
                print(f"Response: {response.decode('utf-8', errors='ignore').strip()}")
            else:
                print("No response")
        
        ser.close()
        return True
    except Exception as e:
        print(f"Error configuring device: {e}")
        return False

def main():
    device_port = '/dev/tty.usbserial-1140'
    
    print("Waveshare RS232 to CAN Device Configuration")
    print("=" * 50)
    
    # Test connection
    if test_serial_connection(device_port):
        print("\n✓ Serial connection successful")
    else:
        print("\n✗ Serial connection failed")
        sys.exit(1)
    
    # Configure device
    if configure_can_device(device_port):
        print("\n✓ Device configuration completed")
    else:
        print("\n✗ Device configuration failed")
        sys.exit(1)
    
    print("\nDevice is ready for CAN communication!")
    print("Connect your CAN bus and use the device for RS232 to CAN conversion.")

if __name__ == "__main__":
    main()