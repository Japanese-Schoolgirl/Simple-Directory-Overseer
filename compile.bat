@echo off
set project_app="App/Simple Directory Overseer.pyw"
set /p project_venv=<_venvName.txt

set compile_dist="App/"
set compiler_files="_compile/"
:: Should be adjusted for specpath
set project_icon="../App/icon.png"

call "%project_venv%/Scripts/activate"

pip install pyinstaller
pyinstaller --onefile %project_app% --icon %project_icon% --distpath %compile_dist% --workpath %compiler_files% --specpath %compiler_files% --clean

call deactivate
pause
exit