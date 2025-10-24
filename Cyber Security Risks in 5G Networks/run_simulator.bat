@echo off
echo ========================================
echo Running 5G Network Simulator
echo ========================================
echo.

call venv\Scripts\activate.bat
python src/5g_network_simulator.py

echo.
echo Simulation completed. Check the simulation/ directory for outputs.
pause
