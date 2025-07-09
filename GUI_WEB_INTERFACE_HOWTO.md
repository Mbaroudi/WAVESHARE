# Complete GUI and Web Interface HowTo Guide

## Overview

This guide provides comprehensive instructions for using both the GUI and web interfaces of the Waveshare CAN Tool. The web interface is recommended for its cross-platform compatibility and modern design.

## 🌐 Web Interface (Recommended)

### Starting the Web Interface

#### macOS
```bash
# Navigate to project directory
cd /Users/malek/WAVE-SHARE

# Activate virtual environment
source venv/bin/activate

# Start web interface
python waveshare_web_tool.py
```

#### Windows
```batch
:: Navigate to project directory
cd C:\WaveshareCAN

:: Activate virtual environment
call venv\Scripts\activate

:: Start web interface
python waveshare_web_tool.py
```

### Accessing the Interface
1. **Automatic**: Browser opens automatically at `http://localhost:8080`
2. **Manual**: Open any browser and navigate to `http://localhost:8080`
3. **Network**: Use `http://[your-ip]:8080` for network access

## 📱 Web Interface User Guide

### Main Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│                Waveshare CAN Tool - Web Interface          │
├─────────────────────────────────────────────────────────────┤
│ Connection: [Port Field] [Connect] [Disconnect] [Status]   │
├─────────────────────────────────────────────────────────────┤
│ [Configuration] [Monitor] [Test] ←── Navigation Tabs       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    Tab Content Area                         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                     Status Messages                         │
└─────────────────────────────────────────────────────────────┘
```

### 🔌 Connection Tab

#### Step 1: Device Connection
1. **Port Selection**: 
   - macOS: `/dev/tty.usbserial-1140` (default)
   - Windows: `COM3`, `COM4`, etc.
2. **Connect**: Click "Connect" button
3. **Status**: Green "Connected" or red "Disconnected"

#### Connection Troubleshooting
- **Device Not Found**: Check USB cable and device power
- **Permission Denied**: 
  - macOS: `sudo chmod 666 /dev/tty.usbserial-*`
  - Windows: Run as Administrator
- **Port Busy**: Close other applications using the port

### ⚙️ Configuration Tab

#### UART Settings
| Setting | Options | Recommended | Description |
|---------|---------|-------------|-------------|
| Baud Rate | 9600-460800 | **115200** | Serial communication speed |
| Data Bits | 7, 8 | **8** | Data bits per frame |
| Stop Bits | 1, 2 | **1** | Stop bits per frame |
| Parity | None, Even, Odd | **None** | Error checking method |

#### CAN Settings
| Setting | Options | Recommended | Description |
|---------|---------|-------------|-------------|
| CAN Baud Rate | 10k-1M | **500k** | CAN bus speed (automotive standard) |
| Frame Type | Standard, Extended | **Standard** | CAN frame format |

#### Working Modes
1. **Transparent** (Recommended)
   - Direct data pass-through
   - Maximum performance
   - Industrial standard

2. **Transparent with ID**
   - Adds CAN ID to data
   - Better traceability
   - Debugging applications

3. **Format Conversion**
   - Protocol conversion
   - Custom data formats
   - Advanced applications

4. **Modbus RTU**
   - Modbus protocol support
   - Industrial automation
   - SCADA systems

#### Configuration Process
1. **Select Settings**: Choose appropriate values
2. **Apply Configuration**: Click "Apply Configuration"
3. **Save to Device**: Configuration automatically saved
4. **Reset Device**: Use "Reset Device" if needed

### 📊 Monitor Tab

#### Real-time Monitoring
1. **Start Monitor**: Click "Start Monitor"
2. **Live Data**: View real-time CAN traffic
3. **Timestamps**: Each frame includes timestamp
4. **Data Format**: Hexadecimal display

#### Monitor Display Format
```
[12:34:56.789] RX: 0123456789ABCDEF
[12:34:56.790] TX: FEDCBA9876543210
[12:34:56.791] RX: 1122334455667788
```

#### Monitor Controls
- **Start Monitor**: Begin data capture
- **Stop Monitor**: End data capture
- **Clear Log**: Clear display buffer
- **Save Log**: Export to file

#### Data Logging
1. **Automatic Logging**: All data automatically logged
2. **File Format**: Timestamped entries
3. **Export Options**: 
   - `.log` files (text format)
   - `.txt` files (readable format)
   - `.csv` files (spreadsheet format)

### 🧪 Test Tab

#### Manual Frame Transmission
1. **CAN ID**: Enter hexadecimal ID (e.g., `0x123`)
2. **Data**: Enter hex data (e.g., `01 02 03 04 05 06 07 08`)
3. **Send Frame**: Click "Send Frame"
4. **Confirmation**: Success/failure message displayed

#### Frame Format Examples
```
Standard Frame:
  ID: 0x123
  Data: 01 02 03 04 05 06 07 08

Extended Frame:
  ID: 0x1FFFFFFF
  Data: AA BB CC DD EE FF 00 11

Short Frame:
  ID: 0x456
  Data: 12 34
```

#### Auto-Test Mode
1. **Enable Auto Test**: Check the checkbox
2. **Interval**: Set transmission interval (ms)
3. **Start Auto Test**: Begin automatic transmission
4. **Stop Auto Test**: End automatic transmission

#### Test Scenarios
- **Basic Connectivity**: Send single frames
- **Load Testing**: High-frequency transmission
- **Protocol Testing**: Various frame formats
- **Error Testing**: Invalid data handling

## 🖥️ GUI Interface (Alternative)

### Starting the GUI

#### macOS
```bash
# Install tkinter if needed
brew install python-tk

