#!/usr/bin/env python3
"""
Quick Start Script for Waveshare CAN Tool
"""

import sys
import os
from waveshare_can_tool import WaveshareCANTool, WorkMode, FrameType

def main():
    print("=== Waveshare CAN Tool - Quick Start ===")
    print()
    
    # Create tool instance
    tool = WaveshareCANTool()
    
    # Connect to device
    print("1. Connecting to device...")
    if tool.connect():
        print("   ✓ Connected successfully")
    else:
        print("   ✗ Connection failed")
        print("   Check that device is plugged in and try again")
        return 1
    
    try:
        # Get device info
        print("\n2. Getting device information...")
        info = tool.get_device_info()
        if info:
            for cmd, response in info.items():
                print(f"   {cmd}: {response}")
        else:
            print("   Device connected but not responding to AT commands")
            print("   This is normal - device may be in transparent mode")
        
        # Configure device with common settings
        print("\n3. Applying standard configuration...")
        tool.config.uart_baud = 115200
        tool.config.can_baud = 500000
        tool.config.work_mode = WorkMode.TRANSPARENT
        tool.config.can_frame_type = FrameType.STANDARD
        
        if tool.apply_config():
            print("   ✓ Configuration applied")
        else:
            print("   ⚠ Configuration may have failed (this is normal for some devices)")
        
        # Test frame sending
        print("\n4. Testing CAN frame transmission...")
        test_id = 0x123
        test_data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
        
        if tool.send_can_frame(test_id, test_data):
            print(f"   ✓ Test frame sent: ID=0x{test_id:03X}, Data={test_data.hex()}")
        else:
            print("   ⚠ Frame send may have failed")
        
        # Start monitoring
        print("\n5. Starting monitoring for 10 seconds...")
        tool.start_monitoring()
        
        import time
        for i in range(10):
            print(f"   Monitoring... {10-i}s remaining", end='\r')
            time.sleep(1)
        
        tool.stop_monitoring()
        print("\n   ✓ Monitoring completed")
        
        print("\n=== Quick Start Complete ===")
        print("Your device is configured and ready to use!")
        print()
        print("Next steps:")
        print("  • Run 'python waveshare_web_tool.py' for web interface")
        print("  • Run 'python waveshare_can_tool.py --help' for command line options")
        print("  • Check README.md for detailed usage instructions")
        
    finally:
        tool.disconnect()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())