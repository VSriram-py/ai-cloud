@echo off
REM Quick Start Script for DR-MAS Test Suite (Windows)

echo ==================================
echo DR-MAS Test Suite - Quick Start
echo ==================================
echo.

REM Check Python version
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To run the tests:
echo 1. Activate environment: venv\Scripts\activate
echo 2. Launch Jupyter: jupyter notebook DR_MAS_Comprehensive_Test_Suite.ipynb
echo 3. Run all cells in the notebook
echo.
pause
