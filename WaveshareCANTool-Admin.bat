@echo off
title Waveshare CAN Tool - Administrator Mode
color 0A

echo.
echo ================================================================
echo   🚀 Waveshare CAN Tool - Administrator Mode
echo ================================================================
echo   ⚠️  Running with elevated privileges for COM port access
echo   ✅ Real serial communication with hardware validation
echo   ✅ Advanced CAN configuration with all parameters
echo   ✅ JSON parameter management (save/load/apply)
echo   ✅ Windows CH340 driver compatibility
echo ================================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Administrator privileges detected
) else (
    echo ❌ Administrator privileges required for COM port access
    echo.
    echo Please run this script as Administrator:
    echo 1. Right-click on this file
    echo 2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

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

echo ✅ Java found - launching application with admin privileges...
echo.

REM Launch the application with Windows-specific settings
java -Djava.library.path=. -Dfile.encoding=UTF-8 -Djava.security.policy=all.policy -jar WaveshareCANTool-executable.jar

REM Check if launch was successful
if errorlevel 1 (
    echo.
    echo ❌ Application failed to start!
    echo.
    echo Possible solutions:
    echo 1. Install CH340 driver: https://www.wch.cn/downloads/CH341SER_ZIP.html
    echo 2. Check Device Manager for COM port conflicts
    echo 3. Verify Java installation: java -version
    echo 4. Try disconnecting and reconnecting USB device
    echo 5. Check if another application is using the COM port
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Application closed successfully.
pause