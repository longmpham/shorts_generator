@echo off

echo Activate the Python environment
call .\virtual_env\Scripts\activate

echo Run the Python script
python make_short_reddit.py

echo Deactivate the Python environment
call deactivate

Pause