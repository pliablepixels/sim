#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

# Import the module by importing the file directly
import importlib.util
spec = importlib.util.spec_from_file_location("code_analyzer", "python/try.py")
code_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(code_analyzer)

# Test documentation analysis
analyzer = code_analyzer.CodeSimilarityAnalyzer()
results = analyzer.analyze_code_similarity('samples/complex_a.py', 'samples/complex_b.py', 0.6)
analyzer.print_detailed_report(results)
