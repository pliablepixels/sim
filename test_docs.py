#!/usr/bin/env python3

# Simple import from the python directory
from python.code_similarity_analyzer import CodeSimilarityAnalyzer

# Test documentation analysis
analyzer = CodeSimilarityAnalyzer()
results = analyzer.analyze_code_similarity('samples/complex_a.py', 'samples/complex_b.py', 0.6)
analyzer.print_detailed_report(results)
