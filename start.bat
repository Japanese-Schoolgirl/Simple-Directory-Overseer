@echo off
set project_app="App/Simple Directory Overseer.pyw"
set /p project_venv=<_venvName.txt

call "%project_venv%/Scripts/activate"

::goto debug
start pythonw %project_app% :: pythonw is for hidden window

:close
call deactivate
exit

:debug
python %project_app%
pause
goto close