#!/usr/bin/env python3
"""
Test script to verify the 5G Network Security project setup
"""

import sys
import os

print("=" * 60)
print("5G Network Security Project - Setup Test")
print("=" * 60)

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Check if we can import required packages
print("\nTesting package imports...")
try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ numpy import failed: {e}")

try:
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported successfully")
except ImportError as e:
    print(f"✗ matplotlib import failed: {e}")

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ pandas import failed: {e}")

try:
    import sklearn
    print("✓ scikit-learn imported successfully")
except ImportError as e:
    print(f"✗ scikit-learn import failed: {e}")

try:
    import networkx as nx
    print("✓ networkx imported successfully")
except ImportError as e:
    print(f"✗ networkx import failed: {e}")

# Check project structure
print("\nChecking project structure...")
directories = ['src', 'simulation', 'docs', 'presentation']
for directory in directories:
    if os.path.exists(directory):
        print(f"✓ {directory}/ directory exists")
        files = os.listdir(directory)
        if files:
            print(f"  Files: {files}")
        else:
            print(f"  Directory is empty")
    else:
        print(f"✗ {directory}/ directory not found")

# Test basic functionality
print("\nTesting basic functionality...")
try:
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Test numpy
    test_array = np.array([1, 2, 3, 4, 5])
    print(f"✓ NumPy test: {test_array.mean()}")
    
    # Test matplotlib (non-interactive)
    plt.ioff()  # Turn off interactive mode
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax.set_title("Test Plot")
    plt.savefig('test_plot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("✓ Matplotlib test: Plot saved as test_plot.png")
    
except Exception as e:
    print(f"✗ Basic functionality test failed: {e}")

print("\n" + "=" * 60)
print("Setup test completed!")
print("=" * 60)
