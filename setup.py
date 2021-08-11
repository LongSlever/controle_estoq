import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["PyQt5", "mysql.connector", "reportlab.pdfgen"], "include_files": ["aviso.ui", "formulario.ui", "listagemtela.ui", "menueditar.ui"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Cadastro de estoque",
    version="1.1",
    description="Minha 1° Aplicação!",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="controle.py", base = base)]
)