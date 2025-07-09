@echo off
title Windows COM Port Diagnostic Tool
color 0A

echo.
echo ================================================================
echo   🔍 Windows COM Port Diagnostic Tool
echo ================================================================
echo.

echo === SYSTEM INFORMATION ===
echo OS Version: %OS%
echo Computer: %COMPUTERNAME%
echo User: %USERNAME%
echo.

echo === JAVA INFORMATION ===
java -version
echo.

echo === COM PORT DETECTION ===
echo Available COM ports in system:
wmic path Win32_SerialPort get Name,Description,DeviceID
echo.

echo === USB DEVICES ===
echo USB Serial devices:
wmic path Win32_PnPEntity where "Name like '%%COM%%'" get Name,Status,DeviceID
echo.

echo === DEVICE MANAGER CHECK ===
echo Please check Device Manager for:
echo 1. Ports (COM ^& LPT) section
echo 2. Yellow warning triangles
echo 3. "USB-SERIAL CH340" or similar device
echo 4. Right-click on device → Properties → Driver tab
echo.

echo === REGISTRY COM PORTS ===
echo Checking registry for COM port assignments...
reg query "HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\SERIALCOMM"
echo.

echo === DRIVER RECOMMENDATIONS ===
echo If COM3 shows errors, try these drivers:
echo 1. CH340/CH341 Official: https://www.wch.cn/downloads/CH341SER_ZIP.html
echo 2. FTDI Official: https://www.ftdichip.com/Drivers/VCP.htm
echo 3. Prolific Official: http://www.prolific.com.tw/US/ShowProduct.aspx?p_id=225
echo.

echo === TROUBLESHOOTING STEPS ===
echo 1. Uninstall current driver in Device Manager
echo 2. Disconnect USB device
echo 3. Download and install correct driver
echo 4. Reconnect USB device
echo 5. Verify COM port appears without warnings
echo 6. Run this application as Administrator
echo.

echo === PROCESS CHECK ===
echo Checking if any process is using COM ports...
netstat -an | find "COM"
echo.

pause