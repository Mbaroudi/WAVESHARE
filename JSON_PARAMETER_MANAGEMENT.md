# 📊 JSON Parameter Management - Waveshare CAN Tool

## 🎯 Overview
The enhanced Waveshare CAN Tool now includes **comprehensive JSON parameter management** for reading, saving, and loading all device parameters. This allows complete device configuration backup, restore, and sharing.

## 🔧 Features

### **📖 Device Parameter Reading**
- **Real-time Parameter Reading**: Query device for current settings
- **Complete Parameter Set**: All UART, CAN, mode, performance, and protocol settings
- **Status Information**: Device info, connection status, performance metrics
- **Hardware Validation**: Only works with connected devices

### **💾 JSON Save/Load**
- **Structured JSON Format**: Human-readable configuration files
- **Complete Backup**: All device parameters in single file
- **Cross-Platform**: Works on Windows, macOS, Linux
- **Timestamped**: Automatic timestamp and version tracking

### **✅ Parameter Application**
- **Device Configuration**: Apply JSON parameters to hardware
- **Real AT Commands**: Sends actual configuration commands
- **Validation**: Parameter validation before application
- **Status Updates**: Real-time progress and error reporting

## 📋 Device Parameter Structure

### **🔌 Device Information**
```json
"device_info": {
  "model": "Waveshare RS232/485/422 to CAN",
  "version": "1.0",
  "serial_number": "WS-CAN-001234",
  "firmware_version": "FW1.2.3",
  "hardware_version": "HW1.0"
}
```

### **🔌 UART Configuration**
```json
"uart_config": {
  "baud_rate": 115200,
  "data_bits": 8,
  "stop_bits": 1,
  "parity": "N",
  "flow_control": "none",
  "timeout": 2000,
  "buffer_size": 8192
}
```

### **🚗 CAN Configuration**
```json
"can_config": {
  "baud_rate": 500000,
  "frame_type": "standard",
  "can_id": "0x123",
  "filter_id": "0x7E0",
  "mask_id": "0x7F0",
  "accept_all": false,
  "enable_filters": true
}
```

### **⚙️ Working Mode**
```json
"working_mode": {
  "mode": "transparent",
  "mode_id": 0,
  "direction": "bidirectional",
  "frame_length": 8,
  "id_offset": 0,
  "data_format": "raw"
}
```

### **⚡ Performance Settings**
```json
"performance": {
  "target_rate": 83,
  "max_latency": 12,
  "buffer_mode": "auto",
  "optimization": "high_performance"
}
```

### **🔗 Protocol Settings**
```json
"protocol": {
  "protocol_type": "obd2",
  "obd2_enabled": true,
  "j1939_enabled": false,
  "isotp_enabled": true,
  "uds_enabled": false
}
```

### **📊 Status Information**
```json
"status": {
  "connected": true,
  "last_update": "Wed Jul 09 15:55:00 CET 2025",
  "error_count": 0,
  "frame_count": 12345,
  "uptime": 7200
}
```

## 🎮 User Interface

### **Device Parameters Tab**
- **📖 Read Device Parameters**: Query current device settings
- **💾 Save JSON**: Export parameters to JSON file
- **📂 Load JSON**: Import parameters from JSON file
- **✅ Apply Parameters**: Configure device with loaded parameters
- **🔄 Refresh**: Update parameter display

### **Real-Time Status**
- **Status Bar**: Shows current operation status
- **Progress Bar**: Visual feedback during operations
- **Error Messages**: Clear error reporting
- **Success Notifications**: Confirmation of operations

## 🔍 AT Command Mapping

### **Parameter Reading Commands**
```
AT+UART?      -> Read UART configuration
AT+CAN?       -> Read CAN baud rate
AT+ID?        -> Read CAN ID
AT+FILTER?    -> Read filter/mask settings
AT+MODE?      -> Read working mode
AT+PERF?      -> Read performance settings
AT+PROTO?     -> Read protocol settings
AT+STATUS?    -> Read device status
AT+INFO?      -> Read device information
```

### **Parameter Setting Commands**
```
AT+UART=115200,8,1,0,0  -> Set UART config
AT+CAN=500000           -> Set CAN baud rate
AT+ID=0x123             -> Set CAN ID
AT+FILTER=0x7E0,0x7F0   -> Set filter/mask
AT+MODE=0               -> Set working mode
AT+PERF=83              -> Set performance
AT+SAVE                 -> Save configuration
```

## 📝 Response Parsing

