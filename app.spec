# -*- mode: python ; coding: utf-8 -*-
def find_library(name):
    paths = [
        f'/System/Library/Frameworks/{name}.framework/{name}',
        f'/usr/lib/lib{name}.dylib',
        f'{name}.dylib',
    ]

    for path in paths:
        try:
            cdll.LoadLibrary(path)
            return path
        except OSError:
            pass

    return None
block_cipher = None
import sys

a = Analysis(['app.py'],
             pathex=['/Users/patrikhauguth/GIT/yt_dl'],
             binaries=[( '/usr/lib/libiodbc.2.dylib', '.' ) ],
             datas=[('main.ui', '.'), ('./icons/*', 'icons')],
             hiddenimports=['PyQt5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
if sys.platform == 'darwin':
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='YT_DL',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon='./icons/yt_bl.ico')
if sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
    exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='YT Downloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='./icons/yt_bl.ico',
          console=False )
if sys.platform == 'darwin':
    app = BUNDLE(exe,
                name='YT_DL.app',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                },
                icon='./icons/yt_bl.ico')
if sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
    coll = COLLECT(coll,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='YT_DL')
