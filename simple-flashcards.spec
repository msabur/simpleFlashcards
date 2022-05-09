# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['simple-flashcards.py'],
             pathex=[],
             binaries=[],
             datas=[('design.glade', '.'), ('icon.png', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={
				 "gi": {
					 "icons": ["Adwaita"],
					 "themes": ["Adwaita"],
					 "languages": ["en_US", "en_GB"],
					 "module-versions": {
						 "Gtk": "3.0",
					 },
				 },
			 },
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='simple-flashcards',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icon.png')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='simple-flashcards')
