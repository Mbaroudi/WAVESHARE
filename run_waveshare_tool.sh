#!/bin/bash
echo "Lancement de Waveshare CAN Tool..."
java -jar dist/WaveshareCANTool.jar

if [ $? -ne 0 ]; then
    echo ""
    echo "Erreur: Java n'est pas installe ou JAR introuvable"
    echo ""
    echo "Verifiez que:"
    echo "1. Java est installe (java -version)"
    echo "2. Le fichier JAR existe dans dist/"
    echo "3. Le JAR a ete compile avec build_jar.sh"
    echo ""
fi
