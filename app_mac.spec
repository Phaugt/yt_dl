# -*- mode: python -*-

block_cipher = None



a = Analysis(['main.py'],
             pathex=['/Users/patrikhauguth/GIT/yt_dl'],
             binaries=None,
             datas=[('main.ui', '.'), ('./icons/*', 'icons')],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             **get_deps_all())
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='touchtracer',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, 
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='touchtracer')
app = BUNDLE(coll,
             name='touchtracer.app',
             icon=None,
         bundle_identifier=None)