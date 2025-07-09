// Windows COM Port Fix - Patch pour WaveshareCANTool.java
// Ajouter ces méthodes dans la classe WaveshareCANTool

/**
 * Détecte si l'application fonctionne sur Windows
 */
private boolean isWindows() {
    return System.getProperty("os.name").toLowerCase().contains("win");
}

/**
 * Configuration spécifique Windows pour les ports COM
 */
private void configureWindowsSerialPort(SerialPort port) {
    if (isWindows()) {
        // Configuration Windows spécifique
        port.setComPortTimeouts(SerialPort.TIMEOUT_READ_SEMI_BLOCKING, 2000, 1000);
        port.setRTS(true);
        port.setDTR(true);
        
        // Attendre que le port soit prêt
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

/**
 * Méthode améliorée pour la connexion avec gestion Windows
 */
private void connectDeviceWindows() {
    String portName = getSelectedPort();
    
    if (portName == null || portName.isEmpty()) {
        logMessage("✗ Aucun port sélectionné");
        return;
    }
    
    // Vérification spécifique Windows
    if (isWindows() && portName.startsWith("COM")) {
        // Vérifier si le port existe vraiment
        SerialPort[] availablePorts = SerialPort.getCommPorts();
        boolean portExists = false;
        for (SerialPort p : availablePorts) {
            if (p.getSystemPortName().equals(portName)) {
                portExists = true;
                break;
            }
        }
        
        if (!portExists) {
            logMessage("✗ Port " + portName + " n'existe pas dans le système");
            showWindowsPortHelp();
            return;
        }
    }
    
    // Suite de la connexion normale...
    serialPort = SerialPort.getCommPort(portName);
    
    if (serialPort == null) {
        logMessage("✗ Impossible d'obtenir le port " + portName);
        showWindowsPortHelp();
        return;
    }
    
    // Configuration Windows spécifique
    configureWindowsSerialPort(serialPort);
    
    // Configuration standard
    serialPort.setBaudRate(115200);
    serialPort.setNumDataBits(8);
    serialPort.setNumStopBits(1);
    serialPort.setParity(SerialPort.NO_PARITY);
    
    // Tentative d'ouverture avec gestion d'erreur Windows
    try {
        if (serialPort.openPort()) {
            serialInput = serialPort.getInputStream();
            serialOutput = serialPort.getOutputStream();
            
            isConnected = true;
            statusLabel.setText("Connecté - " + portName);
            statusLabel.setForeground(Color.GREEN);
            connectButton.setEnabled(false);
            disconnectButton.setEnabled(true);
            
            logMessage("✓ Connexion réussie au port: " + portName);
            logMessage("✓ Configuration: 115200 baud, 8N1");
            
        } else {
            logMessage("✗ Impossible d'ouvrir le port " + portName);
            showWindowsPortHelp();
        }
    } catch (Exception e) {
        logMessage("✗ Erreur de connexion: " + e.getMessage());
        showWindowsPortHelp();
    }
}

/**
 * Affiche l'aide spécifique Windows pour les problèmes de port COM
 */
private void showWindowsPortHelp() {
    if (isWindows()) {
        String helpMessage = 
            "Problème de port COM Windows détecté!\n\n" +
            "Solutions à essayer:\n" +
            "1. Installer le driver CH340 officiel:\n" +
            "   https://www.wch.cn/downloads/CH341SER_ZIP.html\n\n" +
            "2. Vérifier dans le Gestionnaire de périphériques:\n" +
            "   - Ports (COM & LPT)\n" +
            "   - Chercher des points d'exclamation jaunes\n\n" +
            "3. Redémarrer l'application en tant qu'Administrateur\n\n" +
            "4. Déconnecter et reconnecter le périphérique USB\n\n" +
            "5. Utiliser Windows-COM-Diagnostic.bat pour plus d'infos";
        
        JOptionPane.showMessageDialog(this, helpMessage, 
            "Aide Windows COM Port", JOptionPane.INFORMATION_MESSAGE);
    }
}

/**
 * Rafraîchir les ports avec détection Windows améliorée
 */
private void refreshPortsWindows() {
    portComboBox.removeAllItems();
    
    SerialPort[] ports = SerialPort.getCommPorts();
    logMessage("=== DÉTECTION PORTS WINDOWS ===");
    logMessage("Ports disponibles: " + ports.length);
    
    for (SerialPort port : ports) {
        String portName = port.getSystemPortName();
        String description = port.getDescriptivePortName();
        String portInfo = portName;
        
        if (description != null && !description.isEmpty()) {
            portInfo += ": " + description;
        }
        
        portComboBox.addItem(portInfo);
        logMessage("  " + portInfo);
        
        // Vérifier si c'est un périphérique Waveshare probable
        if (description != null && 
            (description.toLowerCase().contains("ch340") || 
             description.toLowerCase().contains("ch341") || 
             description.toLowerCase().contains("usb-serial"))) {
            logMessage("    → Périphérique Waveshare probable: " + portName);
        }
    }
    
    // Ajouter quelques ports COM standards pour Windows
    if (isWindows()) {
        for (int i = 1; i <= 20; i++) {
            String comPort = "COM" + i;
            boolean alreadyExists = false;
            
            for (int j = 0; j < portComboBox.getItemCount(); j++) {
                if (portComboBox.getItemAt(j).startsWith(comPort)) {
                    alreadyExists = true;
                    break;
                }
            }
            
            if (!alreadyExists) {
                portComboBox.addItem(comPort);
            }
        }
    }
    
    logMessage("=== FIN DÉTECTION PORTS ===");
}