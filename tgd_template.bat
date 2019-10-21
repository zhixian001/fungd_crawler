@echo off
:_loop
python .\run.py .\output.txt
pause
goto _loop
