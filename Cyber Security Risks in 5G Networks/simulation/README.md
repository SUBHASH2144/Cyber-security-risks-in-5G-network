# Simulation Directory

This directory contains simulation outputs, sample data, and configuration files for the 5G Network Security project.

## 📁 Directory Contents

### Configuration Files
- **`network_configuration.json`**: Network topology and security configuration
- **`attack_scenarios.json`**: Predefined attack scenarios and mitigation strategies
- **`sample_traffic_data.json`**: Sample network traffic data for testing

### Simulation Scripts
- **`run_simulation.py`**: Main simulation runner script
- **`README.md`**: This documentation file

### Output Files (Generated during simulation)
- **`network_topology.png`**: Network topology visualization
- **`traffic_analysis.png`**: Traffic analysis charts
- **`security_report.json`**: Comprehensive security analysis report
- **`attack_detection_results.json`**: Detailed attack detection results
- **`simulation.log`**: Simulation execution log
- **`traffic_data.json`**: Complete traffic data from simulation

## 🚀 Running Simulations

### Basic Simulation
```bash
# Run default simulation (5 minutes)
python run_simulation.py

# Run with custom duration (10 minutes)
python run_simulation.py --duration 600

# Run with verbose logging
python run_simulation.py --verbose
```

### Specific Attack Scenarios
```bash
# Run DDoS attack scenario
python run_simulation.py --scenario SCENARIO-001

# Run jamming attack scenario
python run_simulation.py --scenario SCENARIO-002

# Run MITM attack scenario
python run_simulation.py --scenario SCENARIO-003
```

### Available Scenarios
- **SCENARIO-001**: Distributed DDoS Attack
- **SCENARIO-002**: Signal Jamming Attack
- **SCENARIO-003**: Man-in-the-Middle Attack
- **SCENARIO-004**: Rogue Base Station Attack
- **SCENARIO-005**: Core Network Infiltration

## 📊 Understanding Output Files

### Network Topology Visualization
The `network_topology.png` file shows:
- Network node positions and connections
- Node types (AMF, SMF, UPF, gNodeB, UE)
- Security boundaries and attack surfaces

### Traffic Analysis Charts
The `traffic_analysis.png` file includes:
- Packet count over time
- Signal strength distribution
- Attack vs normal traffic breakdown
- Network latency analysis

### Security Report
The `security_report.json` file contains:
- Summary statistics
- Threat distribution
- Severity analysis
- Recent security events
- Performance metrics

### Attack Detection Results
The `attack_detection_results.json` file includes:
- Detected attacks by type
- Detection confidence scores
- Attack metrics and timestamps
- Mitigation recommendations

## 🔧 Customizing Simulations

### Network Configuration
Edit `network_configuration.json` to modify:
- Network topology
- Security thresholds
- Detection parameters
- Mitigation strategies

### Attack Scenarios
Edit `attack_scenarios.json` to:
- Add new attack scenarios
- Modify attack parameters
- Update mitigation strategies
- Configure detection metrics

### Sample Data
Use `sample_traffic_data.json` for:
- Testing detection algorithms
- Validating simulation logic
- Benchmarking performance
- Development and debugging

## 📈 Performance Monitoring

### Key Metrics
- **Detection Accuracy**: Percentage of correctly identified attacks
- **False Positive Rate**: Percentage of false alarms
- **Response Time**: Time from attack to detection
- **Mitigation Effectiveness**: Success rate of countermeasures

### Monitoring Commands
```bash
# Monitor simulation progress
tail -f simulation/simulation.log

# Check detection results
cat simulation/attack_detection_results.json | jq '.summary'

# View security report
cat simulation/security_report.json | jq '.summary'
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Permission Errors
```bash
# Fix file permissions
chmod +x run_simulation.py
chmod 755 simulation/
```

#### 2. Missing Dependencies
```bash
# Install required packages
pip install -r ../src/requirements.txt
```

#### 3. Memory Issues
```bash
# Reduce simulation size
python run_simulation.py --duration 60
```

#### 4. Visualization Problems
```bash
# Use non-interactive backend
export MPLBACKEND=Agg
python run_simulation.py
```

### Debug Mode
```bash
# Enable debug logging
python run_simulation.py --verbose

# Check log file
tail -f simulation/simulation.log
```

## 📚 Additional Resources

### Documentation
- **Main Report**: `../docs/CyberSecurity_5G_Report.md`
- **Presentation**: `../presentation/5G_Security_Presentation.md`
- **Project README**: `../README.md`

### Source Code
- **Simulator**: `../src/5g_network_simulator.py`
- **Detector**: `../src/attack_detector.py`
- **Dependencies**: `../src/requirements.txt`

### Support
- **Issues**: Report problems via GitHub Issues
- **Documentation**: Check comprehensive documentation
- **Community**: Join research community discussions

---

*This simulation framework is designed for educational and research purposes. For production use, additional security measures and testing are recommended.*
