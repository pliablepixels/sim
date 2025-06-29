#!/usr/bin/env python3
"""
Cross-language test comparison script to verify Python and TypeScript 
implementations behave consistently
"""

import sys
import os
import tempfile

# Simple import from the python directory
from python.code_similarity_analyzer import CodeSimilarityAnalyzer

def test_equivalent_cases():
    """Test cases that should behave the same across Python and TypeScript"""
    
    analyzer = CodeSimilarityAnalyzer()
    
    print("=== PYTHON EQUIVALENT TESTS (Matching TypeScript) ===")
    print("=" * 70)
    
    # Test 1: Structural Modifications (equivalent to TypeScript test)
    print("\n1. Testing Structural Modifications...")
    
    original_code = '''class DataProcessor:
    def __init__(self):
        self.data = []

    def add_data(self, value):
        self.data.append(value)

    def calculate_average(self):
        if len(self.data) == 0:
            return 0
        total = sum(self.data)
        return total / len(self.data)

    def get_max_value(self):
        return max(self.data) if self.data else 0

    def get_min_value(self):
        return min(self.data) if self.data else 0
'''

    modified_code = '''class NumberAnalyzer:
    def __init__(self):
        self.numbers = []

    def insert_number(self, num):
        self.numbers.append(num)

    def compute_mean(self):
        if len(self.numbers) == 0:
            return 0
        total = sum(self.numbers)
        return total / len(self.numbers)

    def find_maximum(self):
        return max(self.numbers) if self.numbers else 0

    def find_minimum(self):
        return min(self.numbers) if self.numbers else 0

    def get_count(self):
        return len(self.numbers)
'''

    # Create temp files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1:
        f1.write(original_code)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
        f2.write(modified_code)
        file2 = f2.name
    
    try:
        results = analyzer.analyze_code_similarity(file1, file2, 0.4)
        print(f"   Structural modifications similarity: {results['similarity_percentage']:.1f}%")
        print(f"   Expected: 30-70%, TypeScript got: 100.0%")
        
        if results['similarity_percentage'] >= 30.0 and results['similarity_percentage'] <= 70.0:
            print("   ✅ Python: Within expected range")
        else:
            print("   ❌ Python: Outside expected range")
            
    finally:
        os.unlink(file1)
        os.unlink(file2)
    
    # Test 2: Different Implementations Same Logic
    print("\n2. Testing Different Implementations Same Logic...")
    
    binary_search_iterative = '''def binary_search_iterative(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def sort_array(numbers):
    return sorted(numbers)
'''

    binary_search_recursive = '''def binary_search_recursive(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1
        
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

def arrange_numbers(data):
    return sorted(data)
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1:
        f1.write(binary_search_iterative)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
        f2.write(binary_search_recursive)
        file2 = f2.name
    
    try:
        results = analyzer.analyze_code_similarity(file1, file2, 0.3)
        print(f"   Different implementations similarity: {results['similarity_percentage']:.1f}%")
        print(f"   Expected: 15-60%, TypeScript got: 100.0%")
        
        if results['similarity_percentage'] >= 15.0 and results['similarity_percentage'] <= 60.0:
            print("   ✅ Python: Within expected range")
        else:
            print("   ❌ Python: Outside expected range")
            
    finally:
        os.unlink(file1)
        os.unlink(file2)
    
    # Test 3: Completely Unrelated Code
    print("\n3. Testing Completely Unrelated Code...")
    
    api_client = '''class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        try:
            import requests
            response = requests.get(f"{self.base_url}/{endpoint}")
            
            return {
                'data': response.json(),
                'status': response.status_code,
                'message': 'Success' if response.ok else 'Error'
            }
        except Exception as error:
            raise Exception(f"Network error: {error}")

    def post(self, endpoint, body):
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                json=body,
                headers={'Content-Type': 'application/json'}
            )
            
            return {
                'data': response.json(),
                'status': response.status_code,
                'message': 'Success' if response.ok else 'Error'
            }
        except Exception as error:
            raise Exception(f"Network error: {error}")
'''

    geometry_calculations = '''import math

class GeometryCalculator:
    @staticmethod
    def calculate_distance(point1, point2):
        dx = point2['x'] - point1['x']
        dy = point2['y'] - point1['y']
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def calculate_rectangle_area(rectangle):
        return rectangle['width'] * rectangle['height']

    @staticmethod
    def calculate_rectangle_perimeter(rectangle):
        return 2 * (rectangle['width'] + rectangle['height'])

    @staticmethod
    def is_point_inside_rectangle(point, rect, origin):
        return (
            point['x'] >= origin['x'] and
            point['x'] <= origin['x'] + rect['width'] and
            point['y'] >= origin['y'] and
            point['y'] <= origin['y'] + rect['height']
        )

    @staticmethod
    def calculate_triangle_area(base, height):
        return 0.5 * base * height
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1:
        f1.write(api_client)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
        f2.write(geometry_calculations)
        file2 = f2.name
    
    try:
        results = analyzer.analyze_code_similarity(file1, file2, 0.1)
        print(f"   Unrelated code similarity: {results['similarity_percentage']:.1f}%")
        print(f"   Expected: ≤30%, TypeScript got: 51.5%")
        
        if results['similarity_percentage'] <= 30.0:
            print("   ✅ Python: Within expected range")
        else:
            print("   ❌ Python: Outside expected range")
            
    finally:
        os.unlink(file1)
        os.unlink(file2)
    
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    print("This comparison helps identify if the TypeScript implementation")
    print("is overly sensitive compared to the Python implementation.")

if __name__ == "__main__":
    test_equivalent_cases()
