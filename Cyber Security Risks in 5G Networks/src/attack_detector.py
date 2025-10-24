#!/usr/bin/env python3
"""
5G Network Attack Detection Module
=================================

This module implements various attack detection algorithms for 5G networks.
It includes machine learning-based anomaly detection and rule-based systems.

Author: Cyber Security Research Team
Date: 2024
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
from collections import deque
import json

logger = logging.getLogger(__name__)

class AttackDetector:
    """
    Advanced attack detection system for 5G networks
    """
    
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.traffic_history = deque(maxlen=1000)
        self.attack_patterns = self._load_attack_patterns()
        self.detection_rules = self._initialize_detection_rules()
        
    def _load_attack_patterns(self) -> Dict:
        """Load known attack patterns for signature-based detection"""
        return {
            "ddos_patterns": {
                "high_packet_rate": 1000,  # packets per second
                "burst_threshold": 5000,   # packets in burst
                "duration_threshold": 10   # seconds
            },
            "jamming_patterns": {
                "signal_strength_threshold": 0.3,
                "consecutive_low_signals": 5,
                "frequency_deviation": 0.1
            },
            "mitm_patterns": {
                "anomaly_score_threshold": 0.7,
                "latency_increase": 2.0,  # factor
                "packet_modification_rate": 0.1
            }
        }
    
    def _initialize_detection_rules(self) -> Dict:
        """Initialize rule-based detection parameters"""
        return {
            "rate_limiting": {
                "max_requests_per_second": 100,
                "max_connections_per_ip": 50
            },
            "behavioral_analysis": {
                "unusual_time_patterns": True,
                "geographic_anomalies": True,
                "device_fingerprinting": True
            },
            "protocol_analysis": {
                "invalid_packet_structures": True,
                "protocol_violations": True,
                "encryption_weaknesses": True
            }
        }
    
    def detect_ddos_attack(self, traffic_data: List[Dict]) -> List[Dict]:
        """
        Detect DDoS attacks using multiple detection methods
        
        Args:
            traffic_data: List of traffic records
            
        Returns:
            List of detected DDoS attacks
        """
        logger.info("Detecting DDoS attacks...")
        attacks = []
        
        # Group traffic by time windows
        time_windows = self._group_by_time_windows(traffic_data, window_size=60)  # 1-minute windows
        
        for timestamp, traffic_window in time_windows.items():
            if not traffic_window:
                continue
                
            # Calculate metrics
            total_packets = sum(t["packet_count"] for t in traffic_window)
            unique_sources = len(set(t["source"] for t in traffic_window))
            avg_packet_size = np.mean([t["data_volume"] for t in traffic_window])
            
            # Rule-based detection
            if total_packets > self.attack_patterns["ddos_patterns"]["high_packet_rate"]:
                attack = {
                    "attack_type": "DDoS",
                    "timestamp": timestamp,
                    "severity": "HIGH",
                    "metrics": {
                        "total_packets": total_packets,
                        "unique_sources": unique_sources,
                        "avg_packet_size": avg_packet_size
                    },
                    "confidence": min(total_packets / 1000, 1.0)
                }
                attacks.append(attack)
                logger.warning(f"DDoS attack detected: {total_packets} packets from {unique_sources} sources")
        
        return attacks
    
    def detect_jamming_attack(self, traffic_data: List[Dict]) -> List[Dict]:
        """
        Detect jamming attacks based on signal strength analysis
        
        Args:
            traffic_data: List of traffic records
            
        Returns:
            List of detected jamming attacks
        """
        logger.info("Detecting jamming attacks...")
        attacks = []
        
        # Analyze signal strength patterns
        signal_data = [(t["timestamp"], t["signal_strength"]) for t in traffic_data if "signal_strength" in t]
        
        if not signal_data:
            return attacks
        
        # Group by time and location
        signal_df = pd.DataFrame(signal_data, columns=["timestamp", "signal_strength"])
        signal_df["time_window"] = signal_df["timestamp"].dt.floor("1min")
        
        for time_window, group in signal_df.groupby("time_window"):
            avg_signal = group["signal_strength"].mean()
            min_signal = group["signal_strength"].min()
            signal_variance = group["signal_strength"].var()
            
            # Detection criteria
            if (avg_signal < self.attack_patterns["jamming_patterns"]["signal_strength_threshold"] or
                min_signal < 0.2 or
                signal_variance > 0.1):
                
                attack = {
                    "attack_type": "Jamming",
                    "timestamp": time_window,
                    "severity": "MEDIUM",
                    "metrics": {
                        "avg_signal_strength": avg_signal,
                        "min_signal_strength": min_signal,
                        "signal_variance": signal_variance
                    },
                    "confidence": 1.0 - avg_signal
                }
                attacks.append(attack)
                logger.warning(f"Jamming attack detected: avg signal {avg_signal:.3f}")
        
        return attacks
    
    def detect_mitm_attack(self, traffic_data: List[Dict]) -> List[Dict]:
        """
        Detect man-in-the-middle attacks using anomaly detection
        
        Args:
            traffic_data: List of traffic records
            
        Returns:
            List of detected MITM attacks
        """
        logger.info("Detecting MITM attacks...")
        attacks = []
        
        # Extract features for anomaly detection
        features = []
        traffic_records = []
        
        for traffic in traffic_data:
            if all(key in traffic for key in ["packet_count", "latency", "data_volume"]):
                feature_vector = [
                    traffic["packet_count"],
                    traffic["latency"],
                    traffic["data_volume"],
                    traffic.get("signal_strength", 0.5),
                    traffic.get("anomaly_score", 0.0)
                ]
                features.append(feature_vector)
                traffic_records.append(traffic)
        
        if len(features) < 10:  # Need minimum data for detection
            return attacks
        
        # Convert to numpy array and scale
        X = np.array(features)
        X_scaled = self.scaler.fit_transform(X)
        
        # Use Isolation Forest for anomaly detection
        anomaly_scores = self.isolation_forest.fit_predict(X_scaled)
        
        # Identify anomalies
        for i, (score, traffic) in enumerate(zip(anomaly_scores, traffic_records)):
            if score == -1:  # Anomaly detected
                attack = {
                    "attack_type": "MITM",
                    "timestamp": traffic["timestamp"],
                    "severity": "CRITICAL",
                    "metrics": {
                        "anomaly_score": abs(self.isolation_forest.score_samples([X_scaled[i]])[0]),
                        "packet_count": traffic["packet_count"],
                        "latency": traffic["latency"]
                    },
                    "confidence": abs(self.isolation_forest.score_samples([X_scaled[i]])[0])
                }
                attacks.append(attack)
                logger.warning(f"MITM attack detected: anomaly score {attack['metrics']['anomaly_score']:.3f}")
        
        return attacks
    
    def detect_spoofing_attack(self, traffic_data: List[Dict]) -> List[Dict]:
        """
        Detect spoofing attacks by analyzing source address patterns
        
        Args:
            traffic_data: List of traffic records
            
        Returns:
            List of detected spoofing attacks
        """
        logger.info("Detecting spoofing attacks...")
        attacks = []
        
        # Analyze source address patterns
        source_analysis = {}
        
        for traffic in traffic_data:
            source = traffic["source"]
            if source not in source_analysis:
                source_analysis[source] = {
                    "packet_count": 0,
                    "data_volume": 0,
                    "first_seen": traffic["timestamp"],
                    "last_seen": traffic["timestamp"]
                }
            
            source_analysis[source]["packet_count"] += traffic["packet_count"]
            source_analysis[source]["data_volume"] += traffic["data_volume"]
            source_analysis[source]["last_seen"] = traffic["timestamp"]
        
        # Detect suspicious patterns
        for source, stats in source_analysis.items():
            # Check for rapid address changes (possible spoofing)
            time_span = (stats["last_seen"] - stats["first_seen"]).total_seconds()
            if time_span > 0:
                packet_rate = stats["packet_count"] / time_span
                
                # High packet rate from single source might indicate spoofing
                if packet_rate > 50:  # packets per second
                    attack = {
                        "attack_type": "Spoofing",
                        "timestamp": stats["last_seen"],
                        "severity": "HIGH",
                        "metrics": {
                            "source": source,
                            "packet_rate": packet_rate,
                            "total_packets": stats["packet_count"]
                        },
                        "confidence": min(packet_rate / 100, 1.0)
                    }
                    attacks.append(attack)
                    logger.warning(f"Spoofing attack detected from {source}: {packet_rate:.1f} pps")
        
        return attacks
    
    def _group_by_time_windows(self, traffic_data: List[Dict], window_size: int = 60) -> Dict:
        """Group traffic data by time windows"""
        windows = {}
        
        for traffic in traffic_data:
            timestamp = traffic["timestamp"]
            window_start = timestamp.replace(second=0, microsecond=0)
            window_start = window_start.replace(minute=(window_start.minute // (window_size // 60)) * (window_size // 60))
            
            if window_start not in windows:
                windows[window_start] = []
            windows[window_start].append(traffic)
        
        return windows
    
    def comprehensive_attack_detection(self, traffic_data: List[Dict]) -> Dict:
        """
        Perform comprehensive attack detection using all methods
        
        Args:
            traffic_data: List of traffic records
            
        Returns:
            Dictionary containing all detected attacks
        """
        logger.info("Performing comprehensive attack detection...")
        
        results = {
            "ddos_attacks": self.detect_ddos_attack(traffic_data),
            "jamming_attacks": self.detect_jamming_attack(traffic_data),
            "mitm_attacks": self.detect_mitm_attack(traffic_data),
            "spoofing_attacks": self.detect_spoofing_attack(traffic_data)
        }
        
        # Calculate overall statistics
        total_attacks = sum(len(attacks) for attacks in results.values())
        results["summary"] = {
            "total_attacks": total_attacks,
            "detection_timestamp": datetime.now().isoformat(),
            "traffic_records_analyzed": len(traffic_data)
        }
        
        logger.info(f"Comprehensive detection completed: {total_attacks} attacks detected")
        return results
    
    def generate_detection_report(self, detection_results: Dict) -> str:
        """
        Generate a detailed detection report
        
        Args:
            detection_results: Results from comprehensive_attack_detection
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("5G NETWORK ATTACK DETECTION REPORT")
        report.append("=" * 60)
        report.append(f"Detection Time: {detection_results['summary']['detection_timestamp']}")
        report.append(f"Traffic Records Analyzed: {detection_results['summary']['traffic_records_analyzed']}")
        report.append(f"Total Attacks Detected: {detection_results['summary']['total_attacks']}")
        report.append("")
        
        # DDoS attacks
        if detection_results["ddos_attacks"]:
            report.append("DDoS ATTACKS DETECTED:")
            for attack in detection_results["ddos_attacks"]:
                report.append(f"  - {attack['timestamp']}: {attack['metrics']['total_packets']} packets")
            report.append("")
        
        # Jamming attacks
        if detection_results["jamming_attacks"]:
            report.append("JAMMING ATTACKS DETECTED:")
            for attack in detection_results["jamming_attacks"]:
                report.append(f"  - {attack['timestamp']}: Signal strength {attack['metrics']['avg_signal_strength']:.3f}")
            report.append("")
        
        # MITM attacks
        if detection_results["mitm_attacks"]:
            report.append("MITM ATTACKS DETECTED:")
            for attack in detection_results["mitm_attacks"]:
                report.append(f"  - {attack['timestamp']}: Anomaly score {attack['metrics']['anomaly_score']:.3f}")
            report.append("")
        
        # Spoofing attacks
        if detection_results["spoofing_attacks"]:
            report.append("SPOOFING ATTACKS DETECTED:")
            for attack in detection_results["spoofing_attacks"]:
                report.append(f"  - {attack['timestamp']}: Source {attack['metrics']['source']}")
            report.append("")
        
        return "\n".join(report)

