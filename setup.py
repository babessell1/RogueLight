import cx_Freeze
import os

executables = [cx_Freeze.Executable("main_game.py")]


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

build_exe_options = {'packages': ['pygame', 'tcod', 'constants'],
                     'include_files': [(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                                        os.path.join('lib', 'tcl86t.dll')),
                                       (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                        os.path.join('lib', 'tk86t.dll')),
                                        'constants.py',
                                        'libtcod.dll',
                                        'SDL2.dll',
                                        '__init__.py',
                                        'data',
                                        '__pycache__'
                                       # add here further files which need to be included as described in 1.
                                      ]}

cx_Freeze.setup(
    name="RogueLight",
    options={"build_exe": build_exe_options},
    executables = executables

)
dist_dir = "C:/Users/babes/Desktop/RogueLight/build/exe.win-amd64-3.7/"
numpy_core_dir = os.path.join(dist_dir, 'lib', 'numpy', 'core')
for file_name in os.listdir(numpy_core_dir):
    if file_name.lower().endswith('.dll'):
        file_path = os.path.join(numpy_core_dir, file_name)
        os.remove(file_path)
