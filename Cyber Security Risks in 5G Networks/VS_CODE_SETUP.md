# VS Code Setup Guide for 5G Network Security Project

This guide will help you set up and run the 5G Network Security project in Visual Studio Code.

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.8+** installed on your system
- **Visual Studio Code** with Python extension
- **Git** (optional, for version control)

### 2. Project Setup

#### Option A: Automated Setup (Recommended)
1. **Run the setup script:**
   ```bash
   setup.bat
   ```
   This will:
   - Create a Python virtual environment
   - Install all required dependencies
   - Set up the project structure

#### Option B: Manual Setup
1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r src/requirements.txt
   ```

### 3. VS Code Configuration

The project includes pre-configured VS Code settings:

- **`.vscode/settings.json`** - Python interpreter and linting settings
- **`.vscode/launch.json`** - Debug configurations for different scenarios
- **`.vscode/tasks.json`** - Build and run tasks

## 🎯 Running the Project

### Method 1: Using VS Code Debug Panel

1. **Open VS Code** in the project directory
2. **Select Python Interpreter:**
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose `./venv/Scripts/python.exe`

3. **Run Simulations:**
   - Press `F5` or go to Run and Debug panel
   - Select from available configurations:
     - **Run 5G Network Simulator** - Basic network simulation
     - **Run Attack Detector** - Attack detection system
     - **Run Simulation with Scenario** - Specific attack scenario
     - **Run Full Simulation** - Complete security analysis

### Method 2: Using Batch Scripts

Run these scripts from the command line:

```bash
# Run basic simulator
run_simulator.bat

# Run attack detection
run_detection.bat

# Run full simulation
run_full_simulation.bat
```

### Method 3: Using VS Code Tasks

1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select from available tasks:
   - Setup Python Environment
   - Install Dependencies
   - Run 5G Simulator
   - Run Attack Detection
   - Run Full Simulation
   - Clean Output Files

## 📊 Understanding the Output

### Generated Files
The simulation creates several output files in the `simulation/` directory:

- **`network_topology.png`** - Visual network diagram
- **`traffic_analysis.png`** - Traffic analysis charts
- **`security_report.json`** - Detailed security analysis
- **`attack_detection_results.json`** - Attack detection results
- **`simulation.log`** - Execution log

### Key Metrics
- **Detection Accuracy** - Percentage of correctly identified attacks
- **False Positive Rate** - Percentage of false alarms
- **Response Time** - Time from attack to detection
- **Network Performance** - Impact of security measures

## 🔧 Customization

### Running Specific Scenarios
```bash
# Run DDoS attack scenario
python simulation/run_simulation.py --scenario SCENARIO-001

# Run jamming attack scenario
python simulation/run_simulation.py --scenario SCENARIO-002

# Run with custom duration
python simulation/run_simulation.py --duration 600
```

### Modifying Detection Parameters
Edit `src/attack_detector.py` to adjust:
- Detection thresholds
- Attack patterns
- Detection algorithms

### Customizing Network Topology
Edit `src/5g_network_simulator.py` to modify:
- Network nodes
- Connections
- Traffic patterns

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Not Found
```bash
# Check Python installation
python --version

# If not found, install Python from python.org
```

#### 2. Virtual Environment Issues
```bash
# Delete and recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
```

#### 3. Import Errors
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r src/requirements.txt
```

#### 4. Permission Errors
```bash
# Run VS Code as administrator
# Or check file permissions
```

#### 5. Memory Issues
- Reduce simulation duration
- Close other applications
- Increase system memory

### Debug Mode
Enable debug logging by adding to your Python files:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Project Structure

```
Cyber Security Risks in 5G Networks/
├── .vscode/                    # VS Code configuration
│   ├── settings.json          # Python settings
│   ├── launch.json            # Debug configurations
│   └── tasks.json             # Build tasks
├── src/                       # Source code
│   ├── 5g_network_simulator.py
│   ├── attack_detector.py
│   └── requirements.txt
├── simulation/                # Simulation outputs
├── docs/                     # Documentation
├── presentation/             # Presentation materials
├── setup.bat                 # Setup script
├── run_simulator.bat         # Run simulator
├── run_detection.bat         # Run detection
├── run_full_simulation.bat   # Run full simulation
└── VS_CODE_SETUP.md          # This guide
```

## 🎓 Learning Resources

### Understanding 5G Security
- Read `docs/CyberSecurity_5G_Report.md` for comprehensive analysis
- Review `presentation/5G_Security_Presentation.md` for key concepts

### Code Documentation
- All Python files include detailed comments
- Function docstrings explain parameters and return values
- Inline comments describe complex algorithms

### Experimentation
- Modify attack parameters in `simulation/attack_scenarios.json`
- Adjust detection thresholds in the source code
- Create custom network topologies
- Implement new attack types

## 🤝 Getting Help

### VS Code Features
- **IntelliSense** - Auto-completion and suggestions
- **Debugging** - Set breakpoints and step through code
- **Integrated Terminal** - Run commands without leaving VS Code
- **Git Integration** - Version control support

### Python Features
- **Type Hints** - Better code understanding
- **Docstrings** - Function documentation
- **Logging** - Debug information
- **Error Handling** - Graceful error management

## 🚀 Next Steps

1. **Run the basic simulator** to understand the network topology
2. **Execute attack detection** to see how threats are identified
3. **Modify parameters** to experiment with different scenarios
4. **Read the documentation** to understand the underlying concepts
5. **Create custom scenarios** for specific research needs

---

**Happy coding!** 🎉

For additional support, check the project README.md or create an issue in the project repository.
