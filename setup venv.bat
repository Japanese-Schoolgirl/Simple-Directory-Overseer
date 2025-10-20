@echo off
echo Python 3.9+ (along with pip and tkinter) must be installed.
pause

:generate_configs
call "setup config.bat"

set /p project_venv=<_venvName.txt
if [%project_venv%] == [] goto exit

set /p project_python=<PythonPath.txt
if [%project_python%] == [] set project_python=python

:create
%project_python% -m venv %project_venv%

call "%project_venv%/Scripts/activate"

pip install -r requirements.txt
call deactivate

:exit
echo Done!
pause
exit