@echo off
py -3 "%~dp0gcc_tool.py" "%~n0" %*
if errorlevel 9009 python "%~dp0gcc_tool.py" "%~n0" %*
