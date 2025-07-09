@echo off
echo 🚀 Lancement de Waveshare CAN Tool Enhanced avec JSON Parameter Management
echo ================================================================
echo ✅ Support série réel avec jSerialComm
echo ✅ Configuration CAN avancée complète
echo ✅ Lecture et sauvegarde des paramètres en JSON
echo ✅ Interface professionnelle multi-onglets
echo ================================================================
echo.
echo Fonctionnalités disponibles:
echo • 📖 Lecture des paramètres périphérique
echo • 💾 Sauvegarde JSON des configurations
echo • 📂 Chargement de configurations JSON
echo • ✅ Application des paramètres au périphérique
echo • 🔄 Mise à jour temps réel
echo.
echo Démarrage de l'application...

REM Lancer l'application avec tous les composants
java -cp "lib/jSerialComm-2.10.4.jar;src/main/java" com.waveshare.cantool.WaveshareCANTool

echo.
echo Application fermée.
pause