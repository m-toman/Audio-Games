# -*- mode: python -*-
a = Analysis(['..\\src\\memory.py'],
             pathex=['..'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas = list({tuple(map(str.upper, t)) for t in a.datas})
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='memory.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
