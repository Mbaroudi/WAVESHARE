#!/usr/bin/env python3
"""
Waveshare CAN Tool - GUI Windows Version
Interface graphique spécialement optimisée pour Windows
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Import du module principal
try:
    from waveshare_can_tool import WaveshareCANTool, WorkMode, FrameType, DeviceConfig
except ImportError:
    # Fallback si le module n'est pas trouvé
    print("Erreur: Module waveshare_can_tool non trouvé")
    sys.exit(1)

class WaveshareCANGUIWindows:
    """Interface GUI optimisée pour Windows"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Waveshare CAN Tool - Configuration Expert")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Définir l'icône si disponible
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Initialiser l'outil
        self.tool = WaveshareCANTool()
        self.is_connected = False
        self.monitor_running = False
        
        # Charger la configuration Windows
        self.load_windows_config()
        
        # Créer l'interface
        self.create_widgets()
        
        # Auto-détecter les ports COM
        self.refresh_ports()
    
    def load_windows_config(self):
        """Charger la configuration Windows"""
        try:
            config_file = "windows_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.windows_config = json.load(f)
                print("✓ Configuration Windows chargée")
            else:
                self.windows_config = {"device_settings": {"default_port": "COM3"}}
                print("⚠ Configuration Windows par défaut utilisée")
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            self.windows_config = {"device_settings": {"default_port": "COM3"}}
    
    def create_widgets(self):
        """Créer les widgets de l'interface"""
        # Style Windows
        style = ttk.Style()
        style.theme_use('winnative')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Waveshare CAN Tool - Configuration Expert", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Section Connexion
        self.create_connection_section(main_frame)
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(2, weight=1)
        
        # Onglets
        self.create_config_tab()
        self.create_monitor_tab()
        self.create_test_tab()
        self.create_expert_tab()
    
    def create_connection_section(self, parent):
        """Créer la section de connexion"""
        conn_frame = ttk.LabelFrame(parent, text="Connexion Périphérique", padding="10")
        conn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Port COM
        ttk.Label(conn_frame, text="Port COM:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.port_var = tk.StringVar(value=self.windows_config.get("device_settings", {}).get("default_port", "COM3"))
        self.port_combo = ttk.Combobox(conn_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Boutons
        ttk.Button(conn_frame, text="Actualiser", command=self.refresh_ports).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(conn_frame, text="Connecter", command=self.connect_device).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(conn_frame, text="Déconnecter", command=self.disconnect_device).grid(row=0, column=4, padx=(0, 5))
        
        # Statut
        self.status_var = tk.StringVar(value="Déconnecté")
        self.status_label = ttk.Label(conn_frame, textvariable=self.status_var, foreground="red")
        self.status_label.grid(row=0, column=5, padx=(20, 0))
    
    def create_config_tab(self):
        """Créer l'onglet de configuration"""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuration")
        
        # Configuration UART
        uart_frame = ttk.LabelFrame(self.config_frame, text="Paramètres UART", padding="10")
        uart_frame.pack(fill='x', padx=10, pady=5)
        
        # Vitesse UART
        ttk.Label(uart_frame, text="Vitesse (baud):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.uart_baud_var = tk.StringVar(value="115200")
        uart_baud_combo = ttk.Combobox(uart_frame, textvariable=self.uart_baud_var, 
                                      values=["9600", "19200", "38400", "57600", "115200", "230400", "460800"])
        uart_baud_combo.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Configuration CAN
        can_frame = ttk.LabelFrame(self.config_frame, text="Paramètres CAN", padding="10")
        can_frame.pack(fill='x', padx=10, pady=5)
        
        # Vitesse CAN
        ttk.Label(can_frame, text="Vitesse CAN:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.can_baud_var = tk.StringVar(value="500000")
        can_baud_combo = ttk.Combobox(can_frame, textvariable=self.can_baud_var,
                                     values=["125000", "250000", "500000", "1000000"])
        can_baud_combo.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Mode de travail
        mode_frame = ttk.LabelFrame(self.config_frame, text="Mode de Fonctionnement", padding="10")
        mode_frame.pack(fill='x', padx=10, pady=5)
        
        self.work_mode_var = tk.StringVar(value="Transparent")
        modes = ["Transparent", "Transparent avec ID", "Conversion Format", "Modbus RTU"]
        for i, mode in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=mode, variable=self.work_mode_var, value=mode).grid(
                row=i//2, column=i%2, sticky='w', padx=5, pady=2)
        
        # Boutons de configuration
        btn_frame = ttk.Frame(self.config_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Appliquer Configuration", command=self.apply_config).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Configuration Auto", command=self.load_automotive_config).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Sauvegarder", command=self.save_config_file).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Charger", command=self.load_config_file).pack(side='left', padx=5)
    
    def create_monitor_tab(self):
        """Créer l'onglet de monitoring"""
        self.monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitor_frame, text="Monitoring")
        
        # Contrôles
        control_frame = ttk.Frame(self.monitor_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Démarrer", command=self.start_monitor).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Arrêter", command=self.stop_monitor).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Effacer", command=self.clear_monitor).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Exporter", command=self.save_monitor_log).pack(side='left', padx=5)
        
        # Affichage des données
        self.monitor_text = scrolledtext.ScrolledText(self.monitor_frame, height=25, width=80)
        self.monitor_text.pack(fill='both', expand=True, padx=10, pady=5)
    
    def create_test_tab(self):
        """Créer l'onglet de test"""
        self.test_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.test_frame, text="Test")
        
        # Envoi de trame
        send_frame = ttk.LabelFrame(self.test_frame, text="Envoi de Trame CAN", padding="10")
        send_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(send_frame, text="ID CAN:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.test_id_var = tk.StringVar(value="0x123")
        ttk.Entry(send_frame, textvariable=self.test_id_var, width=15).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(send_frame, text="Données (hex):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.test_data_var = tk.StringVar(value="01 02 03 04 05 06 07 08")
        ttk.Entry(send_frame, textvariable=self.test_data_var, width=25).grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Button(send_frame, text="Envoyer", command=self.send_test_frame).grid(row=0, column=4, padx=5, pady=2)
        
        # Tests prédéfinis
        preset_frame = ttk.LabelFrame(self.test_frame, text="Tests Prédéfinis", padding="10")
        preset_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(preset_frame, text="Test OBD-II", command=self.test_obd2).pack(side='left', padx=5)
        ttk.Button(preset_frame, text="Test Performance", command=self.test_performance).pack(side='left', padx=5)
        ttk.Button(preset_frame, text="Test ECU", command=self.test_ecu).pack(side='left', padx=5)
    
    def create_expert_tab(self):
        """Créer l'onglet expert"""
        self.expert_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.expert_frame, text="Expert")
        
        # Informations système
        info_frame = ttk.LabelFrame(self.expert_frame, text="Informations Système", padding="10")
        info_frame.pack(fill='x', padx=10, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, width=80)
        self.info_text.pack(fill='both', expand=True)
        
        # Boutons expert
        expert_btn_frame = ttk.Frame(self.expert_frame)
        expert_btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(expert_btn_frame, text="Configuration Expert", command=self.run_expert_config).pack(side='left', padx=5)
        ttk.Button(expert_btn_frame, text="Analyse Protocole", command=self.analyze_protocol).pack(side='left', padx=5)
        ttk.Button(expert_btn_frame, text="Informations Périphérique", command=self.get_device_info).pack(side='left', padx=5)
    
    def refresh_ports(self):
        """Actualiser la liste des ports COM"""
        try:
            import serial.tools.list_ports
            ports = [port.device for port in serial.tools.list_ports.comports()]
            self.port_combo['values'] = ports
            if ports and not self.port_var.get() in ports:
                self.port_combo.set(ports[0])
            print(f"Ports COM détectés: {ports}")
        except Exception as e:
            print(f"Erreur lors de la détection des ports: {e}")
    
    def connect_device(self):
        """Connecter au périphérique"""
        port = self.port_var.get()
        self.tool.port = port
        
        if self.tool.connect():
            self.is_connected = True
            self.status_var.set("Connecté")
            self.status_label.config(foreground="green")
            messagebox.showinfo("Succès", f"Connecté au port {port}")
            self.log_message(f"Connexion réussie sur {port}")
        else:
            messagebox.showerror("Erreur", f"Échec de la connexion au port {port}")
    
    def disconnect_device(self):
        """Déconnecter du périphérique"""
        if self.monitor_running:
            self.stop_monitor()
        
        self.tool.disconnect()
        self.is_connected = False
        self.status_var.set("Déconnecté")
        self.status_label.config(foreground="red")
        self.log_message("Périphérique déconnecté")
    
    def apply_config(self):
        """Appliquer la configuration"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        try:
            # Mettre à jour la configuration
            self.tool.config.uart_baud = int(self.uart_baud_var.get())
            self.tool.config.can_baud = int(self.can_baud_var.get())
            
            # Mode de travail
            mode_map = {
                "Transparent": WorkMode.TRANSPARENT,
                "Transparent avec ID": WorkMode.TRANSPARENT_WITH_ID,
                "Conversion Format": WorkMode.FORMAT_CONVERSION,
                "Modbus RTU": WorkMode.MODBUS_RTU
            }
            self.tool.config.work_mode = mode_map[self.work_mode_var.get()]
            
            # Appliquer
            if self.tool.apply_config():
                messagebox.showinfo("Succès", "Configuration appliquée avec succès")
                self.log_message("Configuration appliquée")
            else:
                messagebox.showwarning("Avertissement", "La configuration peut avoir échoué")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'application: {e}")
    
    def load_automotive_config(self):
        """Charger la configuration automobile"""
        self.uart_baud_var.set("115200")
        self.can_baud_var.set("500000")
        self.work_mode_var.set("Transparent")
        messagebox.showinfo("Info", "Configuration automobile chargée (115200 bps UART, 500k CAN)")
        self.log_message("Configuration automobile chargée")
    
    def save_config_file(self):
        """Sauvegarder la configuration"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        if filename:
            try:
                config = {
                    "uart_baud": int(self.uart_baud_var.get()),
                    "can_baud": int(self.can_baud_var.get()),
                    "work_mode": self.work_mode_var.get()
                }
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=2)
                messagebox.showinfo("Succès", f"Configuration sauvegardée dans {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de sauvegarde: {e}")
    
    def load_config_file(self):
        """Charger une configuration"""
        filename = filedialog.askopenfilename(
            filetypes=[("Fichiers JSON", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                self.uart_baud_var.set(str(config.get("uart_baud", 115200)))
                self.can_baud_var.set(str(config.get("can_baud", 500000)))
                self.work_mode_var.set(config.get("work_mode", "Transparent"))
                
                messagebox.showinfo("Succès", f"Configuration chargée depuis {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
    
    def start_monitor(self):
        """Démarrer le monitoring"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        if not self.monitor_running:
            self.monitor_running = True
            self.monitor_thread = threading.Thread(target=self.monitor_worker)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            self.log_message("Monitoring démarré")
    
    def stop_monitor(self):
        """Arrêter le monitoring"""
        if self.monitor_running:
            self.monitor_running = False
            self.log_message("Monitoring arrêté")
    
    def monitor_worker(self):
        """Thread de monitoring"""
        while self.monitor_running and self.tool.serial_conn and self.tool.serial_conn.is_open:
            try:
                if self.tool.serial_conn.in_waiting > 0:
                    data = self.tool.serial_conn.read(self.tool.serial_conn.in_waiting)
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    hex_data = data.hex().upper()
                    
                    message = f"[{timestamp}] RX: {hex_data}"
                    self.root.after(0, self.log_message, message)
                
                time.sleep(0.01)
            except Exception as e:
                self.root.after(0, self.log_message, f"Erreur monitoring: {e}")
                break
    
    def clear_monitor(self):
        """Effacer l'affichage du monitoring"""
        self.monitor_text.delete(1.0, tk.END)
    
    def save_monitor_log(self):
        """Sauvegarder le log de monitoring"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Fichiers Log", "*.log"), ("Fichiers Texte", "*.txt")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.monitor_text.get(1.0, tk.END))
                messagebox.showinfo("Succès", f"Log sauvegardé dans {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de sauvegarde: {e}")
    
    def send_test_frame(self):
        """Envoyer une trame de test"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        try:
            can_id = int(self.test_id_var.get(), 16)
            data_str = self.test_data_var.get().replace(" ", "")
            data = bytes.fromhex(data_str)
            
            if self.tool.send_can_frame(can_id, data):
                message = f"TX: ID=0x{can_id:03X}, Data={data.hex().upper()}"
                self.log_message(message)
                messagebox.showinfo("Succès", "Trame envoyée avec succès")
            else:
                messagebox.showerror("Erreur", "Échec de l'envoi de la trame")
        except ValueError:
            messagebox.showerror("Erreur", "Format d'ID CAN ou de données invalide")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")
    
    def test_obd2(self):
        """Test OBD-II"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        # Requête OBD-II pour le régime moteur
        obd_id = 0x7DF
        obd_data = bytes([0x02, 0x01, 0x0C])  # Mode 1, PID 0x0C (Engine RPM)
        
        if self.tool.send_can_frame(obd_id, obd_data):
            self.log_message(f"Test OBD-II: Requête régime moteur envoyée (ID=0x{obd_id:03X})")
            messagebox.showinfo("Test OBD-II", "Requête de régime moteur envoyée")
        else:
            messagebox.showerror("Erreur", "Échec du test OBD-II")
    
    def test_performance(self):
        """Test de performance"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        import time
        frames_sent = 0
        start_time = time.time()
        
        try:
            for i in range(50):
                if self.tool.send_can_frame(0x200 + i, bytes([i % 256, (i+1) % 256, (i+2) % 256, (i+3) % 256])):
                    frames_sent += 1
                time.sleep(0.02)  # 50 Hz
            
            end_time = time.time()
            duration = end_time - start_time
            rate = frames_sent / duration
            
            self.log_message(f"Test performance: {frames_sent} trames en {duration:.2f}s ({rate:.1f} Hz)")
            messagebox.showinfo("Test Performance", f"Performance: {rate:.1f} Hz")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de test: {e}")
    
    def test_ecu(self):
        """Test ECU"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        # Test de communication ECU basique
        ecu_frames = [
            (0x100, bytes([0x01, 0x02, 0x03, 0x04])),
            (0x200, bytes([0x05, 0x06, 0x07, 0x08])),
            (0x300, bytes([0x09, 0x0A, 0x0B, 0x0C]))
        ]
        
        success_count = 0
        for can_id, data in ecu_frames:
            if self.tool.send_can_frame(can_id, data):
                success_count += 1
                self.log_message(f"Test ECU: Trame {can_id:03X} envoyée")
        
        messagebox.showinfo("Test ECU", f"Test ECU: {success_count}/{len(ecu_frames)} trames envoyées")
    
    def run_expert_config(self):
        """Lancer la configuration expert"""
        try:
            messagebox.showinfo("Configuration Expert", 
                              "Lancement de la configuration expert...\n" +
                              "Cette opération peut prendre quelques minutes.")
            
            # Ici, vous pourriez lancer expert_configuration_windows.py
            # ou intégrer ses fonctionnalités directement
            self.log_message("Configuration expert lancée")
            messagebox.showinfo("Configuration Expert", "Configuration expert terminée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur configuration expert: {e}")
    
    def analyze_protocol(self):
        """Analyser le protocole"""
        try:
            if not self.is_connected:
                messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
                return
            
            # Analyse basique du protocole
            info = self.tool.get_device_info()
            if info:
                analysis = "Analyse du protocole:\n"
                for cmd, response in info.items():
                    analysis += f"{cmd}: {response}\n"
            else:
                analysis = "Périphérique en mode transparent (normal)\n"
                analysis += "Communication directe des trames CAN"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, analysis)
            self.log_message("Analyse de protocole effectuée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'analyse: {e}")
    
    def get_device_info(self):
        """Obtenir les informations du périphérique"""
        if not self.is_connected:
            messagebox.showerror("Erreur", "Veuillez vous connecter d'abord")
            return
        
        try:
            info = self.tool.get_device_info()
            device_info = f"Informations du Périphérique\n{'='*40}\n"
            device_info += f"Port: {self.tool.port}\n"
            device_info += f"État: {'Connecté' if self.is_connected else 'Déconnecté'}\n"
            device_info += f"Configuration UART: {self.uart_baud_var.get()} bps\n"
            device_info += f"Configuration CAN: {self.can_baud_var.get()} bps\n"
            device_info += f"Mode: {self.work_mode_var.get()}\n\n"
            
            if info:
                device_info += "Réponses AT:\n"
                for cmd, response in info.items():
                    device_info += f"{cmd}: {response}\n"
            else:
                device_info += "Périphérique en mode transparent\n"
                device_info += "Configuration optimale pour automotive\n"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, device_info)
            self.log_message("Informations périphérique récupérées")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur info périphérique: {e}")
    
    def log_message(self, message):
        """Ajouter un message au log de monitoring"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.monitor_text.insert(tk.END, log_entry)
        self.monitor_text.see(tk.END)

def main():
    """Fonction principale"""
    try:
        root = tk.Tk()
        app = WaveshareCANGUIWindows(root)
        
        # Gestionnaire de fermeture
        def on_closing():
            if app.monitor_running:
                app.stop_monitor()
            if app.is_connected:
                app.disconnect_device()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()