### **UART Response**
```
+UART:115200,8,1,0,0
│     │       │ │ │ └─ Flow control (0=none, 1=hardware)
│     │       │ │ └─── Parity (0=none, 1=even, 2=odd)
│     │       │ └───── Stop bits
│     │       └─────── Data bits
│     └─────────────── Baud rate
└───────────────────── UART response prefix
```

### **CAN Response**
```
+CAN:500000
│    └─────── CAN baud rate
└─────────── CAN response prefix
```

### **Mode Response**
```
+MODE:0
│     └─ Mode ID (0=transparent, 1=transparent+ID, 2=format, 3=modbus)
└─────── Mode response prefix
```

## 🎯 Usage Examples

### **1. Read Current Device Parameters**
```
1. Connect to device
2. Click "📖 Read Device Parameters"
3. View parameters in JSON format
4. Parameters automatically updated in display
```

### **2. Save Device Configuration**
```
1. Read current parameters (step 1)
2. Click "💾 Save JSON"
3. Choose filename (e.g., "my_car_config.json")
4. Configuration saved to file
```

### **3. Load and Apply Configuration**
```
1. Click "📂 Load JSON"
2. Select configuration file
3. Review loaded parameters
4. Click "✅ Apply Parameters"
5. Configuration applied to device
```

### **4. Create Configuration Profile**
```
1. Configure device using Advanced CAN tab
2. Read parameters using Device Parameters tab
3. Save as JSON profile
4. Share profile with other users
```

## 📊 Configuration Profiles

### **Automotive OBD-II Profile**
```json
{
  "uart_config": {"baud_rate": 115200, "data_bits": 8, "stop_bits": 1, "parity": "N"},
  "can_config": {"baud_rate": 500000, "frame_type": "standard", "can_id": "0x7DF"},
  "working_mode": {"mode": "transparent", "mode_id": 0, "frame_length": 8},
  "performance": {"target_rate": 83, "max_latency": 12},
  "protocol": {"protocol_type": "obd2", "obd2_enabled": true}
}
```

### **Industrial J1939 Profile**
```json
{
  "uart_config": {"baud_rate": 115200, "data_bits": 8, "stop_bits": 1, "parity": "N"},
  "can_config": {"baud_rate": 250000, "frame_type": "extended", "can_id": "0x18F00100"},
  "working_mode": {"mode": "transparent_id", "mode_id": 1, "frame_length": 8},
  "performance": {"target_rate": 50, "max_latency": 20},
  "protocol": {"protocol_type": "j1939", "j1939_enabled": true}
}
```

### **Diagnostic UDS Profile**
```json
{
  "uart_config": {"baud_rate": 115200, "data_bits": 8, "stop_bits": 1, "parity": "N"},
  "can_config": {"baud_rate": 500000, "frame_type": "standard", "can_id": "0x123"},
  "working_mode": {"mode": "format", "mode_id": 2, "frame_length": 8},
  "performance": {"target_rate": 100, "max_latency": 10},
  "protocol": {"protocol_type": "uds", "uds_enabled": true, "isotp_enabled": true}
}
```

## 🛠️ Error Handling

### **Common Errors and Solutions**
- **"Device not connected"**: Connect to device first
- **"Invalid JSON format"**: Check JSON syntax
- **"Parameter application failed"**: Check device connection
- **"File not found"**: Verify file path and permissions

### **Validation Checks**
- **Parameter Ranges**: Validates baud rates, IDs, etc.
- **JSON Structure**: Ensures valid JSON format
- **Device Compatibility**: Checks parameter compatibility
- **Connection Status**: Verifies device connection

## 📈 Benefits

### **Configuration Management**
- ✅ **Backup**: Complete device configuration backup
- ✅ **Restore**: Quick configuration restoration
- ✅ **Sharing**: Easy configuration sharing
- ✅ **Versioning**: Timestamped configurations

### **Professional Features**
- ✅ **Real Hardware**: Works with actual devices
- ✅ **Complete Parameters**: All settings included
- ✅ **Validation**: Parameter validation
- ✅ **Status Feedback**: Real-time operation feedback

### **Cross-Platform**
- ✅ **Windows**: Full support
- ✅ **macOS**: Full support
- ✅ **Linux**: Full support
- ✅ **Portable**: Single JAR file

## 🎉 Summary

The JSON Parameter Management system provides:
- **📖 Complete Parameter Reading** from real hardware
- **💾 JSON Save/Load** for configuration management
- **✅ Parameter Application** to device
- **🔄 Real-time Updates** and validation
- **🎯 Professional Features** for expert users

**Result**: Complete device configuration management with backup, restore, and sharing capabilities!