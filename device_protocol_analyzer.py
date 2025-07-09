#!/usr/bin/env python3
"""
Device Protocol Analyzer
Analyze communication patterns and determine the correct protocol
"""

import serial
import time
import threading
from datetime import datetime


class ProtocolAnalyzer:
    def __init__(self, port='/dev/tty.usbserial-1140'):
        self.port = port
        self.serial_conn = None
        self.monitoring = False
        
    def connect(self):
        """Connect to device"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
            print(f"✓ Connected to {self.port}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def test_baud_rates(self):
        """Test different baud rates"""
        baud_rates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
        
        for baud in baud_rates:
            print(f"\nTesting baud rate: {baud}")
            try:
                if self.serial_conn:
                    self.serial_conn.close()
                
                self.serial_conn = serial.Serial(
                    port=self.port,
                    baudrate=baud,
                    timeout=2
                )
                
                # Test various command formats
                test_commands = [
                    b'AT\r\n',
                    b'AT+VER\r\n',
                    b'AT+INFO\r\n',
                    b'?\r\n',
                    b'help\r\n',
                    b'\x01\x02\x03\x04',  # Binary command
                    b'+++',  # Escape sequence
                    b'AT+RST\r\n'
                ]
                
                for cmd in test_commands:
                    self.serial_conn.write(cmd)
                    time.sleep(0.5)
                    
                    if self.serial_conn.in_waiting > 0:
                        response = self.serial_conn.read(self.serial_conn.in_waiting)
                        print(f"  Command: {cmd} -> Response: {response}")
                        
                        # If we get a response, this might be the right baud rate
                        if len(response) > 0:
                            print(f"  *** Possible working baud rate: {baud} ***")
                            return baud
                
                self.serial_conn.close()
                
            except Exception as e:
                print(f"  Error at {baud}: {e}")
        
        return None
    
    def sniff_traffic(self, duration=30):
        """Sniff traffic for a specified duration"""
        if not self.serial_conn or not self.serial_conn.is_open:
            return
        
        print(f"Sniffing traffic for {duration} seconds...")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                if self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read(self.serial_conn.in_waiting)
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    # Display both hex and ASCII
                    hex_data = data.hex()
                    ascii_data = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
                    
                    print(f"[{timestamp}] HEX: {hex_data}")
                    print(f"[{timestamp}] ASCII: {ascii_data}")
                    print("-" * 50)
            except Exception as e:
                print(f"Error reading data: {e}")
            
            time.sleep(0.1)
    
    def send_raw_data(self, data):
        """Send raw data to device"""
        if not self.serial_conn:
            return
        
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            self.serial_conn.write(data)
            self.serial_conn.flush()
            
            time.sleep(0.5)
            
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting)
                print(f"Sent: {data.hex()}")
                print(f"Response: {response.hex()}")
                print(f"ASCII: {''.join(chr(b) if 32 <= b <= 126 else '.' for b in response)}")
                return response
            else:
                print(f"Sent: {data.hex()}, No response")
                return None
                
        except Exception as e:
            print(f"Error sending data: {e}")
            return None
    
    def test_can_frame_formats(self):
        """Test different CAN frame formats"""
        print("Testing CAN frame formats...")
        
        # Test different frame formats based on typical CAN protocols
        test_frames = [
            # Standard CAN frame format
            b'\x12\x34\x08\x01\x02\x03\x04\x05\x06\x07\x08',
            
            # Extended CAN frame format
            b'\x80\x00\x12\x34\x08\x01\x02\x03\x04\x05\x06\x07\x08',
            
            # Transparent mode data
            b'\x01\x02\x03\x04\x05\x06\x07\x08',
            
            # Modbus RTU frame
            b'\x01\x03\x00\x00\x00\x01\x84\x0A',
            
            # ASCII hex format
            b'T12345678\r',
            
            # Binary format with header
            b'\xAA\x55\x12\x34\x08\x01\x02\x03\x04\x05\x06\x07\x08\x0D\x0A'
        ]
        
        for i, frame in enumerate(test_frames):
            print(f"\nTest frame {i+1}: {frame.hex()}")
            response = self.send_raw_data(frame)
            if response:
                print(f"Got response - might be correct format!")
            time.sleep(1)
    
    def analyze_device_protocol(self):
        """Comprehensive protocol analysis"""
        print("=== Device Protocol Analysis ===")
        
        if not self.connect():
            return
        
        try:
            # Test 1: Try different baud rates
            print("\n1. Testing baud rates...")
            working_baud = self.test_baud_rates()
            
            if working_baud:
                print(f"Found working baud rate: {working_baud}")
                # Reconnect at working baud rate
                self.serial_conn.close()
                self.serial_conn = serial.Serial(
                    port=self.port,
                    baudrate=working_baud,
                    timeout=2
                )
            
            # Test 2: Sniff for incoming traffic
            print("\n2. Sniffing for incoming traffic...")
            self.sniff_traffic(5)
            
            # Test 3: Test CAN frame formats
            print("\n3. Testing CAN frame formats...")
            self.test_can_frame_formats()
            
            # Test 4: Try proprietary commands
            print("\n4. Testing proprietary commands...")
            proprietary_commands = [
                b'\xAA\x55\x01\x00\x00\x00\x00\x00\x00\x00\x00\x0D\x0A',  # Waveshare format
                b'\x5A\xA5\x06\x83\x00\x00\x01',  # Another format
                b'\xFF\xFF\x01\x02\x03\x04',  # Simple format
                b'WS-CAN-TOOL\r\n',  # Tool identifier
                b'CONFIG\r\n',  # Config command
                b'SETUP\r\n'   # Setup command
            ]
            
            for cmd in proprietary_commands:
                print(f"Testing proprietary command: {cmd.hex()}")
                response = self.send_raw_data(cmd)
                if response:
                    print("*** Proprietary command got response! ***")
                time.sleep(1)
            
        finally:
            if self.serial_conn:
                self.serial_conn.close()
    
    def interactive_mode(self):
        """Interactive mode for manual testing"""
        if not self.connect():
            return
        
        print("Interactive mode - type 'quit' to exit")
        print("Commands:")
        print("  hex:AABBCC - send hex data")
        print("  ascii:hello - send ASCII data")
        print("  sniff:10 - sniff for 10 seconds")
        print("  quit - exit")
        
        try:
            while True:
                cmd = input("\n> ").strip()
                
                if cmd.lower() == 'quit':
                    break
                elif cmd.startswith('hex:'):
                    hex_data = cmd[4:].replace(' ', '')
                    try:
                        data = bytes.fromhex(hex_data)
                        self.send_raw_data(data)
                    except ValueError:
                        print("Invalid hex data")
                elif cmd.startswith('ascii:'):
                    ascii_data = cmd[6:]
                    self.send_raw_data(ascii_data.encode('utf-8'))
                elif cmd.startswith('sniff:'):
                    try:
                        duration = int(cmd[6:])
                        self.sniff_traffic(duration)
                    except ValueError:
                        print("Invalid duration")
                else:
                    print("Unknown command")
        
        finally:
            if self.serial_conn:
                self.serial_conn.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Device Protocol Analyzer")
    parser.add_argument('--port', default='/dev/tty.usbserial-1140', help='Serial port')
    parser.add_argument('--analyze', action='store_true', help='Run full analysis')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--baud-test', action='store_true', help='Test baud rates only')
    
    args = parser.parse_args()
    
    analyzer = ProtocolAnalyzer(args.port)
    
    if args.analyze:
        analyzer.analyze_device_protocol()
    elif args.interactive:
        analyzer.interactive_mode()
    elif args.baud_test:
        analyzer.connect()
        analyzer.test_baud_rates()
    else:
        print("Use --analyze, --interactive, or --baud-test")


if __name__ == "__main__":
    main()