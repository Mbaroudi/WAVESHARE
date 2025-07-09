@echo off
title Waveshare CAN Tool - Professional Configuration Suite
color 0A

echo.
echo ================================================================
echo   🚀 Waveshare CAN Tool - Professional Configuration Suite
echo ================================================================
echo   ✅ Real serial communication with hardware validation
echo   ✅ Advanced CAN configuration with all parameters
echo   ✅ JSON parameter management (save/load/apply)
echo   ✅ Transparent mode handling with smart fallback
echo   ✅ Multi-protocol support (OBD-II, J1939, ISO-TP, UDS)
echo   ✅ Cross-platform compatibility (Windows/Linux/macOS)
echo ================================================================
echo.

REM Check if Java is available
java -version >nul 2>&1
if errorlevel 1 (
    echo ❌ Java not found! Please install Java 8 or later.
    echo.
    echo To install Java:
    echo 1. Download from https://www.java.com/download/
    echo 2. Or install OpenJDK: https://openjdk.org/
    echo 3. Restart this script after installation
    echo.
    pause
    exit /b 1
)

REM Check if JAR file exists
if not exist "WaveshareCANTool-executable.jar" (
    echo ❌ WaveshareCANTool-executable.jar not found!
    echo.
    echo Please ensure the JAR file is in the same directory as this script.
    echo.
    pause
    exit /b 1
)

echo ✅ Java found - launching application...
echo.

REM Launch the application
java -jar WaveshareCANTool-executable.jar

REM Check if launch was successful
if errorlevel 1 (
    echo.
    echo ❌ Application failed to start!
    echo.
    echo Possible solutions:
    echo 1. Try running as administrator
    echo 2. Check if antivirus is blocking the application
    echo 3. Verify Java installation: java -version
    echo 4. Check if JAR file is corrupted
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Application closed successfully.
pause