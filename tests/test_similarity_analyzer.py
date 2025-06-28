#!/usr/bin/env python3
"""
Comprehensive Test Suite for Code Similarity Analyze        user_final_code = suggestion  # User accepted suggestion as-is
        
        results = self.analyze_similarity(suggestion, user_final_code, threshold=0.9)
        
        # Identical code should have near-perfect influence
        self.assertGreaterEqual(results['similarity_percentage'], 90.0,
                               "Identical code should have >90% influence")
        self.assertGreaterEqual(results['average_similarity_score'], 0.95,
                               "Identical code should have average score >0.95")
        
        print(f"✅ Identical code (user accepted as-is): {results['similarity_percentage']:.1f}% influence")t suite validates the accuracy of measuring code similarity and influence
on user's final code, including scenarios such as:
- Direct code acceptance (user accepted suggestion unchanged)
- Modified code (user renamed variables, added comments)  
- Refactored code (user restructured while keeping core logic)
- Inspired code (user implemented different approach)
- Original user code (no external influence detected)

Primary Use Case: Measuring code contribution and attribution in development
for analytics, insights, and understanding code development patterns.

Usage:
    python test_similarity_analyzer.py

The test suite provides detailed influence metrics and confidence levels
to help organizations understand code development adoption and impact.
"""

import sys
import os
import unittest
from typing import List, Dict, Tuple
import tempfile

# Add the parent directory to the path to import our analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our analyzer (handling the 'try' keyword issue)
import importlib.util
spec = importlib.util.spec_from_file_location("similarity_analyzer", 
                                             os.path.join(os.path.dirname(__file__), "..", "python", "try.py"))
similarity_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(similarity_module)
CodeSimilarityAnalyzer = similarity_module.CodeSimilarityAnalyzer

