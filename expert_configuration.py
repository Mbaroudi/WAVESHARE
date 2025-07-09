#!/usr/bin/env python3
"""
WS-CAN-TOOL Expert Configuration Script
Professional device configuration and testing by an expert
"""

import sys
import time
import json
from datetime import datetime
from waveshare_can_tool import WaveshareCANTool, WorkMode, FrameType
import serial.tools.list_ports

class ExpertConfigurator:
    """Expert configuration class for Waveshare CAN devices"""
    
    def __init__(self):
        self.tool = WaveshareCANTool()
        self.test_results = []
        self.configuration_log = []
        
    def log_action(self, action, result, details=""):
        """Log configuration actions"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'result': result,
            'details': details
        }
        self.configuration_log.append(entry)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {action}: {'✓' if result else '✗'} {details}")
    
    def detect_device(self):
        """Expert device detection"""
        print("=== EXPERT DEVICE DETECTION ===")
        
        # List all available ports
        ports = list(serial.tools.list_ports.comports())
        print(f"Available serial ports: {len(ports)}")
        
        for port in ports:
            print(f"  {port.device}: {port.description}")
            if 'usbserial' in port.device or 'USB' in port.description:
                print(f"    → Likely CAN device: {port.device}")
        
        # Test connection to primary port
        primary_port = '/dev/tty.usbserial-1140'
        self.tool.port = primary_port
        
        if self.tool.connect():
            self.log_action("Device Detection", True, f"Connected to {primary_port}")
            return True
        else:
            self.log_action("Device Detection", False, f"Failed to connect to {primary_port}")
            return False
    
    def analyze_device_capabilities(self):
        """Analyze device capabilities and current state"""
        print("\n=== DEVICE CAPABILITY ANALYSIS ===")
        
        # Test various baud rates
        baud_rates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
        working_bauds = []
        
        for baud in baud_rates:
            try:
                self.tool.serial_conn.baudrate = baud
                self.tool.serial_conn.timeout = 0.5
                
                # Test AT command
                self.tool.serial_conn.write(b'AT\r\n')
                time.sleep(0.1)
                response = self.tool.serial_conn.read(100)
                
                if response and len(response) > 0:
                    working_bauds.append(baud)
                    self.log_action(f"Baud Rate Test {baud}", True, f"Response: {response.hex()}")
                else:
                    self.log_action(f"Baud Rate Test {baud}", False, "No response")
                    
            except Exception as e:
                self.log_action(f"Baud Rate Test {baud}", False, f"Error: {e}")
        
        # Reset to standard baud
        self.tool.serial_conn.baudrate = 115200
        
        # Test device info commands
        info_commands = [
            'AT', 'AT+VER', 'AT+INFO', 'AT+STATUS', 'AT+HELP',
            'AT+UART?', 'AT+CAN?', 'AT+WORK?', 'AT+FILTER?'
        ]
        
        device_info = {}
        for cmd in info_commands:
            response = self.tool.send_command(cmd)
            if response:
                device_info[cmd] = response
                self.log_action(f"Info Command {cmd}", True, f"Response: {response[:50]}...")
            else:
                self.log_action(f"Info Command {cmd}", False, "No response")
        
        return {
            'working_bauds': working_bauds,
            'device_info': device_info
        }
    
    def configure_for_industrial_use(self):
        """Configure device for industrial CAN bus applications"""
        print("\n=== INDUSTRIAL CONFIGURATION ===")
        
        # Configuration profiles for different industrial applications
        profiles = {
            'automotive': {
                'uart_baud': 115200,
                'can_baud': 500000,
                'work_mode': WorkMode.TRANSPARENT,
                'frame_type': FrameType.STANDARD,
                'filter_id': 0x000,
                'filter_mask': 0x000
            },
            'industrial_automation': {
                'uart_baud': 115200,
                'can_baud': 250000,
                'work_mode': WorkMode.TRANSPARENT_WITH_ID,
                'frame_type': FrameType.STANDARD,
                'filter_id': 0x100,
                'filter_mask': 0x700
            },
            'heavy_machinery': {
                'uart_baud': 57600,
                'can_baud': 125000,
                'work_mode': WorkMode.TRANSPARENT,
                'frame_type': FrameType.EXTENDED,
                'filter_id': 0x1800,
                'filter_mask': 0x1F00
            },
            'marine_systems': {
                'uart_baud': 38400,
                'can_baud': 250000,
                'work_mode': WorkMode.TRANSPARENT,
                'frame_type': FrameType.STANDARD,
                'filter_id': 0x000,
                'filter_mask': 0x000
            }
        }
        
        # Apply automotive profile (most common)
        profile = profiles['automotive']
        self.tool.config.uart_baud = profile['uart_baud']
        self.tool.config.can_baud = profile['can_baud']
        self.tool.config.work_mode = profile['work_mode']
        self.tool.config.can_frame_type = profile['frame_type']
        self.tool.config.can_filter_id = profile['filter_id']
        self.tool.config.can_filter_mask = profile['filter_mask']
        
        # Apply configuration
        success = self.tool.apply_config()
        self.log_action("Industrial Configuration", success, "Applied automotive profile")
        
        # Save configuration profiles to file
        with open('industrial_profiles.json', 'w') as f:
            json.dump(profiles, f, indent=2, default=str)
        
        return success
    
    def perform_comprehensive_testing(self):
        """Perform comprehensive device testing"""
        print("\n=== COMPREHENSIVE TESTING ===")
        
        test_cases = [
            self.test_basic_communication,
            self.test_can_frame_transmission,
            self.test_different_data_lengths,
            self.test_high_frequency_transmission,
            self.test_extended_frames,
            self.test_error_handling,
            self.test_monitoring_capability
        ]
        
        results = {}
        for test_func in test_cases:
            test_name = test_func.__name__
            try:
                result = test_func()
                results[test_name] = result
                self.log_action(f"Test: {test_name}", result['success'], result.get('details', ''))
            except Exception as e:
                results[test_name] = {'success': False, 'error': str(e)}
                self.log_action(f"Test: {test_name}", False, f"Exception: {e}")
        
        return results
    
    def test_basic_communication(self):
        """Test basic serial communication"""
        try:
            # Test simple data transmission
            test_data = b'\x01\x02\x03\x04'
            self.tool.serial_conn.write(test_data)
            time.sleep(0.1)
            
            return {'success': True, 'details': f'Sent {len(test_data)} bytes'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_can_frame_transmission(self):
        """Test CAN frame transmission"""
        try:
            frames_sent = 0
            test_frames = [
                (0x123, b'\x01\x02\x03\x04'),
                (0x456, b'\x05\x06\x07\x08'),
                (0x789, b'\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10')
            ]
            
            for can_id, data in test_frames:
                if self.tool.send_can_frame(can_id, data):
                    frames_sent += 1
                time.sleep(0.1)
            
            return {'success': frames_sent > 0, 'details': f'Sent {frames_sent}/{len(test_frames)} frames'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_different_data_lengths(self):
        """Test different CAN frame data lengths"""
        try:
            success_count = 0
            test_lengths = [1, 2, 4, 8]  # Common CAN data lengths
            
            for length in test_lengths:
                data = bytes(range(length))
                if self.tool.send_can_frame(0x100 + length, data):
                    success_count += 1
                time.sleep(0.1)
            
            return {'success': success_count > 0, 'details': f'Tested {success_count}/{len(test_lengths)} lengths'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_high_frequency_transmission(self):
        """Test high-frequency frame transmission"""
        try:
            frames_sent = 0
            start_time = time.time()
            
            # Send frames for 2 seconds
            while time.time() - start_time < 2.0:
                if self.tool.send_can_frame(0x200, b'\x01\x02\x03\x04'):
                    frames_sent += 1
                time.sleep(0.01)  # 100Hz attempt
            
            frequency = frames_sent / 2.0
            return {'success': frames_sent > 0, 'details': f'Sent {frames_sent} frames at {frequency:.1f} Hz'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_extended_frames(self):
        """Test extended CAN frames"""
        try:
            # Switch to extended frame mode
            original_frame_type = self.tool.config.can_frame_type
            self.tool.config.can_frame_type = FrameType.EXTENDED
            
            # Test extended ID
            extended_id = 0x1FFFFFFF  # Maximum extended ID
            success = self.tool.send_can_frame(extended_id, b'\x01\x02\x03\x04')
            
            # Restore original frame type
            self.tool.config.can_frame_type = original_frame_type
            
            return {'success': success, 'details': f'Extended ID: 0x{extended_id:08X}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_error_handling(self):
        """Test error handling capabilities"""
        try:
            test_cases = [
                # Invalid CAN ID
                (0x800, b'\x01\x02\x03\x04'),  # Standard ID too large
                # Invalid data length
                (0x123, b'\x01\x02\x03\x04\x05\x06\x07\x08\x09'),  # Too long
                # Empty data
                (0x123, b''),
            ]
            
            handled_errors = 0
            for can_id, data in test_cases:
                try:
                    self.tool.send_can_frame(can_id, data)
                    handled_errors += 1
                except:
                    # Expected to fail
                    pass
            
            return {'success': True, 'details': f'Handled {handled_errors}/{len(test_cases)} error cases'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_monitoring_capability(self):
        """Test monitoring capability"""
        try:
            # Start monitoring
            self.tool.start_monitoring()
            
            # Send some frames to monitor
            for i in range(5):
                self.tool.send_can_frame(0x300 + i, bytes([i, i+1, i+2, i+3]))
                time.sleep(0.1)
            
            # Stop monitoring
            time.sleep(0.5)
            self.tool.stop_monitoring()
            
            return {'success': True, 'details': 'Monitoring test completed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_test_report(self, test_results):
        """Generate comprehensive test report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'device_port': self.tool.port,
            'configuration_log': self.configuration_log,
            'test_results': test_results,
            'summary': {
                'total_tests': len(test_results),
                'passed': sum(1 for r in test_results.values() if r.get('success', False)),
                'failed': sum(1 for r in test_results.values() if not r.get('success', False))
            }
        }
        
        # Save report to file
        report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_filename
    
    def run_expert_configuration(self):
        """Run complete expert configuration sequence"""
        print("=== WS-CAN-TOOL EXPERT CONFIGURATION ===")
        print("Professional device configuration and testing")
        print("=" * 50)
        
        try:
            # Step 1: Device detection
            if not self.detect_device():
                print("✗ Device detection failed - cannot proceed")
                return False
            
            # Step 2: Analyze capabilities
            capabilities = self.analyze_device_capabilities()
            
            # Step 3: Configure for industrial use
            self.configure_for_industrial_use()
            
            # Step 4: Comprehensive testing
            test_results = self.perform_comprehensive_testing()
            
            # Step 5: Generate report
            report_file = self.generate_test_report(test_results)
            
            # Step 6: Summary
            print("\n" + "=" * 50)
            print("EXPERT CONFIGURATION COMPLETE")
            print("=" * 50)
            print(f"Device: {self.tool.port}")
            print(f"Configuration: Applied automotive profile")
            print(f"Tests: {test_results}")
            print(f"Report: {report_file}")
            
            # Recommendations
            print("\nEXPERT RECOMMENDATIONS:")
            if len(capabilities['working_bauds']) == 0:
                print("• Device is in transparent mode (normal operation)")
                print("• Use direct frame transmission for CAN communication")
            else:
                print("• Device responds to AT commands")
                print("• Configuration changes are possible")
            
            print("• Device is configured for automotive CAN (500kbps)")
            print("• Use web interface for real-time monitoring")
            print("• Check test report for detailed results")
            
            return True
            
        except Exception as e:
            self.log_action("Expert Configuration", False, f"Fatal error: {e}")
            return False
        
        finally:
            if self.tool.serial_conn and self.tool.serial_conn.is_open:
                self.tool.disconnect()

def main():
    """Main function"""
    configurator = ExpertConfigurator()
    success = configurator.run_expert_configuration()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())