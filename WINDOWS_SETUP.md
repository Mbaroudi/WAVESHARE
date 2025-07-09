# Waveshare CAN Tool - Windows Setup Guide

## Prerequisites for Windows

### 1. Python Installation
```powershell
# Download Python 3.8+ from python.org
# During installation, CHECK "Add Python to PATH"
# Verify installation
python --version
pip --version
```

### 2. Virtual Environment Setup
```powershell
# Create project directory
mkdir C:\WaveshareCAN
cd C:\WaveshareCAN

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install pyserial python-can
```

### 3. Device Driver Installation
1. Connect Waveshare device to USB port
2. Windows will auto-install CH340 driver
3. If driver fails, download from: http://www.wch.cn/downloads/CH341SER_EXE.html
4. Check Device Manager for COM port number (e.g., COM3, COM4)

## Windows-Specific Configuration

### Finding COM Port
```powershell
# Method 1: Device Manager
# Right-click "This PC" → Properties → Device Manager → Ports (COM & LPT)

# Method 2: PowerShell
Get-WmiObject -Class Win32_SerialPort | Select-Object Name, DeviceID

# Method 3: Python script
python -c "import serial.tools.list_ports; [print(p.device, p.description) for p in serial.tools.list_ports.comports()]"
```

### Windows File Paths
- Configuration files: `C:\WaveshareCAN\configs\`
- Log files: `C:\WaveshareCAN\logs\`
- Test reports: `C:\WaveshareCAN\reports\`

## Quick Start for Windows

### 1. Download and Extract Tools
```powershell
# Create directory structure
mkdir C:\WaveshareCAN\tools
mkdir C:\WaveshareCAN\configs
mkdir C:\WaveshareCAN\logs
mkdir C:\WaveshareCAN\reports

# Copy all Python files to C:\WaveshareCAN\tools\
```

### 2. Create Windows Batch Files
```batch
# create_venv.bat
@echo off
echo Creating Python virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate
echo Installing dependencies...
pip install pyserial python-can
echo Setup complete!
pause
```

```batch
# run_web_tool.bat
@echo off
call venv\Scripts\activate
cd tools
python waveshare_web_tool.py
pause
```

```batch
# run_expert_config.bat
@echo off
call venv\Scripts\activate
cd tools
python expert_configuration.py
pause
```

### 3. Windows Registry for COM Port
```powershell
# Check COM port in registry
Get-ItemProperty -Path "HKLM:\HARDWARE\DEVICEMAP\SERIALCOMM"
```

## Windows-Specific Features

### PowerShell Scripts
Create `WaveshareCAN.ps1`:
```powershell
# PowerShell script for Windows automation
param(
    [string]$Action = "config",
    [string]$Port = "COM3"
)

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

switch ($Action) {
    "config" { python tools\expert_configuration.py }
    "web" { python tools\waveshare_web_tool.py }
    "test" { python tools\quick_start.py }
    "monitor" { python tools\waveshare_can_tool.py --monitor --port $Port }
    default { Write-Host "Usage: .\WaveshareCAN.ps1 -Action [config|web|test|monitor] -Port COMx" }
}
```

### Windows Service Configuration
For industrial applications, create Windows service:
```powershell
# Install pywin32 for service support
pip install pywin32

# Create service installer
python -c "
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os

class WaveshareCANService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'WaveshareCANService'
    _svc_display_name_ = 'Waveshare CAN Bridge Service'
    _svc_description_ = 'RS232/485/422 to CAN converter service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Your service code here
        pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WaveshareCANService)
"
```

## Troubleshooting Windows Issues

### Common Problems and Solutions

1. **"Python not found"**
   ```powershell
   # Add Python to PATH manually
   $env:PATH += ";C:\Python39;C:\Python39\Scripts"
   ```

2. **"Access denied to COM port"**
   ```powershell
   # Run as Administrator
   # Check if another program is using the port
   netstat -ab | findstr :COM3
   ```

3. **Virtual environment issues**
   ```powershell
   # Enable script execution
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # Fix activation issues
   venv\Scripts\Activate.ps1
   ```

4. **Firewall blocking web interface**
   ```powershell
   # Allow Python through firewall
   netsh advfirewall firewall add rule name="Python Web Server" dir=in action=allow program="C:\Python39\python.exe"
   ```

5. **USB driver issues**
   - Download CH340 driver from manufacturer
   - Disable Windows driver signature enforcement
   - Check Device Manager for driver conflicts

### Windows-Specific Testing

```powershell
# Test COM port connectivity
mode COM3: BAUD=115200 PARITY=N DATA=8 STOP=1 TO=ON XON=OFF ODSR=OFF OCTS=OFF DTR=OFF RTS=OFF IDSR=OFF

# Test with PowerShell
$port = new-Object System.IO.Ports.SerialPort COM3,115200,None,8,one
$port.Open()
$port.WriteLine("AT")
$port.ReadLine()
$port.Close()
```

## Windows Performance Optimization

### Registry Tweaks
```powershell
# Optimize COM port performance
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Serial" -Name "Start" -Value 3

# Increase buffer sizes
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Serial\Parameters" -Name "RxBuffer" -Value 32768
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Serial\Parameters" -Name "TxBuffer" -Value 32768
```

### Task Scheduler Integration
```powershell
# Create scheduled task for monitoring
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\WaveshareCAN\tools\waveshare_can_tool.py --monitor" -WorkingDirectory "C:\WaveshareCAN"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "WaveshareCANMonitor" -Action $action -Trigger $trigger -Settings $settings
```

## Windows GUI Alternative

Since tkinter might have issues on Windows, use the web interface:
```powershell
# Start web interface
python tools\waveshare_web_tool.py

# Open in default browser
Start-Process "http://localhost:8080"
```

## Industrial Windows Deployment

### Creating Windows Installer
```powershell
# Install cx_Freeze for executable creation
pip install cx_Freeze

# Create setup.py
python -c "
from cx_Freeze import setup, Executable

setup(
    name='WaveshareCANTool',
    version='1.0',
    description='Waveshare CAN Configuration Tool',
    executables=[
        Executable('waveshare_web_tool.py', base='Console'),
        Executable('expert_configuration.py', base='Console')
    ]
)
"

# Build executable
python setup.py build
```

### Windows Configuration Management
```powershell
# Store configuration in Windows registry
$regPath = "HKCU:\Software\WaveshareCAN"
New-Item -Path $regPath -Force
Set-ItemProperty -Path $regPath -Name "DefaultPort" -Value "COM3"
Set-ItemProperty -Path $regPath -Name "DefaultBaud" -Value "115200"
```

This Windows setup guide provides comprehensive instructions for deploying and using the Waveshare CAN tools on Windows systems, including PowerShell scripts, batch files, and Windows-specific optimizations.