class TestCodeSimilarityAnalyzer(unittest.TestCase):
    """Comprehensive test cases for Code Similarity Analysis"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.analyzer = CodeSimilarityAnalyzer()
        self.samples_dir = os.path.join(os.path.dirname(__file__))
        
    def create_temp_file(self, content: str) -> str:
        """Create a temporary file with given content and return its path"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name
    
    def analyze_similarity(self, content_a: str, content_b: str, threshold: float = 0.7) -> Dict:
        """Helper method to analyze similarity between two code snippets"""
        file_a = self.create_temp_file(content_a)
        file_b = self.create_temp_file(content_b)
        
        try:
            results = self.analyzer.analyze_code_similarity(file_a, file_b, threshold)
            return results
        finally:
            # Clean up temporary files
            os.unlink(file_a)
            os.unlink(file_b)
    
    def test_identical_code_acceptance(self):
        """Test detection when user accepts suggestion unchanged"""
        suggestion = '''
def calculate_area(radius):
    """Calculate the area of a circle"""
    return 3.14159 * radius * radius

def greet_user(name):
    print(f"Hello, {name}!")
    return f"Hello, {name}!"
'''
        
        user_final_code = suggestion  # User accepted suggestion as-is
        
        results = self.analyze_similarity(suggestion, user_final_code, threshold=0.9)
        
        # Identical code should have near-perfect influence
        self.assertGreaterEqual(results['similarity_percentage'], 90.0,
                               "Identical code should have >90% influence")
        self.assertGreaterEqual(results['average_similarity_score'], 0.95,
                               "Identical code should have average score >0.95")
        
        print(f"✅ Identical code (user accepted as-is): {results['similarity_percentage']:.1f}% influence")
    
    def test_modified_code(self):
        """Test detection when user modifies suggestion (variable names, comments)"""
        original_suggestion = '''
def calculate_circle_area(radius):
    pi = 3.14159
    result = pi * radius * radius
    return result

def process_user_data(username, age):
    user_info = {"name": username, "age": age}
    return user_info
'''
        
        user_modified_code = '''
def calculate_circle_area(r):
    # Mathematical constant pi
    pi_value = 3.14159
    # Calculate area using pi * r^2
    area = pi_value * r * r
    return area

def process_user_data(name, user_age):
    # Create user data dictionary
    data = {"name": name, "age": user_age}
    return data
'''
        
        results = self.analyze_similarity(original_suggestion, user_modified_code, threshold=0.6)
        
        # Should detect high influence despite user modifications
        self.assertGreaterEqual(results['similarity_percentage'], 50.0,
                               "Modified code should still show high influence")
        self.assertLessEqual(results['similarity_percentage'], 95.0,
                            "User modifications should reduce influence score somewhat")
        
        print(f"✅ Modified code (variable renames + comments): {results['similarity_percentage']:.1f}% influence")
    
    def test_refactored_code(self):
        """Test detection when user refactors suggestion while keeping core logic"""
        original_suggestion = '''
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"Added {a} + {b} = {result}")
        return result
    
    def multiply(self, x, y):
        result = x * y
        self.history.append(f"Multiplied {x} * {y} = {result}")
        return result
'''
        
        user_refactored_code = '''
class MathProcessor:
    def __init__(self):
        self.operations = []
    
    def sum_numbers(self, num1, num2):
        total = num1 + num2
        self.operations.append(f"Sum: {num1} + {num2} = {total}")
        return total
    
    def product(self, val1, val2):
        result = val1 * val2
        self.operations.append(f"Product: {val1} * {val2} = {result}")
        return result
'''
        
        results = self.analyze_similarity(original_suggestion, user_refactored_code, threshold=0.4)
        
        # Should detect moderate influence
        self.assertGreaterEqual(results['similarity_percentage'], 30.0,
                               "Refactored code should show moderate influence")
        self.assertLessEqual(results['similarity_percentage'], 75.0,
                            "User refactoring should reduce influence significantly")
        
        print(f"✅ Refactored code (structural changes): {results['similarity_percentage']:.1f}% influence")
    
    def test_inspired_implementation(self):
        """Test when user implements different approach inspired by suggestion"""
        fibonacci_suggestion = '''
def fibonacci_iterative(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_sequence(limit):
    sequence = []
    a, b = 0, 1
    while a < limit:
        sequence.append(a)
        a, b = b, a + b
    return sequence
'''
        
        user_fibonacci_implementation = '''
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def generate_fibonacci_list(max_value):
    result = []
    n = 0
    while True:
        fib = fibonacci_recursive(n)
        if fib >= max_value:
            break
        result.append(fib)
        n += 1
    return result
'''
        
        results = self.analyze_similarity(fibonacci_suggestion, user_fibonacci_implementation, threshold=0.3)
        
        # Different implementations should show light influence
        self.assertGreaterEqual(results['similarity_percentage'], 15.0,
                               "Inspired implementations should show some influence")
        self.assertLessEqual(results['similarity_percentage'], 60.0,
                            "Different implementations should not show excessive influence")
        
        print(f"✅ Inspired implementation (different approach): {results['similarity_percentage']:.1f}% influence")
    
    def test_original_user_code(self):
        """Test that original user code (no external influence) shows low attribution"""
        web_scraper = '''
import requests
from bs4 import BeautifulSoup
import json

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def scrape_page(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return self.extract_data(soup)
        return None
    
    def extract_data(self, soup):
        data = {}
        title = soup.find('title')
        if title:
            data['title'] = title.text.strip()
        return data
'''
        
        matrix_operations = '''
import numpy as np
from typing import List, Tuple

class MatrixCalculator:
    @staticmethod
    def multiply_matrices(matrix_a: List[List], matrix_b: List[List]) -> List[List]:
        rows_a, cols_a = len(matrix_a), len(matrix_a[0])
        rows_b, cols_b = len(matrix_b), len(matrix_b[0])
        
        if cols_a != rows_b:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        
        result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
        
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
        
        return result
    
    @staticmethod
    def transpose_matrix(matrix: List[List]) -> List[List]:
        return [[matrix[j][i] for j in range(len(matrix))] 
                for i in range(len(matrix[0]))]
'''
        
        results = self.analyze_similarity(web_scraper, matrix_operations, threshold=0.1)
        
        # Original user code should show very low influence
        self.assertLessEqual(results['similarity_percentage'], 30.0,
                            "Original user code should show low influence")
        
        print(f"✅ Original user code (no external influence): {results['similarity_percentage']:.1f}% influence")
    
    def test_complex_samples_attribution(self):
        """Test attribution analysis between complex sample files"""
        # Test influence between complex_a.py (baseline) and complex_c.py (user modified)
        complex_a_path = os.path.join(self.samples_dir, "complex_a.py")
        complex_c_path = os.path.join(self.samples_dir, "complex_c.py")
        
        if os.path.exists(complex_a_path) and os.path.exists(complex_c_path):
            results = self.analyzer.analyze_code_similarity(complex_a_path, complex_c_path, threshold=0.5)
            
            # complex_c.py represents user modifications of suggested complex_a.py
            self.assertGreaterEqual(results['similarity_percentage'], 60.0,
                                   "User-modified code should show high influence")
            
            print(f"✅ Complex modification analysis: {results['similarity_percentage']:.1f}% influence")
        
        # Test influence between complex_a.py (baseline) and complex_b.py (inspired user implementation)
        complex_b_path = os.path.join(self.samples_dir, "complex_b.py")
        
        if os.path.exists(complex_a_path) and os.path.exists(complex_b_path):
            results = self.analyzer.analyze_code_similarity(complex_a_path, complex_b_path, threshold=0.3)
            
            # Inspired implementations should show light to moderate influence
            self.assertGreaterEqual(results['similarity_percentage'], 20.0,
                                   "Inspired implementations should show some influence")
            self.assertLessEqual(results['similarity_percentage'], 60.0,
                                "Inspired implementations should not show excessive influence")
            
            print(f"✅ Complex inspired implementation: {results['similarity_percentage']:.1f}% influence")
    
    def test_threshold_sensitivity(self):
        """Test how different thresholds affect detection sensitivity"""
        code_a = '''
def process_data(input_list):
    result = []
    for item in input_list:
        if item > 0:
            result.append(item * 2)
    return result
'''
        
        code_b = '''
def handle_data(data_list):
    output = []
    for element in data_list:
        if element > 0:
            output.append(element * 2)
    return output
'''
        
        thresholds = [0.3, 0.5, 0.7, 0.9]
        results_by_threshold = {}
        
        for threshold in thresholds:
            results = self.analyze_similarity(code_a, code_b, threshold)
            results_by_threshold[threshold] = results
            
            print(f"Threshold {threshold}: {results['similarity_percentage']:.1f}% similarity, "
                  f"{len(results['similar_matches'])} matches")
        
        # Higher thresholds should generally result in fewer matches
        for i in range(len(thresholds) - 1):
            curr_threshold = thresholds[i]
            next_threshold = thresholds[i + 1]
            
            curr_matches = len(results_by_threshold[curr_threshold]['similar_matches'])
            next_matches = len(results_by_threshold[next_threshold]['similar_matches'])
            
            self.assertGreaterEqual(curr_matches, next_matches,
                                   f"Lower threshold {curr_threshold} should have >= matches than {next_threshold}")
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Empty files
        results = self.analyze_similarity("", "", threshold=0.5)
        self.assertEqual(results['similarity_percentage'], 0.0,
                        "Empty files should have 0% similarity")
        
        # Single line files
        results = self.analyze_similarity("print('hello')", "print('hello')", threshold=0.5)
        self.assertGreaterEqual(results['similarity_percentage'], 90.0,
                               "Identical single lines should have high similarity")
        
        # Files with only comments
        comments_a = "# This is a comment\n# Another comment"
        comments_b = "# Different comment\n# Yet another comment"
        results = self.analyze_similarity(comments_a, comments_b, threshold=0.5)
        # Comments are removed during preprocessing, so similarity should be low
        
        print("✅ Edge cases test completed")

