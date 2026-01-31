#!/bin/bash
# Quick Start Script for DR-MAS Test Suite

echo "=================================="
echo "DR-MAS Test Suite - Quick Start"
echo "=================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "To run the tests:"
echo "1. Activate environment: source venv/bin/activate (or venv\Scripts\activate on Windows)"
echo "2. Launch Jupyter: jupyter notebook DR_MAS_Comprehensive_Test_Suite.ipynb"
echo "3. Run all cells in the notebook"
echo ""
