@echo off

rem Activate the Python environment
call .\Scripts\activate

rem Run the Python script
python make_short_reddit.py

rem Deactivate the Python environment
call deactivate

Pause