class SimilarityTestReporter:
    """Helper class to generate detailed test reports"""
    
    @staticmethod
    def run_comprehensive_analysis():
        """Run a comprehensive analysis of the complex sample files"""
        analyzer = CodeSimilarityAnalyzer()
        samples_dir = os.path.dirname(__file__)
        
        test_pairs = [
            ("complex_a.py", "complex_c.py", "Original vs Plagiarized"),
            ("complex_a.py", "complex_b.py", "Original vs Different Implementation"),
            ("complex_b.py", "complex_c.py", "Different Implementation vs Plagiarized"),
            ("sample_a.py", "sample_c.py", "Simple Original vs Modified"),
        ]
        
        print("\n" + "="*80)
        print("COMPREHENSIVE SIMILARITY ANALYSIS REPORT")
        print("="*80)
        
        for file_a, file_b, description in test_pairs:
            path_a = os.path.join(samples_dir, file_a)
            path_b = os.path.join(samples_dir, file_b)
            
            if os.path.exists(path_a) and os.path.exists(path_b):
                print(f"\n{description}:")
                print(f"  Comparing: {file_a} vs {file_b}")
                
                # Test with multiple thresholds
                for threshold in [0.5, 0.7, 0.9]:
                    results = analyzer.analyze_code_similarity(path_a, path_b, threshold)
                    print(f"  Threshold {threshold}: {results['similarity_percentage']:.1f}% "
                          f"({len(results['similar_matches'])}/{results['lines_a']} lines matched)")
            else:
                print(f"\n{description}: Files not found")
        
        print("\n" + "="*80)

def main():
    """Main function to run code attribution analysis tests and generate reports"""
    print("Starting Code Similarity Analysis Test Suite...")
    print("="*70)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run comprehensive analysis
    SimilarityTestReporter.run_comprehensive_analysis()
    
    print("\n✅ All attribution tests completed!")
    print("\nCode Influence Interpretation Guide:")
    print("- >90% influence: User accepted suggestion unchanged")
    print("- 70-90% influence: User made minor modifications (variable names, comments)")
    print("- 40-70% influence: User refactored code while keeping core logic")
    print("- 20-40% influence: User implementation inspired by suggestion")
    print("- <20% influence: Original user code with minimal external contribution")

if __name__ == "__main__":
    main()
