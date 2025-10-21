@echo off
if not exist "_venvName.txt" echo|set /p="_Environment">"_venvName.txt"
if not exist "PythonPath.txt" copy NUL "PythonPath.txt"
if not exist "Config/" md "Config"
if not exist "Config/IgnoreWatchlist.txt" echo|set /p="RegExp: (?i)\.cat$">"Config/IgnoreWatchlist.txt"
if not exist "Config/Watchlist.txt" echo|set /p="C:\">"Config/Watchlist.txt"
if not exist "Config/Settings.txt" echo|set /p="language: en">"Config/Settings.txt"