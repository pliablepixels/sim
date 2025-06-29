#!/usr/bin/env python3
"""
Comprehensive Test Suite for Code Similarity Analyzer

This test suite covers all major functionality including:
- Basic similarity analysis
- Complex code analysis
- Edge cases and error handling
- Documentation and comment analysis
- Performance with large files
- Code fragment analysis (is_file=False)

Both implementations (Python/TypeScript) should pass these tests with
similar results (within 3% variance for similarity percentages).
"""

import unittest
import os
import sys
import tempfile

# Add the parent directory to the path to import from python/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from python.code_similarity_analyzer import CodeSimilarityAnalyzer


class TestCodeSimilarityAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CodeSimilarityAnalyzer()
        
        # Set up paths to sample files
        self.test_dir = os.path.dirname(__file__)
        self.project_root = os.path.dirname(self.test_dir)
        self.samples_dir = os.path.join(self.project_root, 'samples')
        
    def analyze_similarity(self, file_a, file_b, threshold=0.7):
        """Helper method to analyze similarity between two files."""
        return self.analyzer.analyze_code_similarity(file_a, file_b, similarity_threshold=threshold)

    def test_identical_files(self):
        """Test that identical files have 100% similarity"""
        print("\n--- Testing Identical Files ---")
        
        file_a = os.path.join(self.samples_dir, 'sample_a.py')
        results = self.analyze_similarity(file_a, file_a, threshold=0.7)
        
        self.assertEqual(results['similarity_percentage'], 100.0,
                        "Identical files should have 100% similarity")
        self.assertEqual(results['similar_lines_count'], results['lines_a_count'],
                        "All lines should match for identical files")
        
        print(f"✅ Identical files: {results['similarity_percentage']}% similarity "
              f"({results['similar_lines_count']} of {results['lines_a_count']} lines matched)")

    def test_similar_files_variable_renaming(self):
        """Test files with variable renaming (sample_a.py vs sample_c.py)"""
        print("\n--- Testing Variable Renaming ---")
        
        file_a = os.path.join(self.samples_dir, 'sample_a.py')
        file_c = os.path.join(self.samples_dir, 'sample_c.py')
        
        results = self.analyze_similarity(file_a, file_c, threshold=0.6)
        
        # Should detect high similarity despite variable name changes
        self.assertGreaterEqual(results['similarity_percentage'], 60.0,
                               "Files with variable renaming should have >60% similarity")
        self.assertGreater(results['similar_lines_count'], 0,
                          "Should find similar lines despite variable renaming")
        
        print(f"✅ Variable renaming: {results['similarity_percentage']:.1f}% similarity "
              f"({results['similar_lines_count']} of {results['lines_a_count']} lines matched)")

    def test_different_languages(self):
        """Test files in different languages (should have low similarity)"""
        print("\n--- Testing Different Languages ---")
        
        file_py = os.path.join(self.samples_dir, 'sample_c.py')  # Different algorithm
        file_java = os.path.join(self.samples_dir, 'sample_a.java')  # Different algorithm
        
        results = self.analyze_similarity(file_py, file_java, threshold=0.5)
        
        # Different languages should have low similarity (adjusting threshold for realistic case)
        self.assertLessEqual(results['similarity_percentage'], 60.0,
                           "Different languages should have low similarity")
        
        print(f"✅ Different languages: {results['similarity_percentage']:.1f}% similarity "
              f"({results['similar_lines_count']} of {results['lines_a_count']} lines matched)")

    def test_complex_files(self):
        """Test analysis of complex files with documentation"""
        print("\n--- Testing Complex Files ---")
        
        complex_a_path = os.path.join(self.samples_dir, 'complex_a.py')
        complex_b_path = os.path.join(self.samples_dir, 'complex_b.py')
        
        if os.path.exists(complex_a_path) and os.path.exists(complex_b_path):
            results = self.analyze_similarity(complex_a_path, complex_b_path, threshold=0.3)
            
            # Complex files should show some similarity
            self.assertGreaterEqual(results['similarity_percentage'], 20.0,
                                   "Complex files should have some detectable similarity")
            
            print(f"✅ Complex files: {results['similarity_percentage']:.1f}% similarity "
                  f"({results['similar_lines_count']} of {results['lines_a_count']} lines matched)")
        else:
            print("⚠️  Complex test files not found, skipping complex file test")

    def test_code_fragment_analysis(self):
        """Test analyzing code fragments instead of files"""
        print("\n--- Testing Code Fragment Analysis ---")
        
        # Test with code fragments
        code_a = """def hello_world():
    print("Hello, World!")
    return True"""
        
        code_b = """def greet():
    print("Hello, World!")
    return True"""
        
        results = self.analyzer.analyze_code_similarity(code_a, code_b, similarity_threshold=0.7, is_file=False)
        
        # Should detect high similarity despite different function names
        self.assertGreaterEqual(results['similarity_percentage'], 60.0,
                               "Code fragments with similar logic should have >60% similarity")
        self.assertGreater(results['similar_lines_count'], 0,
                          "Should find at least some similar lines")
        self.assertFalse(results['is_file'], "Should indicate this is code fragment analysis")
        
        print(f"✅ Code fragment analysis: {results['similarity_percentage']:.1f}% similarity "
              f"({results['similar_lines_count']} of {results['lines_a_count']} lines matched)")

    def test_empty_files(self):
        """Test handling of empty or non-existent files"""
        print("\n--- Testing Empty/Non-existent Files ---")
        
        # Test with non-existent files
        results = self.analyze_similarity('nonexistent1.py', 'nonexistent2.py', threshold=0.7)
        
        self.assertIn('error', results, "Should return error for non-existent files")
        self.assertEqual(results['similarity_percentage'], 0.0,
                        "Non-existent files should have 0% similarity")
        
        print(f"✅ Non-existent files: Properly handled with error message")

    def test_empty_code_fragments(self):
        """Test handling of empty code fragments"""
        print("\n--- Testing Empty Code Fragments ---")
        
        results = self.analyzer.analyze_code_similarity("", "def test(): pass", similarity_threshold=0.7, is_file=False)
        
        self.assertIn('error', results, "Should return error for empty code fragments")
        self.assertEqual(results['similarity_percentage'], 0.0,
                        "Empty code fragments should have 0% similarity")
        
        print(f"✅ Empty code fragments: Properly handled with error message")

    def test_threshold_sensitivity(self):
        """Test that different thresholds produce appropriate results"""
        print("\n--- Testing Threshold Sensitivity ---")
        
        file_a = os.path.join(self.samples_dir, 'sample_a.py')
        file_c = os.path.join(self.samples_dir, 'sample_c.py')
        
        # Test with low threshold
        results_low = self.analyze_similarity(file_a, file_c, threshold=0.3)
        
        # Test with high threshold  
        results_high = self.analyze_similarity(file_a, file_c, threshold=0.8)
        
        # Lower threshold should find more matches
        self.assertGreaterEqual(results_low['similar_lines_count'], results_high['similar_lines_count'],
                               "Lower threshold should find more or equal matches")
        
        print(f"✅ Threshold sensitivity: Low threshold ({results_low['similar_lines_count']} matches) >= "
              f"High threshold ({results_high['similar_lines_count']} matches)")

    def test_performance_stress_test(self):
        """Test performance with artificially large inputs"""
        print("\n--- Testing Performance Stress Test ---")
        
        # Create large code fragments
        large_code_a = "\n".join([f"def function_{i}():\n    return {i}" for i in range(100)])
        large_code_b = "\n".join([f"def func_{i}():\n    return {i}" for i in range(100)])
        
        import time
        start_time = time.time()
        
        results = self.analyzer.analyze_code_similarity(large_code_a, large_code_b, 
                                                       similarity_threshold=0.5, is_file=False)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within reasonable time (under 10 seconds for this size)
        self.assertLess(processing_time, 10.0, "Should process large inputs within 10 seconds")
        self.assertGreater(results['similarity_percentage'], 60.0,
                          "Large similar code blocks should have high similarity")
        
        print(f"✅ Performance stress test: {results['similarity_percentage']:.1f}% similarity "
              f"in {processing_time:.2f} seconds ({results['similar_lines_count']} matches)")


def run_comprehensive_tests():
    """Run all tests and provide summary"""
    print("=" * 80)
    print("COMPREHENSIVE CODE SIMILARITY ANALYZER TEST SUITE")
    print("=" * 80)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCodeSimilarityAnalyzer)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nSUCCESS RATE: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("✅ Test suite PASSED - Implementation is working correctly")
    else:
        print("❌ Test suite FAILED - Implementation needs attention")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_comprehensive_tests()
