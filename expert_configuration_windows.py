#!/usr/bin/env python3
"""
WS-CAN-TOOL Expert Configuration Script - Windows Version
Professional device configuration and testing for Windows systems
"""

import sys
import time
import json
import os
import platform
from datetime import datetime
from waveshare_can_tool import WaveshareCANTool, WorkMode, FrameType
import serial.tools.list_ports

class WindowsExpertConfigurator:
    """Windows-specific expert configuration class"""
    
    def __init__(self):
        self.tool = WaveshareCANTool()
        self.test_results = []
        self.configuration_log = []
        self.windows_version = platform.platform()
        
        # Create Windows-specific directories
        self.base_dir = os.path.join(os.path.expanduser("~"), "WaveshareCAN")
        self.config_dir = os.path.join(self.base_dir, "configs")
        self.log_dir = os.path.join(self.base_dir, "logs")
        self.report_dir = os.path.join(self.base_dir, "reports")
        
        # Create directories if they don't exist
        for directory in [self.base_dir, self.config_dir, self.log_dir, self.report_dir]:
            os.makedirs(directory, exist_ok=True)
        
    def log_action(self, action, result, details=""):
        """Log configuration actions with Windows-specific formatting"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'result': result,
            'details': details,
            'windows_version': self.windows_version
        }
        self.configuration_log.append(entry)
        
        # Color output for Windows Command Prompt
        if platform.system() == 'Windows':
            import colorama
            colorama.init()
            color = colorama.Fore.GREEN if result else colorama.Fore.RED
            reset = colorama.Style.RESET_ALL
            status = f"{color}{'✓' if result else '✗'}{reset}"
        else:
            status = '✓' if result else '✗'
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {action}: {status} {details}")
    
    def detect_windows_com_ports(self):
        """Windows-specific COM port detection"""
        print("=== WINDOWS COM PORT DETECTION ===")
        
        # Method 1: Using serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        print(f"Available COM ports: {len(ports)}")
        
        com_ports = []
        for port in ports:
            print(f"  {port.device}: {port.description}")
            if 'CH340' in port.description or 'USB' in port.description:
                com_ports.append(port.device)
                print(f"    → Likely Waveshare device: {port.device}")
        
        # Method 2: Windows Registry check
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\\DEVICEMAP\\SERIALCOMM")
            i = 0
            registry_ports = []
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    registry_ports.append(value)
                    i += 1
                except WindowsError:
                    break
            winreg.CloseKey(key)
            print(f"Registry COM ports: {registry_ports}")
        except ImportError:
            print("Windows registry check not available (winreg module)")
        except Exception as e:
            print(f"Registry check failed: {e}")
        
        # Try to connect to detected ports
        for port in com_ports:
            self.tool.port = port
            if self.tool.connect():
                self.log_action("Windows COM Port Detection", True, f"Connected to {port}")
                return port
        
        # Fallback to common COM ports
        common_ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8']
        for port in common_ports:
            self.tool.port = port
            try:
                if self.tool.connect():
                    self.log_action("Windows COM Port Detection", True, f"Connected to {port}")
                    return port
            except:
                continue
        
        self.log_action("Windows COM Port Detection", False, "No COM ports responded")
        return None
    
    def test_windows_specific_features(self):
        """Test Windows-specific features"""
        print("\\n=== WINDOWS SPECIFIC TESTS ===")
        
        tests = {
            'com_port_stability': self.test_com_port_stability,
            'windows_permissions': self.test_windows_permissions,
            'firewall_compatibility': self.test_firewall_compatibility,
            'service_compatibility': self.test_service_compatibility,
            'performance_timing': self.test_performance_timing
        }
        
        results = {}
        for test_name, test_func in tests.items():
            try:
                result = test_func()
                results[test_name] = result
                self.log_action(f"Windows Test: {test_name}", result['success'], result.get('details', ''))
            except Exception as e:
                results[test_name] = {'success': False, 'error': str(e)}
                self.log_action(f"Windows Test: {test_name}", False, f"Exception: {e}")
        
        return results
    
    def test_com_port_stability(self):
        """Test COM port stability on Windows"""
        try:
            # Test multiple connect/disconnect cycles
            cycles = 10
            successful_cycles = 0
            
            for i in range(cycles):
                if self.tool.connect():
                    time.sleep(0.1)
                    self.tool.disconnect()
                    successful_cycles += 1
                    time.sleep(0.1)
            
            # Reconnect for subsequent tests
            self.tool.connect()
            
            success_rate = (successful_cycles / cycles) * 100
            return {
                'success': success_rate > 80,
                'details': f'{successful_cycles}/{cycles} cycles successful ({success_rate:.1f}%)'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_windows_permissions(self):
        """Test Windows permissions for COM port access"""
        try:
            # Test file operations in user directories
            test_file = os.path.join(self.config_dir, "permission_test.txt")
            
            with open(test_file, 'w') as f:
                f.write("Permission test")
            
            with open(test_file, 'r') as f:
                content = f.read()
            
            os.remove(test_file)
            
            # Test COM port exclusive access
            if self.tool.serial_conn and self.tool.serial_conn.is_open:
                return {
                    'success': True,
                    'details': 'File and COM port permissions OK'
                }
            else:
                return {
                    'success': False,
                    'details': 'COM port access denied'
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_firewall_compatibility(self):
        """Test Windows firewall compatibility for web interface"""
        try:
            import socket
            
            # Test if we can bind to localhost
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('localhost', 0))
            port = test_socket.getsockname()[1]
            test_socket.close()
            
            return {
                'success': True,
                'details': f'Can bind to localhost:{port}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_service_compatibility(self):
        """Test Windows service compatibility"""
        try:
            # Test if we can run as a background process
            import subprocess
            import tempfile
            
            # Create a simple test script
            test_script = os.path.join(tempfile.gettempdir(), "service_test.py")
            with open(test_script, 'w') as f:
                f.write("""
