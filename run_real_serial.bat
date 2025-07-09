@echo off
echo Lancement de Waveshare CAN Tool avec support serial reel...
echo ================================================
echo ATTENTION: Cette version detecte les vrais ports serie!
echo ================================================
echo.

REM Lancer l'application avec le support serial reel
java -cp "lib/jSerialComm-2.10.4.jar;src/main/java" com.waveshare.cantool.WaveshareCANTool

echo.
echo Application fermee.
pause