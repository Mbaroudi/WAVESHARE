#!/bin/bash
echo "Lancement de Waveshare CAN Tool avec support serial reel..."
echo "================================================"
echo "ATTENTION: Cette version detecte les vrais ports serie!"
echo "================================================"
echo ""

# Lancer l'application avec le support serial reel
java -cp "/Users/malek/WAVE-SHARE/lib/jSerialComm-2.10.4.jar:/Users/malek/WAVE-SHARE/src/main/java" com.waveshare.cantool.WaveshareCANTool

echo ""
echo "Application fermee."