import time
import sys
try:
    time.sleep(1)
    sys.exit(0)
except:
    sys.exit(1)
""")
            
            # Run the script as a subprocess
            result = subprocess.run([sys.executable, test_script], 
                                  capture_output=True, timeout=5)
            
            os.remove(test_script)
            
            return {
                'success': result.returncode == 0,
                'details': 'Service compatibility verified'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_performance_timing(self):
        """Test performance timing on Windows"""
        try:
            # Test frame transmission timing
            frame_count = 100
            start_time = time.perf_counter()
            
            for i in range(frame_count):
                self.tool.send_can_frame(0x100, bytes([i % 256]))
                if i % 10 == 0:
                    time.sleep(0.001)  # Small delay every 10 frames
            
            end_time = time.perf_counter()
            duration = end_time - start_time
            fps = frame_count / duration
            
            return {
                'success': fps > 10,  # At least 10 FPS
                'details': f'Transmitted {frame_count} frames in {duration:.3f}s ({fps:.1f} FPS)'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_windows_config_files(self):
        """Create Windows-specific configuration files"""
        print("\\n=== CREATING WINDOWS CONFIG FILES ===")
        
        # Create batch files for easy execution
        batch_files = {
            'start_web_tool.bat': f'''@echo off
cd /d "{os.path.dirname(os.path.abspath(__file__))}"
if exist venv\\Scripts\\activate.bat (
    call venv\\Scripts\\activate.bat
) else (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)
python waveshare_web_tool.py
pause
''',
            'run_expert_config.bat': f'''@echo off
cd /d "{os.path.dirname(os.path.abspath(__file__))}"
if exist venv\\Scripts\\activate.bat (
    call venv\\Scripts\\activate.bat
) else (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)
python expert_configuration_windows.py
pause
''',
            'setup_environment.bat': '''@echo off
echo Setting up Python virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\\Scripts\\activate.bat
echo Installing required packages...
pip install pyserial python-can colorama
echo Setup complete!
pause
''',
            'quick_test.bat': f'''@echo off
cd /d "{os.path.dirname(os.path.abspath(__file__))}"
call venv\\Scripts\\activate.bat
python quick_start.py
pause
'''
        }
        
        for filename, content in batch_files.items():
            filepath = os.path.join(self.base_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            self.log_action(f"Created batch file", True, filename)
        
        # Create PowerShell script
        powershell_script = f'''# Waveshare CAN Tool - PowerShell Script
param(
    [string]$Action = "web",
    [string]$Port = "COM3"
)

$ErrorActionPreference = "Stop"
$ToolDir = "{os.path.dirname(os.path.abspath(__file__))}"

try {{
    Set-Location $ToolDir
    
    if (Test-Path "venv\\Scripts\\Activate.ps1") {{
        & "venv\\Scripts\\Activate.ps1"
    }} else {{
        Write-Host "Virtual environment not found. Please run setup_environment.bat first." -ForegroundColor Red
        exit 1
    }}
    
    switch ($Action) {{
        "web" {{ python waveshare_web_tool.py }}
        "config" {{ python expert_configuration_windows.py }}
        "test" {{ python quick_start.py }}
        "monitor" {{ python waveshare_can_tool.py --monitor --port $Port }}
        default {{ 
            Write-Host "Usage: .\\WaveshareCAN.ps1 -Action [web|config|test|monitor] -Port COMx" -ForegroundColor Yellow
        }}
    }}
}} catch {{
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}}
'''
        
        powershell_path = os.path.join(self.base_dir, "WaveshareCAN.ps1")
        with open(powershell_path, 'w') as f:
            f.write(powershell_script)
        self.log_action("Created PowerShell script", True, "WaveshareCAN.ps1")
        
        # Create Windows configuration
        windows_config = {
            'default_port': 'COM3',
            'default_baud': 115200,
            'web_interface_port': 8080,
            'auto_detect_port': True,
            'log_directory': self.log_dir,
            'config_directory': self.config_dir,
            'report_directory': self.report_dir,
            'windows_version': self.windows_version
        }
        
        config_path = os.path.join(self.config_dir, "windows_config.json")
        with open(config_path, 'w') as f:
            json.dump(windows_config, f, indent=2)
        self.log_action("Created Windows config", True, "windows_config.json")
    
    def generate_windows_report(self, test_results):
        """Generate Windows-specific test report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'windows_version': self.windows_version,
            'python_version': sys.version,
            'device_port': self.tool.port,
            'configuration_log': self.configuration_log,
            'test_results': test_results,
            'summary': {
                'total_tests': len(test_results),
                'passed': sum(1 for r in test_results.values() if r.get('success', False)),
                'failed': sum(1 for r in test_results.values() if not r.get('success', False))
            },
            'windows_specific': {
                'com_ports_detected': [p.device for p in serial.tools.list_ports.comports()],
                'user_directory': os.path.expanduser("~"),
                'config_directory': self.config_dir,
                'log_directory': self.log_dir
            }
        }
        
        # Save report with Windows-compatible filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"windows_test_report_{timestamp}.json"
        report_path = os.path.join(self.report_dir, report_filename)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also create a human-readable summary
        summary_filename = f"windows_test_summary_{timestamp}.txt"
        summary_path = os.path.join(self.report_dir, summary_filename)
        
        with open(summary_path, 'w') as f:
            f.write(f"WAVESHARE CAN TOOL - WINDOWS TEST REPORT\\n")
            f.write(f"{'='*50}\\n")
            f.write(f"Timestamp: {report['timestamp']}\\n")
            f.write(f"Windows Version: {report['windows_version']}\\n")
            f.write(f"Python Version: {report['python_version']}\\n")
            f.write(f"Device Port: {report['device_port']}\\n")
            f.write(f"\\n")
            f.write(f"TEST SUMMARY\\n")
            f.write(f"{'='*50}\\n")
            f.write(f"Total Tests: {report['summary']['total_tests']}\\n")
            f.write(f"Passed: {report['summary']['passed']}\\n")
            f.write(f"Failed: {report['summary']['failed']}\\n")
            f.write(f"\\n")
            f.write(f"DETAILED RESULTS\\n")
            f.write(f"{'='*50}\\n")
            
            for test_name, result in test_results.items():
                status = "PASS" if result.get('success', False) else "FAIL"
                f.write(f"{test_name}: {status}\\n")
                if 'details' in result:
                    f.write(f"  Details: {result['details']}\\n")
                if 'error' in result:
                    f.write(f"  Error: {result['error']}\\n")
                f.write(f"\\n")
        
        return report_path, summary_path
    
    def run_windows_expert_configuration(self):
        """Run complete Windows expert configuration"""
        print("=== WAVESHARE CAN TOOL - WINDOWS EXPERT CONFIGURATION ===")
        print("Professional Windows device configuration and testing")
        print("=" * 60)
        print(f"Windows Version: {self.windows_version}")
        print(f"Python Version: {sys.version}")
        print(f"Working Directory: {self.base_dir}")
        print("=" * 60)
        
        try:
            # Step 1: Windows COM port detection
            detected_port = self.detect_windows_com_ports()
            if not detected_port:
                print("✗ No COM ports detected - cannot proceed")
                return False
            
            # Step 2: Create Windows configuration files
            self.create_windows_config_files()
            
            # Step 3: Run Windows-specific tests
            test_results = self.test_windows_specific_features()
            
            # Step 4: Run standard CAN tests
            print("\\n=== STANDARD CAN TESTS ===")
            standard_tests = {
                'basic_communication': self.test_basic_communication,
                'can_frame_transmission': self.test_can_frame_transmission,
                'monitoring_capability': self.test_monitoring_capability
            }
            
            for test_name, test_func in standard_tests.items():
                try:
                    result = test_func()
                    test_results[test_name] = result
                    self.log_action(f"Standard Test: {test_name}", result['success'], result.get('details', ''))
                except Exception as e:
                    test_results[test_name] = {'success': False, 'error': str(e)}
                    self.log_action(f"Standard Test: {test_name}", False, f"Exception: {e}")
            
            # Step 5: Generate Windows report
            report_path, summary_path = self.generate_windows_report(test_results)
            
            # Step 6: Windows-specific summary
            print("\\n" + "=" * 60)
            print("WINDOWS EXPERT CONFIGURATION COMPLETE")
            print("=" * 60)
            print(f"Device Port: {detected_port}")
            print(f"Configuration Files: {self.config_dir}")
            print(f"Log Directory: {self.log_dir}")
            print(f"Test Report: {report_path}")
            print(f"Summary: {summary_path}")
            
            passed = sum(1 for r in test_results.values() if r.get('success', False))
            total = len(test_results)
            print(f"\\nTest Results: {passed}/{total} tests passed")
            
            # Windows-specific recommendations
            print("\\nWINDOWS RECOMMENDATIONS:")
            print(f"• Device connected to: {detected_port}")
            print(f"• Use batch files in: {self.base_dir}")
            print("• Run 'start_web_tool.bat' for web interface")
            print("• Run 'run_expert_config.bat' for this configuration")
            print("• Check Windows firewall if web interface doesn't work")
            print("• Use 'WaveshareCAN.ps1' for PowerShell automation")
            
            if passed < total:
                print("\\n⚠ WARNINGS:")
                for test_name, result in test_results.items():
                    if not result.get('success', False):
                        print(f"• {test_name}: {result.get('error', 'Failed')}")
            
            return True
            
        except Exception as e:
            self.log_action("Windows Expert Configuration", False, f"Fatal error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            if self.tool.serial_conn and self.tool.serial_conn.is_open:
                self.tool.disconnect()
    
    def test_basic_communication(self):
        """Test basic serial communication"""
        try:
            test_data = b'\\x01\\x02\\x03\\x04'
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
                (0x123, b'\\x01\\x02\\x03\\x04'),
                (0x456, b'\\x05\\x06\\x07\\x08'),
                (0x789, b'\\x09\\x0A\\x0B\\x0C')
            ]
            
            for can_id, data in test_frames:
                if self.tool.send_can_frame(can_id, data):
                    frames_sent += 1
                time.sleep(0.1)
            
            return {'success': frames_sent > 0, 'details': f'Sent {frames_sent}/{len(test_frames)} frames'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_monitoring_capability(self):
        """Test monitoring capability"""
        try:
            self.tool.start_monitoring()
            time.sleep(0.5)
            
            # Send test frames
            for i in range(3):
                self.tool.send_can_frame(0x300 + i, bytes([i, i+1, i+2, i+3]))
                time.sleep(0.1)
            
            self.tool.stop_monitoring()
            return {'success': True, 'details': 'Monitoring test completed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

def main():
    """Main function"""
    # Install colorama for Windows color support
    try:
        import colorama
        colorama.init()
    except ImportError:
        print("Installing colorama for Windows color support...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        import colorama
        colorama.init()
    
    configurator = WindowsExpertConfigurator()
    success = configurator.run_windows_expert_configuration()
    
    if success:
        print("\\n✓ Windows expert configuration completed successfully!")
        print("Press any key to exit...")
        try:
            input()
        except:
            pass
    else:
        print("\\n✗ Windows expert configuration failed!")
        print("Press any key to exit...")
        try:
            input()
        except:
            pass
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())