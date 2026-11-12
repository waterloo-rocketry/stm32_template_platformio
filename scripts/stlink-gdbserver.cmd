@echo off
py -3 "%~dp0stlink_gdbserver.py" %*
if errorlevel 9009 python "%~dp0stlink_gdbserver.py" %*
