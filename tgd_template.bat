@echo off
:_loop
python .\fungd_crawler\tchang.py .\output.txt
pause
goto _loop
