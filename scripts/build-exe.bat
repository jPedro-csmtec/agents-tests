@echo off
setlocal

echo ========================================
echo   Gerando arquivo .spec inicial...
echo ========================================

REM Gera um .spec temporário
pyinstaller --onefile interface.py

echo ========================================
echo   Sobrescrevendo arquivo .spec com configuração personalizada...
echo ========================================

REM Escreve diretamente o conteúdo personalizado no .spec
> interface.spec (
    echo # -*- mode: python ; coding: utf-8 -*-
    echo from PyInstaller.utils.hooks import collect_data_files, collect_submodules
    echo.
    echo # Importacoes ocultas necessarias
    echo hiddenimports = [
    echo     "gradio",
    echo     "gradio.blocks",
    echo     "gradio.components",
    echo     "gradio.components.annotated_image",
    echo     "gradio.processing_utils",
    echo     "gradio.oauth",
    echo     "gradio_client",
    echo     "gradio_client.client",
    echo     "gradio_client.serializing",
    echo     "gradio_client.compatibility",
    echo     "gradio._simple_templates",
    echo     "gradio._simple_templates.simpledropdown",
    echo     "safehttpx",
    echo     "tiktoken_ext.openai_public",
    echo     "tiktoken_ext",
    echo ]
    echo.
    echo datas = collect_data_files("gradio") + collect_data_files("gradio_client", includes=["*.json"])
    echo datas += collect_data_files("safehttpx")
    echo datas += collect_data_files("tiktoken")
    echo datas += collect_data_files("litellm", includes=["**/*.json"])
    echo datas += collect_data_files("pydantic")
    echo datas.append((".env", "."))
    echo.
    echo hiddenimports += collect_submodules("gradio")
    echo hiddenimports += collect_submodules("gradio_client")
    echo hiddenimports += collect_submodules("tiktoken")
    echo hiddenimports += collect_submodules("litellm")
    echo hiddenimports += collect_submodules("pydantic")
    echo.
    echo a = Analysis(
    echo     ['interface.py'],
    echo     pathex=[],
    echo     binaries=[],
    echo     datas=datas,
    echo     hiddenimports=hiddenimports,
    echo     hookspath=[],
    echo     hooksconfig={},
    echo     runtime_hooks=[],
    echo     excludes=[],
    echo     noarchive=False,
    echo     optimize=0,
    echo     module_collection_mode={ 'gradio': 'py' },
    echo )
    echo pyz = PYZ(a.pure)
    echo.
    echo exe = EXE(
    echo     pyz,
    echo     a.scripts,
    echo     a.binaries,
    echo     a.datas,
    echo     [],
    echo     name='shaun_back',
    echo     debug=False,
    echo     bootloader_ignore_signals=False,
    echo     strip=False,
    echo     upx=True,
    echo     upx_exclude=[],
    echo     runtime_tmpdir=None,
    echo     console=True,
    echo     disable_windowed_traceback=False,
    echo     argv_emulation=False,
    echo     target_arch=None,
    echo     codesign_identity=None,
    echo     entitlements_file=None,
    echo )
)

echo ========================================
echo   Compilando o .exe com arquivo .spec...
echo ========================================
pyinstaller interface.spec

echo ========================================
echo   Build finalizado com sucesso!
echo ========================================
pause
