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
    """Run the analyzer in interactive mode."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("\n=== INTERACTIVE MODE ===")
    print("Enter the paths to two files you want to compare:")
    
    file_a = input("Path to file A: ").strip()
    file_b = input("Path to file B: ").strip()
    
    if not os.path.exists(file_a):
        print(f"Error: File A '{file_a}' does not exist!")
        return
    
    if not os.path.exists(file_b):
        print(f"Error: File B '{file_b}' does not exist!")
        return
    
    threshold_input = input("Similarity threshold (0.0-1.0, default 0.7): ").strip()
    threshold = float(threshold_input) if threshold_input else 0.7
    
    print(f"\nAnalyzing files with threshold {threshold}...")
    results = analyzer.analyze_code_similarity(file_a, file_b, threshold)
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
    print("2. Interactive mode - compare your own files")
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
