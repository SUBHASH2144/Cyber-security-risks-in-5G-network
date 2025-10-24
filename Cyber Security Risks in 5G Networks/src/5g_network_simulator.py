#!/usr/bin/env python3
"""
5G Network Security Simulator
============================

This module simulates a 5G network environment and demonstrates various
cybersecurity threats and detection mechanisms.

Author: Cyber Security Research Team
Date: 2024
"""

import random
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('5g_security.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ThreatType(Enum):
    """Enumeration of 5G network threat types"""
    DDOS = "DDoS Attack"
    MITM = "Man-in-the-Middle"
    SPOOFING = "Spoofing Attack"
    JAMMING = "Jamming Attack"
    DATA_BREACH = "Data Privacy Breach"
    IMSI_CATCHING = "IMSI Catching"
    ROGUE_BASE_STATION = "Rogue Base Station"

class Severity(Enum):
    """Threat severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class NetworkNode:
    """Represents a 5G network node"""
    node_id: str
    node_type: str  # gNodeB, AMF, SMF, UPF, etc.
    ip_address: str
    location: Tuple[float, float]
    status: str = "active"
    security_level: int = 5  # 1-10 scale

@dataclass
class SecurityEvent:
    """Represents a security event in the network"""
    event_id: str
    timestamp: datetime
    threat_type: ThreatType
    severity: Severity
    source_node: str
    target_node: str
    description: str
    mitigation_status: str = "pending"

class FiveGNetworkSimulator:
    """
    Main simulator class for 5G network security analysis
    """
    
    def __init__(self):
        self.nodes: Dict[str, NetworkNode] = {}
        self.security_events: List[SecurityEvent] = []
        self.traffic_data: List[Dict] = []
        self.attack_patterns: Dict[ThreatType, List[Dict]] = defaultdict(list)
        self.detection_thresholds = {
            ThreatType.DDOS: 1000,  # packets per second
            ThreatType.JAMMING: 0.8,  # signal strength threshold
            ThreatType.MITM: 0.7,  # anomaly score threshold
        }
        
    def initialize_network(self):
        """Initialize a basic 5G network topology"""
        logger.info("Initializing 5G network topology...")
        
        # Core Network Elements
        core_nodes = [
            ("AMF-001", "AMF", "10.0.1.1", (0, 0)),
            ("SMF-001", "SMF", "10.0.1.2", (0, 1)),
            ("UPF-001", "UPF", "10.0.1.3", (0, 2)),
            ("AUSF-001", "AUSF", "10.0.1.4", (0, 3)),
            ("UDM-001", "UDM", "10.0.1.5", (0, 4)),
        ]
        
        # Radio Access Network
        ran_nodes = [
            ("gNB-001", "gNodeB", "10.0.2.1", (1, 0)),
            ("gNB-002", "gNodeB", "10.0.2.2", (1, 1)),
            ("gNB-003", "gNodeB", "10.0.2.3", (1, 2)),
            ("gNB-004", "gNodeB", "10.0.2.4", (1, 3)),
        ]
        
        # User Equipment
        ue_nodes = [
            ("UE-001", "User Equipment", "192.168.1.1", (2, 0)),
            ("UE-002", "User Equipment", "192.168.1.2", (2, 1)),
            ("UE-003", "User Equipment", "192.168.1.3", (2, 2)),
            ("UE-004", "User Equipment", "192.168.1.4", (2, 3)),
        ]
        
        all_nodes = core_nodes + ran_nodes + ue_nodes
        
        for node_id, node_type, ip, location in all_nodes:
            self.nodes[node_id] = NetworkNode(
                node_id=node_id,
                node_type=node_type,
                ip_address=ip,
                location=location
            )
        
        logger.info(f"Network initialized with {len(self.nodes)} nodes")
    
    def generate_normal_traffic(self, duration: int = 60):
        """Generate normal network traffic patterns"""
        logger.info(f"Generating normal traffic for {duration} seconds...")
        
        for second in range(duration):
            for node_id, node in self.nodes.items():
                if node.node_type == "User Equipment":
                    # Simulate normal UE traffic
                    traffic = {
                        "timestamp": datetime.now(),
                        "source": node_id,
                        "destination": random.choice(list(self.nodes.keys())),
                        "packet_count": random.randint(10, 100),
                        "data_volume": random.randint(100, 1000),  # bytes
                        "latency": random.uniform(1, 50),  # ms
                        "signal_strength": random.uniform(0.7, 1.0),
                        "is_attack": False
                    }
                    self.traffic_data.append(traffic)
        
        logger.info(f"Generated {len(self.traffic_data)} traffic records")
    
    def simulate_ddos_attack(self, target_node: str, duration: int = 30):
        """Simulate a DDoS attack on a target node"""
        logger.warning(f"Simulating DDoS attack on {target_node}")
        
        attack_start = datetime.now()
        attack_packets = 0
        
        for second in range(duration):
            # Generate high volume of malicious packets
            packet_count = random.randint(1000, 5000)  # Much higher than normal
            attack_packets += packet_count
            
            traffic = {
                "timestamp": datetime.now(),
                "source": f"ATTACKER-{random.randint(1000, 9999)}",
                "destination": target_node,
                "packet_count": packet_count,
                "data_volume": packet_count * random.randint(50, 200),
                "latency": random.uniform(100, 500),  # Higher latency
                "signal_strength": random.uniform(0.3, 0.6),  # Weaker signal
                "is_attack": True,
                "attack_type": "DDoS"
            }
            self.traffic_data.append(traffic)
        
        # Create security event
        event = SecurityEvent(
            event_id=f"DDOS-{int(time.time())}",
            timestamp=attack_start,
            threat_type=ThreatType.DDOS,
            severity=Severity.HIGH,
            source_node="Multiple Attackers",
            target_node=target_node,
            description=f"DDoS attack with {attack_packets} packets over {duration} seconds"
        )
        self.security_events.append(event)
        
        logger.warning(f"DDoS attack completed: {attack_packets} packets sent")
    
    def simulate_jamming_attack(self, target_area: Tuple[float, float], radius: float = 1.0):
        """Simulate a jamming attack in a specific area"""
        logger.warning(f"Simulating jamming attack in area {target_area}")
        
        affected_nodes = []
        for node_id, node in self.nodes.items():
            distance = np.sqrt((node.location[0] - target_area[0])**2 + 
                            (node.location[1] - target_area[1])**2)
            if distance <= radius:
                affected_nodes.append(node_id)
                # Degrade signal strength
                node.status = "degraded"
        
        event = SecurityEvent(
            event_id=f"JAM-{int(time.time())}",
            timestamp=datetime.now(),
            threat_type=ThreatType.JAMMING,
            severity=Severity.MEDIUM,
            source_node="Unknown Jammer",
            target_node=f"Area {target_area}",
            description=f"Jamming attack affecting {len(affected_nodes)} nodes"
        )
        self.security_events.append(event)
        
        logger.warning(f"Jamming attack affecting {len(affected_nodes)} nodes")
    
    def simulate_mitm_attack(self, target_connection: Tuple[str, str]):
        """Simulate a man-in-the-middle attack"""
        source, destination = target_connection
        logger.warning(f"Simulating MITM attack between {source} and {destination}")
        
        # Create malicious traffic that appears to be from legitimate source
        malicious_traffic = {
            "timestamp": datetime.now(),
            "source": source,
            "destination": destination,
            "packet_count": random.randint(50, 200),
            "data_volume": random.randint(500, 2000),
            "latency": random.uniform(20, 100),
            "signal_strength": random.uniform(0.4, 0.8),
            "is_attack": True,
            "attack_type": "MITM",
            "anomaly_score": random.uniform(0.7, 0.9)  # High anomaly score
        }
        self.traffic_data.append(malicious_traffic)
        
        event = SecurityEvent(
            event_id=f"MITM-{int(time.time())}",
            timestamp=datetime.now(),
            threat_type=ThreatType.MITM,
            severity=Severity.CRITICAL,
            source_node="Attacker",
            target_node=f"{source} -> {destination}",
            description="Man-in-the-middle attack detected"
        )
        self.security_events.append(event)
    
    def detect_anomalies(self) -> List[Dict]:
        """Detect anomalies in network traffic"""
        logger.info("Analyzing traffic for anomalies...")
        
        anomalies = []
        
        # Group traffic by time windows
        time_windows = defaultdict(list)
        for traffic in self.traffic_data:
            minute = traffic["timestamp"].minute
            time_windows[minute].append(traffic)
        
        # Analyze each time window
        for minute, traffic_list in time_windows.items():
            if not traffic_list:
                continue
                
            # Calculate statistics
            packet_counts = [t["packet_count"] for t in traffic_list]
            avg_packets = np.mean(packet_counts)
            max_packets = np.max(packet_counts)
            
            # DDoS detection
            if max_packets > self.detection_thresholds[ThreatType.DDOS]:
                anomalies.append({
                    "type": "DDoS",
                    "timestamp": datetime.now(),
                    "severity": "HIGH",
                    "description": f"Unusual packet volume: {max_packets} packets",
                    "affected_nodes": len(set(t["destination"] for t in traffic_list))
                })
            
            # Signal strength analysis
            signal_strengths = [t["signal_strength"] for t in traffic_list]
            avg_signal = np.mean(signal_strengths)
            
            if avg_signal < self.detection_thresholds[ThreatType.JAMMING]:
                anomalies.append({
                    "type": "Jamming",
                    "timestamp": datetime.now(),
                    "severity": "MEDIUM",
                    "description": f"Low signal strength: {avg_signal:.2f}",
                    "affected_nodes": len(traffic_list)
                })
            
            # Anomaly score analysis
            for traffic in traffic_list:
                if "anomaly_score" in traffic and traffic["anomaly_score"] > self.detection_thresholds[ThreatType.MITM]:
                    anomalies.append({
                        "type": "MITM",
                        "timestamp": traffic["timestamp"],
                        "severity": "CRITICAL",
                        "description": f"High anomaly score: {traffic['anomaly_score']:.2f}",
                        "source": traffic["source"],
                        "destination": traffic["destination"]
                    })
        
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies
    
    def generate_security_report(self) -> Dict:
        """Generate a comprehensive security report"""
        logger.info("Generating security report...")
        
        total_events = len(self.security_events)
        total_traffic = len(self.traffic_data)
        attack_traffic = len([t for t in self.traffic_data if t.get("is_attack", False)])
        
        # Event statistics by type
        event_stats = defaultdict(int)
        for event in self.security_events:
            event_stats[event.threat_type.value] += 1
        
        # Severity distribution
        severity_stats = defaultdict(int)
        for event in self.security_events:
            severity_stats[event.severity.value] += 1
        
        report = {
            "summary": {
                "total_security_events": total_events,
                "total_traffic_records": total_traffic,
                "attack_traffic_percentage": (attack_traffic / total_traffic * 100) if total_traffic > 0 else 0,
                "network_nodes": len(self.nodes)
            },
            "threat_distribution": dict(event_stats),
            "severity_distribution": dict(severity_stats),
            "recent_events": [
                {
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "threat_type": event.threat_type.value,
                    "severity": event.severity.value,
                    "description": event.description
                }
                for event in self.security_events[-10:]  # Last 10 events
            ]
        }
        
        return report
    
    def visualize_network_topology(self):
        """Create a visualization of the network topology"""
        logger.info("Creating network topology visualization...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Color mapping for node types
        node_colors = {
            "AMF": "red",
            "SMF": "blue", 
            "UPF": "green",
            "AUSF": "orange",
            "UDM": "purple",
            "gNodeB": "cyan",
            "User Equipment": "gray"
        }
        
        # Plot nodes
        for node_id, node in self.nodes.items():
            color = node_colors.get(node.node_type, "black")
            ax.scatter(node.location[0], node.location[1], 
                      c=color, s=100, alpha=0.7, label=node.node_type)
            ax.annotate(node_id, (node.location[0], node.location[1]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax.set_title("5G Network Topology", fontsize=16, fontweight='bold')
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.grid(True, alpha=0.3)
        
        # Add legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        plt.tight_layout()
        plt.savefig('simulation/network_topology.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def visualize_traffic_analysis(self):
        """Create traffic analysis visualizations"""
        logger.info("Creating traffic analysis visualizations...")
        
        if not self.traffic_data:
            logger.warning("No traffic data available for visualization")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Packet count over time
        timestamps = [t["timestamp"] for t in self.traffic_data]
        packet_counts = [t["packet_count"] for t in self.traffic_data]
        
        ax1.plot(timestamps, packet_counts, alpha=0.7)
        ax1.set_title("Packet Count Over Time")
        ax1.set_ylabel("Packets")
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Signal strength distribution
        signal_strengths = [t["signal_strength"] for t in self.traffic_data]
        ax2.hist(signal_strengths, bins=20, alpha=0.7, color='skyblue')
        ax2.set_title("Signal Strength Distribution")
        ax2.set_xlabel("Signal Strength")
        ax2.set_ylabel("Frequency")
        
        # 3. Attack vs Normal traffic
        attack_traffic = [t for t in self.traffic_data if t.get("is_attack", False)]
        normal_traffic = [t for t in self.traffic_data if not t.get("is_attack", False)]
        
        labels = ['Normal Traffic', 'Attack Traffic']
        sizes = [len(normal_traffic), len(attack_traffic)]
        colors = ['lightgreen', 'red']
        
        ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax3.set_title("Traffic Distribution")
        
        # 4. Latency analysis
        latencies = [t["latency"] for t in self.traffic_data]
        ax4.boxplot(latencies)
        ax4.set_title("Network Latency Distribution")
        ax4.set_ylabel("Latency (ms)")
        
        plt.tight_layout()
        plt.savefig('simulation/traffic_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Main function to run the 5G security simulation"""
    print("=" * 60)
    print("5G Network Security Simulator")
    print("=" * 60)
    
    # Initialize simulator
    simulator = FiveGNetworkSimulator()
    simulator.initialize_network()
    
    # Generate normal traffic
    simulator.generate_normal_traffic(duration=30)
    
    # Simulate various attacks
    print("\nSimulating security threats...")
    simulator.simulate_ddos_attack("gNB-001", duration=10)
    simulator.simulate_jamming_attack((1, 1), radius=0.5)
    simulator.simulate_mitm_attack(("UE-001", "gNB-001"))
    
    # Detect anomalies
    print("\nDetecting anomalies...")
    anomalies = simulator.detect_anomalies()
    
    # Generate report
    print("\nGenerating security report...")
    report = simulator.generate_security_report()
    
    # Save report to file
    with open('simulation/security_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Create visualizations
    print("\nCreating visualizations...")
    simulator.visualize_network_topology()
    simulator.visualize_traffic_analysis()
    
    # Print summary
    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)
    print(f"Total Network Nodes: {report['summary']['network_nodes']}")
    print(f"Total Traffic Records: {report['summary']['total_traffic_records']}")
    print(f"Security Events: {report['summary']['total_security_events']}")
    print(f"Attack Traffic: {report['summary']['attack_traffic_percentage']:.1f}%")
    print(f"Anomalies Detected: {len(anomalies)}")
    
    print("\nThreat Distribution:")
    for threat, count in report['threat_distribution'].items():
        print(f"  {threat}: {count}")
    
    print(f"\nDetailed report saved to: simulation/security_report.json")
    print(f"Visualizations saved to: simulation/ directory")

if __name__ == "__main__":
    main()
