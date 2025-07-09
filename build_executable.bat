@echo off
echo ================================================
echo  Creation de l'executable Waveshare CAN Tool
echo ================================================

echo Installation des dependances...
pip install pyinstaller pyserial python-can

echo Creation des fichiers de configuration...
python create_windows_executable.py

echo Compilation en cours...
pyinstaller --clean WaveshareCANTool.spec

echo ================================================
echo  Compilation terminee!
echo ================================================
echo L'executable se trouve dans le dossier: dist\WaveshareCANTool.exe
echo.
echo Pour tester l'executable:
echo cd dist
echo WaveshareCANTool.exe
echo.
pause
