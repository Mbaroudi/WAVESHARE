
; Script d'installation NSIS pour Waveshare CAN Tool
!include "MUI2.nsh"

; Informations générales
Name "Waveshare CAN Tool"
OutFile "WaveshareCANTool_Installer.exe"
InstallDir "$PROGRAMFILES\Waveshare CAN Tool"
RequestExecutionLevel admin

; Interface utilisateur moderne
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "French"

; Section d'installation
Section "Programme Principal" SecMain
    SetOutPath "$INSTDIR"
    
    ; Copier les fichiers
    File "dist\WaveshareCANTool.exe"
    File "windows_config.json"
    File "README.md"
    File "icon.ico"
    
    ; Créer le raccourci du menu démarrer
    CreateDirectory "$SMPROGRAMS\Waveshare CAN Tool"
    CreateShortcut "$SMPROGRAMS\Waveshare CAN Tool\Waveshare CAN Tool.lnk" "$INSTDIR\WaveshareCANTool.exe"
    CreateShortcut "$SMPROGRAMS\Waveshare CAN Tool\Désinstaller.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Créer le raccourci bureau
    CreateShortcut "$DESKTOP\Waveshare CAN Tool.lnk" "$INSTDIR\WaveshareCANTool.exe"
    
    ; Écrire les informations de désinstallation
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WaveshareCANTool" "DisplayName" "Waveshare CAN Tool"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WaveshareCANTool" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WaveshareCANTool" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WaveshareCANTool" "NoRepair" 1
    
    ; Créer le désinstalleur
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; Section de désinstallation
Section "Uninstall"
    ; Supprimer les fichiers
    Delete "$INSTDIR\WaveshareCANTool.exe"
    Delete "$INSTDIR\windows_config.json"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Supprimer les raccourcis
    Delete "$SMPROGRAMS\Waveshare CAN Tool\Waveshare CAN Tool.lnk"
    Delete "$SMPROGRAMS\Waveshare CAN Tool\Désinstaller.lnk"
    RMDir "$SMPROGRAMS\Waveshare CAN Tool"
    Delete "$DESKTOP\Waveshare CAN Tool.lnk"
    
    ; Supprimer le répertoire d'installation
    RMDir "$INSTDIR"
    
    ; Supprimer les entrées de registre
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WaveshareCANTool"
SectionEnd
