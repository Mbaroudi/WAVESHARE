#!/usr/bin/env python3
"""
Waveshare CAN Tool - GUI Version
Graphical interface for configuring RS232/485/422 to CAN converter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
from datetime import datetime
import json
from waveshare_can_tool import WaveshareCANTool, WorkMode, FrameType, DeviceConfig


class WaveshareCANGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Waveshare CAN Tool - Python Edition")
        self.root.geometry("800x600")
        
        # Initialize tool
        self.tool = WaveshareCANTool()
        self.is_connected = False
        self.monitor_running = False
        
        # Create GUI
        self.create_widgets()
        
        # Auto-detect ports
        self.refresh_ports()
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Connection tab
        self.create_connection_tab()
        
        # Configuration tab
        self.create_config_tab()
        
        # Monitor tab
        self.create_monitor_tab()
        
        # Test tab
        self.create_test_tab()
    
    def create_connection_tab(self):
        """Create connection tab"""
        self.conn_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.conn_frame, text="Connection")
        
        # Port selection
        port_frame = ttk.LabelFrame(self.conn_frame, text="Serial Port")
        port_frame.pack(fill='x', padx=10, pady=5)
        
        self.port_var = tk.StringVar(value='/dev/tty.usbserial-1140')
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=30)
        self.port_combo.pack(side='left', padx=5, pady=5)
        
        ttk.Button(port_frame, text="Refresh", command=self.refresh_ports).pack(side='left', padx=5)
        ttk.Button(port_frame, text="Connect", command=self.connect_device).pack(side='left', padx=5)
        ttk.Button(port_frame, text="Disconnect", command=self.disconnect_device).pack(side='left', padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(port_frame, textvariable=self.status_var, foreground="red")
        self.status_label.pack(side='right', padx=5)
        
        # Device info
        info_frame = ttk.LabelFrame(self.conn_frame, text="Device Information")
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10)
        self.info_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Button(info_frame, text="Get Device Info", command=self.get_device_info).pack(pady=5)
    
    def create_config_tab(self):
        """Create configuration tab"""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuration")
        
        # UART Configuration
        uart_frame = ttk.LabelFrame(self.config_frame, text="UART Settings")
        uart_frame.pack(fill='x', padx=10, pady=5)
        
        # UART Baud Rate
        ttk.Label(uart_frame, text="Baud Rate:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.uart_baud_var = tk.StringVar(value="115200")
        uart_baud_combo = ttk.Combobox(uart_frame, textvariable=self.uart_baud_var, 
                                      values=["9600", "19200", "38400", "57600", "115200", "230400", "460800"])
        uart_baud_combo.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Data Bits
        ttk.Label(uart_frame, text="Data Bits:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.uart_data_var = tk.StringVar(value="8")
        ttk.Combobox(uart_frame, textvariable=self.uart_data_var, values=["7", "8"], width=5).grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        # Stop Bits
        ttk.Label(uart_frame, text="Stop Bits:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.uart_stop_var = tk.StringVar(value="1")
        ttk.Combobox(uart_frame, textvariable=self.uart_stop_var, values=["1", "2"], width=5).grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        # Parity
        ttk.Label(uart_frame, text="Parity:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.uart_parity_var = tk.StringVar(value="N")
        ttk.Combobox(uart_frame, textvariable=self.uart_parity_var, values=["N", "E", "O"], width=5).grid(row=1, column=3, sticky='w', padx=5, pady=2)
        
        # CAN Configuration
        can_frame = ttk.LabelFrame(self.config_frame, text="CAN Settings")
        can_frame.pack(fill='x', padx=10, pady=5)
        
        # CAN Baud Rate
        ttk.Label(can_frame, text="CAN Baud Rate:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.can_baud_var = tk.StringVar(value="500000")
        can_baud_combo = ttk.Combobox(can_frame, textvariable=self.can_baud_var,
                                     values=["10000", "20000", "50000", "100000", "125000", "250000", "500000", "1000000"])
        can_baud_combo.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Frame Type
        ttk.Label(can_frame, text="Frame Type:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.can_frame_var = tk.StringVar(value="Standard")
        ttk.Combobox(can_frame, textvariable=self.can_frame_var, values=["Standard", "Extended"]).grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        # Work Mode
        mode_frame = ttk.LabelFrame(self.config_frame, text="Working Mode")
        mode_frame.pack(fill='x', padx=10, pady=5)
        
        self.work_mode_var = tk.StringVar(value="Transparent")
        work_modes = ["Transparent", "Transparent with ID", "Format Conversion", "Modbus RTU"]
        for i, mode in enumerate(work_modes):
            ttk.Radiobutton(mode_frame, text=mode, variable=self.work_mode_var, value=mode).grid(row=i//2, column=i%2, sticky='w', padx=5, pady=2)
        
        # CAN Filter
        filter_frame = ttk.LabelFrame(self.config_frame, text="CAN Filter")
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filter ID:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.filter_id_var = tk.StringVar(value="0x000")
        ttk.Entry(filter_frame, textvariable=self.filter_id_var, width=10).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Filter Mask:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.filter_mask_var = tk.StringVar(value="0x000")
        ttk.Entry(filter_frame, textvariable=self.filter_mask_var, width=10).grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        # Configuration buttons
        btn_frame = ttk.Frame(self.config_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Apply Configuration", command=self.apply_config).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Reset Device", command=self.reset_device).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save to File", command=self.save_config_file).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Load from File", command=self.load_config_file).pack(side='left', padx=5)
    
    def create_monitor_tab(self):
        """Create monitoring tab"""
        self.monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitor_frame, text="Monitor")
        
        # Control buttons
        control_frame = ttk.Frame(self.monitor_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Start Monitor", command=self.start_monitor).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Stop Monitor", command=self.stop_monitor).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Clear Log", command=self.clear_monitor).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Save Log", command=self.save_monitor_log).pack(side='left', padx=5)
        
        # Monitor display
        self.monitor_text = scrolledtext.ScrolledText(self.monitor_frame, height=20)
        self.monitor_text.pack(fill='both', expand=True, padx=10, pady=5)
    
    def create_test_tab(self):
        """Create test tab"""
        self.test_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.test_frame, text="Test")
        
        # Send frame
        send_frame = ttk.LabelFrame(self.test_frame, text="Send CAN Frame")
        send_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(send_frame, text="CAN ID:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.test_id_var = tk.StringVar(value="0x123")
        ttk.Entry(send_frame, textvariable=self.test_id_var, width=10).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(send_frame, text="Data (hex):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.test_data_var = tk.StringVar(value="01 02 03 04 05 06 07 08")
        ttk.Entry(send_frame, textvariable=self.test_data_var, width=25).grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Button(send_frame, text="Send", command=self.send_test_frame).grid(row=0, column=4, padx=5, pady=2)
        
        # Auto test
        auto_frame = ttk.LabelFrame(self.test_frame, text="Auto Test")
        auto_frame.pack(fill='x', padx=10, pady=5)
        
        self.auto_test_var = tk.BooleanVar()
        ttk.Checkbutton(auto_frame, text="Enable Auto Test", variable=self.auto_test_var).pack(side='left', padx=5)
        
        ttk.Label(auto_frame, text="Interval (ms):").pack(side='left', padx=5)
        self.auto_interval_var = tk.StringVar(value="1000")
        ttk.Entry(auto_frame, textvariable=self.auto_interval_var, width=10).pack(side='left', padx=5)
        
        ttk.Button(auto_frame, text="Start Auto Test", command=self.start_auto_test).pack(side='left', padx=5)
        ttk.Button(auto_frame, text="Stop Auto Test", command=self.stop_auto_test).pack(side='left', padx=5)
    
    def refresh_ports(self):
        """Refresh available serial ports"""
        import serial.tools.list_ports
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
    
    def connect_device(self):
        """Connect to the device"""
        port = self.port_var.get()
        self.tool.port = port
        
        if self.tool.connect():
            self.is_connected = True
            self.status_var.set("Connected")
            self.status_label.config(foreground="green")
            messagebox.showinfo("Success", f"Connected to {port}")
        else:
            messagebox.showerror("Error", f"Failed to connect to {port}")
    
    def disconnect_device(self):
        """Disconnect from the device"""
        if self.monitor_running:
            self.stop_monitor()
        
        self.tool.disconnect()
        self.is_connected = False
        self.status_var.set("Disconnected")
        self.status_label.config(foreground="red")
    
    def get_device_info(self):
        """Get device information"""
        if not self.is_connected:
            messagebox.showerror("Error", "Please connect to device first")
            return
        
        info = self.tool.get_device_info()
        self.info_text.delete(1.0, tk.END)
        
        if info:
            for cmd, response in info.items():
                self.info_text.insert(tk.END, f"{cmd}: {response}\n")
        else:
            self.info_text.insert(tk.END, "No response from device\n")
    
    def apply_config(self):
        """Apply configuration to device"""
        if not self.is_connected:
            messagebox.showerror("Error", "Please connect to device first")
            return
        
        # Update tool config
        self.tool.config.uart_baud = int(self.uart_baud_var.get())
        self.tool.config.uart_data_bits = int(self.uart_data_var.get())
        self.tool.config.uart_stop_bits = int(self.uart_stop_var.get())
        self.tool.config.uart_parity = self.uart_parity_var.get()
        self.tool.config.can_baud = int(self.can_baud_var.get())
        
        # Convert frame type
        frame_type = FrameType.STANDARD if self.can_frame_var.get() == "Standard" else FrameType.EXTENDED
        self.tool.config.can_frame_type = frame_type
        
        # Convert work mode
        mode_map = {
            "Transparent": WorkMode.TRANSPARENT,
            "Transparent with ID": WorkMode.TRANSPARENT_WITH_ID,
            "Format Conversion": WorkMode.FORMAT_CONVERSION,
            "Modbus RTU": WorkMode.MODBUS_RTU
        }
        self.tool.config.work_mode = mode_map[self.work_mode_var.get()]
        
        # Filter settings
        try:
            self.tool.config.can_filter_id = int(self.filter_id_var.get(), 16)
            self.tool.config.can_filter_mask = int(self.filter_mask_var.get(), 16)
        except ValueError:
            messagebox.showerror("Error", "Invalid filter ID or mask format")
            return
        
        # Apply configuration
        if self.tool.apply_config():
            messagebox.showinfo("Success", "Configuration applied successfully")
        else:
            messagebox.showerror("Error", "Configuration failed")
    
    def reset_device(self):
        """Reset the device"""
        if not self.is_connected:
            messagebox.showerror("Error", "Please connect to device first")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to reset the device?"):
            self.tool.reset_device()
            messagebox.showinfo("Success", "Device reset")
    
    def save_config_file(self):
        """Save configuration to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.tool.save_config_to_file(filename)
    
    def load_config_file(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.tool.load_config_from_file(filename)
            self.update_gui_from_config()
    
    def update_gui_from_config(self):
        """Update GUI from loaded configuration"""
        config = self.tool.config
        
        self.uart_baud_var.set(str(config.uart_baud))
        self.uart_data_var.set(str(config.uart_data_bits))
        self.uart_stop_var.set(str(config.uart_stop_bits))
        self.uart_parity_var.set(config.uart_parity)
        self.can_baud_var.set(str(config.can_baud))
        
        frame_type = "Standard" if config.can_frame_type == FrameType.STANDARD else "Extended"
        self.can_frame_var.set(frame_type)
        
        mode_map = {
            WorkMode.TRANSPARENT: "Transparent",
            WorkMode.TRANSPARENT_WITH_ID: "Transparent with ID",
            WorkMode.FORMAT_CONVERSION: "Format Conversion",
            WorkMode.MODBUS_RTU: "Modbus RTU"
        }
        self.work_mode_var.set(mode_map[config.work_mode])
        
        self.filter_id_var.set(f"0x{config.can_filter_id:03X}")
        self.filter_mask_var.set(f"0x{config.can_filter_mask:03X}")
    
    def start_monitor(self):
        """Start monitoring"""
        if not self.is_connected:
            messagebox.showerror("Error", "Please connect to device first")
            return
        
        if not self.monitor_running:
            self.monitor_running = True
            self.monitor_thread = threading.Thread(target=self.monitor_worker)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            self.log_message("Monitor started")
    
    def stop_monitor(self):
        """Stop monitoring"""
        if self.monitor_running:
            self.monitor_running = False
            self.log_message("Monitor stopped")
    
    def monitor_worker(self):
        """Monitor worker thread"""
        while self.monitor_running and self.tool.serial_conn and self.tool.serial_conn.is_open:
            try:
                if self.tool.serial_conn.in_waiting > 0:
                    data = self.tool.serial_conn.read(self.tool.serial_conn.in_waiting)
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    hex_data = data.hex()
                    
                    self.root.after(0, self.log_message, f"[{timestamp}] RX: {hex_data}")
                
                time.sleep(0.01)
            except Exception as e:
                self.root.after(0, self.log_message, f"Monitor error: {e}")
                break
    
    def log_message(self, message):
        """Log message to monitor display"""
        self.monitor_text.insert(tk.END, message + "\n")
        self.monitor_text.see(tk.END)
    
    def clear_monitor(self):
        """Clear monitor display"""
        self.monitor_text.delete(1.0, tk.END)
    
    def save_monitor_log(self):
        """Save monitor log to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.monitor_text.get(1.0, tk.END))
            messagebox.showinfo("Success", f"Log saved to {filename}")
    
    def send_test_frame(self):
        """Send test CAN frame"""
        if not self.is_connected:
            messagebox.showerror("Error", "Please connect to device first")
            return
        
        try:
            can_id = int(self.test_id_var.get(), 16)
            data_str = self.test_data_var.get().replace(" ", "")
            data = bytes.fromhex(data_str)
            
            if self.tool.send_can_frame(can_id, data):
                self.log_message(f"TX: ID=0x{can_id:03X}, Data={data.hex()}")
            else:
                messagebox.showerror("Error", "Failed to send frame")
        except ValueError:
            messagebox.showerror("Error", "Invalid CAN ID or data format")
    
    def start_auto_test(self):
        """Start automatic test"""
        if not self.is_connected:
            messagebox.showerror("Error", "Please connect to device first")
            return
        
        self.auto_test_var.set(True)
        self.auto_test_thread = threading.Thread(target=self.auto_test_worker)
        self.auto_test_thread.daemon = True
        self.auto_test_thread.start()
    
    def stop_auto_test(self):
        """Stop automatic test"""
        self.auto_test_var.set(False)
    
    def auto_test_worker(self):
        """Auto test worker thread"""
        while self.auto_test_var.get():
            try:
                can_id = int(self.test_id_var.get(), 16)
                data_str = self.test_data_var.get().replace(" ", "")
                data = bytes.fromhex(data_str)
                interval = int(self.auto_interval_var.get()) / 1000.0
                
                if self.tool.send_can_frame(can_id, data):
                    self.root.after(0, self.log_message, f"AUTO TX: ID=0x{can_id:03X}, Data={data.hex()}")
                
                time.sleep(interval)
            except Exception as e:
                self.root.after(0, self.log_message, f"Auto test error: {e}")
                break


def main():
    """Main function"""
    root = tk.Tk()
    app = WaveshareCANGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()