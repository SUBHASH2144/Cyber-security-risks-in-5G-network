@echo off
echo ========================================
echo Running Attack Detection System
echo ========================================
echo.

call venv\Scripts\activate.bat
python src/attack_detector.py

echo.
echo Detection completed. Check the simulation/ directory for results.
pause
