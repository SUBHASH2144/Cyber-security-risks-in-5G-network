@echo off
echo ========================================
echo Running Full 5G Security Simulation
echo ========================================
echo.

call venv\Scripts\activate.bat
python simulation/run_simulation.py --duration 300 --verbose

echo.
echo Full simulation completed. Check the simulation/ directory for detailed results.
pause
