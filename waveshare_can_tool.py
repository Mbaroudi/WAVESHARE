#!/usr/bin/env python3
"""
Waveshare RS232/485/422 to CAN Configuration Tool
Python-based replacement for WS-CAN-TOOL.exe

Features:
- Device configuration and parameter setting
- CAN communication testing
- Data logging and monitoring
- Cross-platform compatibility (macOS, Linux, Windows)
"""

import serial
import time
import struct
import threading
import json
import os
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


class WorkMode(Enum):
    """Device working modes"""
    TRANSPARENT = 1
    TRANSPARENT_WITH_ID = 2
    FORMAT_CONVERSION = 3
    MODBUS_RTU = 4


class FrameType(Enum):
    """CAN frame types"""
    STANDARD = 0
    EXTENDED = 1


@dataclass
class DeviceConfig:
    """Device configuration parameters"""
    uart_baud: int = 115200
    uart_data_bits: int = 8
    uart_stop_bits: int = 1
    uart_parity: str = 'N'  # N, E, O
    can_baud: int = 500000
    can_frame_type: FrameType = FrameType.STANDARD
    work_mode: WorkMode = WorkMode.TRANSPARENT
    can_filter_id: int = 0x000
    can_filter_mask: int = 0x000
    auto_answer: bool = False
    heartbeat_interval: int = 0  # 0 = disabled
    device_id: int = 0x01


