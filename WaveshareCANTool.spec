# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['waveshare_can_gui_windows.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('windows_config.json', '.'),
        ('industrial_profiles.json', '.'),
        ('README.md', '.'),
        ('icon.ico', '.'),
    ],
    hiddenimports=[
        'serial',
        'serial.tools.list_ports',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'json',
        'threading',
        'time',
        'datetime',
        'enum',
        'dataclasses',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WaveshareCANTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version='version_info.txt'
)