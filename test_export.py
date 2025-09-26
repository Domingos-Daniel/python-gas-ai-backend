#!/usr/bin/env python3
"""
Test script for export functionality
"""
import json
from app.export_utils import DataExporter

def test_export_functionality():
    """Test various export scenarios"""
    exporter = DataExporter()
    
    # Test data - sample chat messages
    test_messages = [
        {
            "id": "1",
            "role": "user",
            "content": "What is the oil production in Angola?",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "id": "2", 
            "role": "assistant",
            "content": "According to recent data, Angola's oil production is approximately 1.2 million barrels per day...",
            "timestamp": "2024-01-15T10:30:15Z"
        }
    ]
    
    # Test data - sample analysis
    test_analysis = {
        "title": "Angola Oil Production Analysis",
        "subtitle": "Comprehensive analysis of oil sector",
        "analysis_category": "oil_production",
        "confidence": 0.85,
        "total_items": 150,
        "contextual_analysis": {
            "executive_summary": "Angola's oil production shows positive trends",
            "title": "Production Analysis",
            "confidence": 0.85
        },
        "kpis": {
            "production_volume": {
                "current": 1200000,
                "target": 1300000,
                "status": "good",
                "trend": "increasing"
            },
            "revenue": {
                "current": 45000000000,
                "target": 50000000000,
                "status": "satisfactory",
                "trend": "stable"
            }
        },
        "trends": {
            "monthly": ["increasing", "stable", "increasing"],
            "yearly": ["positive", "very_positive"]
        },
        "recommendations": [
            {
                "category": "Production",
                "priority": "High",
                "recommendation": "Increase investment in offshore drilling",
                "impact": "High"
            }
        ],
        "data": {
            "Q1": 1150000,
            "Q2": 1200000,
            "Q3": 1250000,
            "Q4": 1300000
        }
    }
    
    print("Testing export functionality...")
    
    # Test 1: Export chat messages to Excel
    print("\n1. Testing chat export to Excel...")
    try:
        result = exporter.export_chat_history(test_messages, 'xlsx')
        print(f"✓ Chat Excel export successful: {len(result)} bytes")
    except Exception as e:
        print(f"✗ Chat Excel export failed: {e}")
    
    # Test 2: Export chat messages to CSV
    print("\n2. Testing chat export to CSV...")
    try:
        result = exporter.export_chat_history(test_messages, 'csv')
        print(f"✓ Chat CSV export successful: {len(result)} bytes")
    except Exception as e:
        print(f"✗ Chat CSV export failed: {e}")
    
    # Test 3: Export analysis to Excel
    print("\n3. Testing analysis export to Excel...")
    try:
        result = exporter.export_analysis_data(test_analysis, 'xlsx')
        print(f"✓ Analysis Excel export successful: {len(result)} bytes")
    except Exception as e:
        print(f"✗ Analysis Excel export failed: {e}")
    
    # Test 4: Export chart data
    print("\n4. Testing chart export...")
    try:
        chart_data = {
            "labels": ["Jan", "Feb", "Mar", "Apr"],
            "values": [100, 200, 150, 300],
            "chart_type": "bar",
            "title": "Monthly Production"
        }
        result = exporter.export_chart_data(chart_data, 'xlsx')
        print(f"✓ Chart export successful: {len(result)} bytes")
    except Exception as e:
        print(f"✗ Chart export failed: {e}")
    
    # Test 5: Export to JSON
    print("\n5. Testing JSON export...")
    try:
        result = exporter.export_chat_history(test_messages, 'json')
        print(f"✓ JSON export successful: {len(result)} bytes")
    except Exception as e:
        print(f"✗ JSON export failed: {e}")
    
    print("\n✓ All export tests completed!")

if __name__ == "__main__":
    test_export_functionality()