# Start GUI
python waveshare_can_gui.py
```

#### Windows
```batch
:: tkinter usually included with Python
python waveshare_can_gui.py
```

### GUI Layout
```
┌─────────────────────────────────────────────────────────────┐
│  Waveshare CAN Tool                                    [X]  │
├─────────────────────────────────────────────────────────────┤
│ ┌─ Connection ─┐ ┌─ Configuration ─┐ ┌─ Monitor ─┐         │
│ │ Port: [COM3] │ │ UART: [115200]   │ │ [Start]   │         │
│ │ [Connect]    │ │ CAN:  [500k]     │ │ [Stop]    │         │
│ │ Status: ●    │ │ [Apply]          │ │ [Clear]   │         │
│ └─────────────┘ └─────────────────┘ └───────────┘         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    Data Display Area                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ ┌─ Test ─────────────────────────────────────────────────┐ │
│ │ ID: [0x123] Data: [01 02 03 04] [Send] [Auto Test]    │ │
│ └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### GUI Features
- **Native Look**: Platform-native appearance
- **Keyboard Shortcuts**: Standard shortcuts supported
- **Window Management**: Resizable, minimizable
- **File Operations**: Save/load configurations

## 🚀 Advanced Features

### Network Access
#### Enable Network Access
1. **Firewall Configuration**: Allow Python through firewall
2. **Network Binding**: Tool binds to all interfaces
3. **Remote Access**: Access from other devices on network

#### Security Considerations
- **Local Network Only**: No internet exposure
- **No Authentication**: Secure your network
- **Firewall Rules**: Restrict access as needed

### API Integration
#### REST API Endpoints
```javascript
// Connection
POST /api/connect
{
  "port": "/dev/tty.usbserial-1140"
}

// Configuration
POST /api/config
{
  "uart_baud": 115200,
  "can_baud": 500000,
  "work_mode": 1
}

// Send Frame
POST /api/send
{
  "id": "0x123",
  "data": "01 02 03 04"
}

// Monitor Data
GET /api/monitor/data
```

### Automation Scripts
#### JavaScript Automation
```javascript
// Automated testing script
async function runTest() {
  // Connect
  await fetch('/api/connect', {
    method: 'POST',
    body: JSON.stringify({port: 'COM3'})
  });
  
  // Configure
  await fetch('/api/config', {
    method: 'POST',
    body: JSON.stringify({
      uart_baud: 115200,
      can_baud: 500000
    })
  });
  
  // Send test frames
  for (let i = 0; i < 10; i++) {
    await fetch('/api/send', {
      method: 'POST',
      body: JSON.stringify({
        id: '0x123',
        data: `0${i} 02 03 04`
      })
    });
  }
}
```

## 🔧 Platform-Specific Setup

### macOS Setup
```bash
# Install dependencies
brew install python-tk
pip install pyserial python-can

# Device permissions
sudo chmod 666 /dev/tty.usbserial-*

# Start web interface
python waveshare_web_tool.py
```

### Windows Setup
```batch
:: Create virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install dependencies
pip install pyserial python-can colorama

:: Install CH340 driver (if needed)
:: Download from: http://www.wch.cn/downloads/CH341SER_EXE.html

:: Start web interface
python waveshare_web_tool.py
```

### Linux Setup
```bash
# Install dependencies
sudo apt-get install python3-tk python3-pip
pip3 install pyserial python-can

# Device permissions
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB*

# Start web interface
python3 waveshare_web_tool.py
```

## 📋 Best Practices

### Performance Optimization
1. **Frame Rate**: Keep under 100 Hz for stability
2. **Data Size**: Use appropriate frame lengths
3. **Monitoring**: Stop monitoring when not needed
4. **Buffer Management**: Clear logs regularly

### Reliability Tips
1. **Connection Stability**: Use quality USB cables
2. **Error Handling**: Monitor for transmission errors
3. **Backup Configuration**: Save configurations to files
4. **Regular Testing**: Verify functionality periodically

### Troubleshooting Workflow
1. **Check Connection**: Verify device connection
2. **Test Basic Communication**: Send simple frames
3. **Monitor Traffic**: Watch for responses
4. **Check Configuration**: Verify settings
5. **Restart if Needed**: Reset device if unresponsive

## 📚 Common Use Cases

### 1. Automotive Development
- **Configuration**: 500kbps CAN, Standard frames
- **Monitoring**: Real-time OBD-II data
- **Testing**: ECU communication validation

### 2. Industrial Automation
- **Configuration**: 250kbps CAN, Extended frames
- **Monitoring**: Sensor data collection
- **Testing**: PLC communication testing

### 3. Protocol Development
- **Configuration**: Custom baud rates
- **Monitoring**: Protocol analysis
- **Testing**: Frame format validation

### 4. Educational Use
- **Configuration**: Standard automotive settings
- **Monitoring**: Learning CAN protocol
- **Testing**: Understanding frame structures

## 🎯 Expert Tips

### Performance Tuning
- **Optimal Settings**: 115200 UART, 500k CAN
- **Frame Timing**: 10ms intervals for sustained transmission
- **Buffer Size**: Monitor system resource usage
- **Network Latency**: Use localhost for best performance

### Advanced Configuration
- **Filter Setup**: Use filters for specific IDs
- **Extended Frames**: 29-bit IDs for complex systems
- **Modbus Mode**: For industrial protocol conversion
- **Transparent Mode**: Maximum performance applications

### Professional Development
- **API Integration**: Use REST endpoints for automation
- **Custom Scripts**: Develop application-specific tools
- **Data Analysis**: Export logs for offline analysis
- **Quality Assurance**: Implement automated testing

This comprehensive guide enables both beginners and experts to effectively use the Waveshare CAN Tool interfaces for professional CAN bus development and testing.