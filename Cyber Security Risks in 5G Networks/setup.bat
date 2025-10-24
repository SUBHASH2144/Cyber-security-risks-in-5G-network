@echo off
echo ========================================
echo 5G Network Security Project Setup
echo ========================================
echo.

echo Creating Python virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    echo Please ensure Python is installed and in your PATH
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing project dependencies...
pip install -r src/requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating simulation output directory...
if not exist simulation mkdir simulation

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the project:
echo   1. Open VS Code in this directory
echo   2. Use Ctrl+Shift+P and select "Python: Select Interpreter"
echo   3. Choose the venv\Scripts\python.exe interpreter
echo   4. Use F5 to run the simulator or use the Run and Debug panel
echo.
echo Available run commands:
echo   - setup.bat (this script)
echo   - run_simulator.bat
echo   - run_detection.bat
echo   - run_full_simulation.bat
echo.
pause