class WaveshareCANTool:
    """Main class for Waveshare CAN Tool"""
    
    def __init__(self, port: str = '/dev/tty.usbserial-1140'):
        self.port = port
        self.serial_conn: Optional[serial.Serial] = None
        self.config = DeviceConfig()
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.log_file: Optional[str] = None
        
        # Command constants
        self.CMD_PREFIX = b'\xAA\x55'  # Command prefix
        self.CMD_SUFFIX = b'\x0D\x0A'  # Command suffix
        
        # AT Command set (common for RS232/CAN converters)
        self.COMMANDS = {
            'reset': 'AT+RST',
            'version': 'AT+VER',
            'set_uart': 'AT+UART={baud},{data},{stop},{parity}',
            'set_can': 'AT+CAN={baud}',
            'set_mode': 'AT+WORK={mode}',
            'set_filter': 'AT+FILTER={id},{mask}',
            'save_config': 'AT+SAVE',
            'load_config': 'AT+LOAD',
            'get_status': 'AT+STATUS',
            'set_id': 'AT+ID={id}',
            'heartbeat': 'AT+HEART={interval}'
        }
    
    def connect(self) -> bool:
        """Connect to the device"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=2
            )
            print(f"✓ Connected to {self.port}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the device"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("✓ Disconnected")
    
    def send_command(self, command: str, wait_response: bool = True) -> Optional[str]:
        """Send AT command to device"""
        if not self.serial_conn or not self.serial_conn.is_open:
            print("✗ Not connected to device")
            return None
        
        try:
            # Format command
            cmd_bytes = f"{command}\r\n".encode('utf-8')
            
            # Send command
            self.serial_conn.write(cmd_bytes)
            self.serial_conn.flush()
            
            if wait_response:
                time.sleep(0.1)
                response = self.serial_conn.read(1000)
                if response:
                    return response.decode('utf-8', errors='ignore').strip()
                else:
                    return None
            return "OK"
        except Exception as e:
            print(f"✗ Command failed: {e}")
            return None
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information"""
        info = {}
        
        # Try different info commands
        commands = ['AT+VER', 'AT+INFO', 'AT+STATUS', 'AT']
        
        for cmd in commands:
            response = self.send_command(cmd)
            if response and response != "OK":
                info[cmd] = response
        
        return info
    
    def configure_uart(self, baud: int = 115200, data_bits: int = 8, 
                      stop_bits: int = 1, parity: str = 'N') -> bool:
        """Configure UART parameters"""
        cmd = self.COMMANDS['set_uart'].format(
            baud=baud, data=data_bits, stop=stop_bits, parity=parity
        )
        
        response = self.send_command(cmd)
        if response and 'OK' in response:
            self.config.uart_baud = baud
            self.config.uart_data_bits = data_bits
            self.config.uart_stop_bits = stop_bits
            self.config.uart_parity = parity
            print(f"✓ UART configured: {baud}bps, {data_bits}{parity}{stop_bits}")
            return True
        else:
            print(f"✗ UART configuration failed: {response}")
            return False
    
    def configure_can(self, baud: int = 500000, frame_type: FrameType = FrameType.STANDARD) -> bool:
        """Configure CAN parameters"""
        # Convert baud to kbps
        can_baud_kbps = baud // 1000
        
        cmd = self.COMMANDS['set_can'].format(baud=can_baud_kbps)
        response = self.send_command(cmd)
        
        if response and 'OK' in response:
            self.config.can_baud = baud
            self.config.can_frame_type = frame_type
            print(f"✓ CAN configured: {baud}bps, {frame_type.name} frame")
            return True
        else:
            print(f"✗ CAN configuration failed: {response}")
            return False
    
    def set_work_mode(self, mode: WorkMode) -> bool:
        """Set device working mode"""
        cmd = self.COMMANDS['set_mode'].format(mode=mode.value)
        response = self.send_command(cmd)
        
        if response and 'OK' in response:
            self.config.work_mode = mode
            print(f"✓ Work mode set to: {mode.name}")
            return True
        else:
            print(f"✗ Work mode setting failed: {response}")
            return False
    
    def set_can_filter(self, filter_id: int = 0x000, filter_mask: int = 0x000) -> bool:
        """Set CAN filter"""
        cmd = self.COMMANDS['set_filter'].format(id=filter_id, mask=filter_mask)
        response = self.send_command(cmd)
        
        if response and 'OK' in response:
            self.config.can_filter_id = filter_id
            self.config.can_filter_mask = filter_mask
            print(f"✓ CAN filter set: ID=0x{filter_id:03X}, Mask=0x{filter_mask:03X}")
            return True
        else:
            print(f"✗ CAN filter setting failed: {response}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to device"""
        response = self.send_command(self.COMMANDS['save_config'])
        
        if response and 'OK' in response:
            print("✓ Configuration saved to device")
            return True
        else:
            print(f"✗ Configuration save failed: {response}")
            return False
    
    def reset_device(self) -> bool:
        """Reset the device"""
        response = self.send_command(self.COMMANDS['reset'])
        time.sleep(1)  # Wait for reset
        
        print("✓ Device reset")
        return True
    
    def send_can_frame(self, can_id: int, data: bytes, extended: bool = False) -> bool:
        """Send CAN frame"""
        if not self.serial_conn or not self.serial_conn.is_open:
            return False
        
        try:
            # Format CAN frame for transmission
            if self.config.work_mode == WorkMode.TRANSPARENT:
                # In transparent mode, send raw data
                self.serial_conn.write(data)
            else:
                # Format frame with ID (implementation depends on device protocol)
                frame_header = struct.pack('<I', can_id)
                frame_data = frame_header + data
                self.serial_conn.write(frame_data)
            
            print(f"✓ CAN frame sent: ID=0x{can_id:03X}, Data={data.hex()}")
            return True
        except Exception as e:
            print(f"✗ CAN frame send failed: {e}")
            return False
    
    def start_monitoring(self, log_file: Optional[str] = None):
        """Start monitoring CAN traffic"""
        self.is_monitoring = True
        self.log_file = log_file
        
        if log_file:
            with open(log_file, 'w') as f:
                f.write(f"# CAN Monitor Log - {datetime.now()}\n")
                f.write("# Timestamp,Direction,ID,Data\n")
        
        self.monitor_thread = threading.Thread(target=self._monitor_worker)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("✓ Monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring CAN traffic"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("✓ Monitoring stopped")
    
    def _monitor_worker(self):
        """Monitor worker thread"""
        while self.is_monitoring and self.serial_conn and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read(self.serial_conn.in_waiting)
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    # Parse received data
                    hex_data = data.hex()
                    print(f"[{timestamp}] RX: {hex_data}")
                    
                    # Log to file if specified
                    if self.log_file:
                        with open(self.log_file, 'a') as f:
                            f.write(f"{timestamp},RX,unknown,{hex_data}\n")
                
                time.sleep(0.01)  # Small delay to prevent CPU overload
            except Exception as e:
                print(f"Monitor error: {e}")
                break
    
    def save_config_to_file(self, filename: str):
        """Save configuration to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(asdict(self.config), f, indent=2, default=str)
            print(f"✓ Configuration saved to {filename}")
        except Exception as e:
            print(f"✗ Failed to save config: {e}")
    
    def load_config_from_file(self, filename: str):
        """Load configuration from JSON file"""
        try:
            with open(filename, 'r') as f:
                config_dict = json.load(f)
            
            # Update config object
            for key, value in config_dict.items():
                if hasattr(self.config, key):
                    # Handle enum conversion
                    if key == 'work_mode':
                        value = WorkMode(value)
                    elif key == 'can_frame_type':
                        value = FrameType(value)
                    setattr(self.config, key, value)
            
            print(f"✓ Configuration loaded from {filename}")
        except Exception as e:
            print(f"✗ Failed to load config: {e}")
    
    def apply_config(self) -> bool:
        """Apply current configuration to device"""
        success = True
        
        print("Applying configuration to device...")
        
        # Configure UART
        if not self.configure_uart(
            self.config.uart_baud,
            self.config.uart_data_bits,
            self.config.uart_stop_bits,
            self.config.uart_parity
        ):
            success = False
        
        # Configure CAN
        if not self.configure_can(
            self.config.can_baud,
            self.config.can_frame_type
        ):
            success = False
        
        # Set work mode
        if not self.set_work_mode(self.config.work_mode):
            success = False
        
        # Set CAN filter
        if not self.set_can_filter(
            self.config.can_filter_id,
            self.config.can_filter_mask
        ):
            success = False
        
        # Save to device
        if success and not self.save_config():
            success = False
        
        return success


def main():
    """Main function for command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Waveshare CAN Tool - Python Edition")
    parser.add_argument('--port', default='/dev/tty.usbserial-1140', help='Serial port')
    parser.add_argument('--info', action='store_true', help='Get device information')
    parser.add_argument('--config', help='Configuration file to load')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring mode')
    parser.add_argument('--log', help='Log file for monitoring')
    parser.add_argument('--send', nargs=2, metavar=('ID', 'DATA'), help='Send CAN frame')
    parser.add_argument('--reset', action='store_true', help='Reset device')
    
    args = parser.parse_args()
    
    # Create tool instance
    tool = WaveshareCANTool(args.port)
    
    if not tool.connect():
        return 1
    
    try:
        if args.info:
            info = tool.get_device_info()
            print("Device Information:")
            for cmd, response in info.items():
                print(f"  {cmd}: {response}")
        
        if args.config:
            tool.load_config_from_file(args.config)
            tool.apply_config()
        
        if args.reset:
            tool.reset_device()
        
        if args.send:
            can_id = int(args.send[0], 16)
            data = bytes.fromhex(args.send[1])
            tool.send_can_frame(can_id, data)
        
        if args.monitor:
            tool.start_monitoring(args.log)
            try:
                print("Monitoring... Press Ctrl+C to stop")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                tool.stop_monitoring()
    
    finally:
        tool.disconnect()
    
    return 0


if __name__ == "__main__":
    exit(main())