def main():
    """Demo function for attack detection"""
    print("5G Network Attack Detection System")
    print("=" * 40)
    
    # Initialize detector
    detector = AttackDetector()
    
    # Generate sample traffic data
    sample_traffic = []
    base_time = datetime.now()
    
    # Normal traffic
    for i in range(100):
        sample_traffic.append({
            "timestamp": base_time + timedelta(seconds=i),
            "source": f"UE-{i%10:03d}",
            "destination": f"gNB-{i%4+1:03d}",
            "packet_count": np.random.randint(10, 100),
            "data_volume": np.random.randint(100, 1000),
            "latency": np.random.uniform(1, 50),
            "signal_strength": np.random.uniform(0.7, 1.0)
        })
    
    # Add some attack traffic
    for i in range(20):
        sample_traffic.append({
            "timestamp": base_time + timedelta(seconds=100+i),
            "source": f"ATTACKER-{i:03d}",
            "destination": "gNB-001",
            "packet_count": np.random.randint(1000, 5000),
            "data_volume": np.random.randint(5000, 50000),
            "latency": np.random.uniform(100, 500),
            "signal_strength": np.random.uniform(0.1, 0.4),
            "is_attack": True
        })
    
    # Perform detection
    results = detector.comprehensive_attack_detection(sample_traffic)
    
    # Generate and print report
    report = detector.generate_detection_report(results)
    print(report)
    
    # Save results
    with open('simulation/attack_detection_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: simulation/attack_detection_results.json")

if __name__ == "__main__":
    main()
