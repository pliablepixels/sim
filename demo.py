#!/usr/bin/env python3
"""
Demo script for the Code Similarity Analyzer.
This script demonstrates how to use the algorithm to compare two files.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the code similarity analyzer
from python.code_similarity_analyzer import CodeSimilarityAnalyzer
import os

def demo_comparison():
    """Demo the code similarity analyzer with sample files."""
    analyzer = CodeSimilarityAnalyzer()
    
    # Define paths to our sample files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_a = os.path.join(current_dir, "sample_a.py")
    file_b = os.path.join(current_dir, "sample_c.py")
    
    print("=== CODE SIMILARITY ANALYZER DEMO ===")
    print(f"Comparing:\n  File A: {file_a}\n  File B: {file_b}\n")
    
    # Test with different similarity thresholds
    thresholds = [0.5, 0.7, 0.9]
    
    for threshold in thresholds:
        print(f"\n{'='*60}")
        print(f"ANALYSIS WITH THRESHOLD: {threshold}")
        print(f"{'='*60}")
        
        results = analyzer.analyze_code_similarity(file_a, file_b, threshold)
        analyzer.print_detailed_report(results)
        
        # Show some example line comparisons
        if results.get('similar_matches'):
            print("\nDetailed Line Comparisons:")
            print("-" * 40)
            
            lines_a = analyzer.preprocess_file(file_a)
            lines_b = analyzer.preprocess_file(file_b)
            
            # Show first 3 matches in detail
            for i, (line_a_idx, line_b_idx, score) in enumerate(results['similar_matches'][:3]):
                print(f"\nMatch {i+1} (Score: {score:.3f}):")
                print(f"  A[{line_a_idx+1}]: {lines_a[line_a_idx].strip()}")
                print(f"  B[{line_b_idx+1}]: {lines_b[line_b_idx].strip()}")

def interactive_mode():
    """Run the analyzer in interactive mode with auto file/text detection."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("\n=== INTERACTIVE MODE ===")
    print("Enter file paths or code text")
    print("(If files don't exist, input will be treated as code text)")
    
    input_a = input("\nEnter first file path or code text: ").strip()
    input_b = input("Enter second file path or code text: ").strip()
    
    # Get similarity threshold from user
    threshold_input = input("\nEnter similarity threshold (0.0-1.0, default 0.7): ").strip()
    threshold = float(threshold_input) if threshold_input else 0.7
    
    # Auto-detect if inputs are files or text
    is_file_a = os.path.isfile(input_a)
    is_file_b = os.path.isfile(input_b)
    
    if is_file_a and is_file_b:
        # Both are files
        print(f"\nDetected: Both inputs are files")
        results = analyzer.analyze_code_similarity(input_a, input_b, threshold, is_file=True)
    elif not is_file_a and not is_file_b:
        # Both are text
        print(f"\nDetected: Both inputs are code text")
        results = analyzer.analyze_code_similarity(input_a, input_b, threshold, is_file=False)
    else:
        # Mixed - one file, one text (treat both as text for consistency)
        print(f"\nDetected: Mixed input types - treating both as code text")
        # If one is a file, read it as text
        if is_file_a:
            try:
                with open(input_a, 'r', encoding='utf-8', errors='ignore') as f:
                    input_a = f.read()
            except Exception as e:
                print(f"Error reading file {input_a}: {e}")
                input_a = ""
        if is_file_b:
            try:
                with open(input_b, 'r', encoding='utf-8', errors='ignore') as f:
                    input_b = f.read()
            except Exception as e:
                print(f"Error reading file {input_b}: {e}")
                input_b = ""
        results = analyzer.analyze_code_similarity(input_a, input_b, threshold, is_file=False)
    
    analyzer.print_detailed_report(results)

def demo_documentation_analysis():
    """Demo documentation and comment analysis with complex files."""
    analyzer = CodeSimilarityAnalyzer()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "=" * 60)
    print("DOCUMENTATION ANALYSIS DEMO")
    print("=" * 60)
    print("This demo tests the analyzer's ability to detect similarity")
    print("in code with extensive documentation and comments.\n")
    
    # Test with complex files if they exist
    complex_a = os.path.join(current_dir, 'samples', 'complex_a.py')
    complex_b = os.path.join(current_dir, 'samples', 'complex_b.py')
    
    if os.path.exists(complex_a) and os.path.exists(complex_b):
        print(f"Analyzing complex files with documentation...")
        results = analyzer.analyze_code_similarity(complex_a, complex_b, 0.6)
        analyzer.print_detailed_report(results)
    else:
        print("Complex sample files not found. Using basic samples instead.")
        sample_a = os.path.join(current_dir, 'samples', 'sample_a.py')
        sample_c = os.path.join(current_dir, 'samples', 'sample_c.py')
        
        if os.path.exists(sample_a) and os.path.exists(sample_c):
            results = analyzer.analyze_code_similarity(sample_a, sample_c, 0.6)
            analyzer.print_detailed_report(results)

def main():
    """Main function to run the demo."""
    print("Code Similarity Analyzer")
    print("1. Run demo with sample files")
    print("2. Interactive mode - compare your own files or text")
    print("3. Documentation analysis demo")
    
    choice = input("\nChoose an option (1, 2, or 3): ").strip()
    
    if choice == "1":
        demo_comparison()
    elif choice == "2":
        interactive_mode()
    elif choice == "3":
        demo_documentation_analysis()
    else:
        print("Invalid choice. Running demo by default.")
        demo_comparison()

if __name__ == "__main__":
    main()
