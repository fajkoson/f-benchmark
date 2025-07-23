@echo off
REM -----------------------------------------------
REM Run Factorio benchmark
REM Usage: benchmark.bat <folder> <cfg_name>
REM -----------------------------------------------


.env\scripts\python benchmark.py --mode bench 0001-iron-smelter

pause