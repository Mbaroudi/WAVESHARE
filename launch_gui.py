#!/usr/bin/env python3
"""
Launch script for Waveshare CAN Tool GUI
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import serial
        import serial.tools.list_ports
        return True
    except ImportError as e:
        messagebox.showerror("Missing Dependencies", 
                           f"Required dependency missing: {e}\n\n"
                           "Please install using:\n"
                           "pip install pyserial")
        return False

def main():
    """Main launch function"""
    if not check_dependencies():
        sys.exit(1)
    
    # Import and launch GUI
    try:
        from waveshare_can_gui import WaveshareCANGUI
        
        root = tk.Tk()
        app = WaveshareCANGUI(root)
        
        # Set window icon if available
        try:
            root.iconbitmap('icon.ico')
        except:
            pass
        
        root.mainloop()
        
    except Exception as e:
        print(f"Failed to launch GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()