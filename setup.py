import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico', 'settings.json', 'gui/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "mchat",
    version = "0.0.0",
    description = "mini chat",
    author = "Timo",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)


# add by timo to delete build file
print("---------start delete unused file by timo------")
import shutil

delete_file_list = ["./build/exe.win-amd64-3.8/lib/PySide6/designer.exe",
                    "./build/exe.win-amd64-3.8/lib/PySide6/linguist.exe",
                    "./build/exe.win-amd64-3.8/lib/PySide6/bin/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/examples/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/plugins/designer/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/scripts/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/translations/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/typesystems/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/lupdate.exe",
                    "./build/exe.win-amd64-3.8/lib/PySide6/opengl32sw.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/QtOpenGL.pyd",
                    "./build/exe.win-amd64-3.8/lib/PySide6/rcc.exe",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6Designer.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/uic.exe",
                    "./build/exe.win-amd64-3.8/lib/PySide6/qml/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/support/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/scripts/",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6OpenGL.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/QtOpenGL.pyi",
                    "./build/exe.win-amd64-3.8/lib/PySide6/d3dcompiler_47.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt63DRender.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6Quick.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6ShaderTools.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6DesignerComponents.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6VirtualKeyboard.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6QuickTemplates2.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6Quick3DRuntimeRender.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6DataVisualization.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt3DRender.pyd",
                    "./build/exe.win-amd64-3.8/lib/PySide6/ucrtbase.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt6Core5Compat.dll",
                    "./build/exe.win-amd64-3.8/lib/PySide6/QtDataVisualization.pyd",
                    "./build/exe.win-amd64-3.8/lib/PySide6/Qt63DExtras.dll"
           
                    ]

for file in delete_file_list:
    try:
        if os.path.isdir(file):
            print(f'start remove dir: {file}')
            shutil.rmtree(file)  
            print(f'remove ok')  
        elif os.path.isfile(file):
            print(f'start remove file: {file}')
            os.remove(file)
            print(f'remove ok')  
        else:
            print(f'{file} is not exist')

    except Exception as e:
        print(f'err: {e}')

print(f'remove end')  
