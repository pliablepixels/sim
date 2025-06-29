#!/usr/bin/env python3
"""
Final comparison script to verify Python and TypeScript implementations 
behave consistently across all test scenarios
"""

import sys
import os
import tempfile
import subprocess
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

import importlib.util
spec = importlib.util.spec_from_file_location("analyzer_module", os.path.join(os.path.dirname(__file__), 'python', 'try.py'))
analyzer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer_module)

def test_both_implementations():
    """Compare Python and TypeScript implementations on identical test cases"""
    
    analyzer = analyzer_module.CodeSimilarityAnalyzer()
    
    print("=== FINAL IMPLEMENTATION COMPARISON ===")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Variable Name Changes",
            "threshold": 0.6,
            "code_a": '''function calculateCompoundInterest(principal: number, rate: number, time: number): number {
    const amount = principal * Math.pow(1 + rate, time);
    const interest = amount - principal;
    return interest;
}

function processUserRegistration(username: string, email: string, password: string): boolean {
    const userExists = checkIfUserExists(username);
    if (!userExists) {
        createNewUser(username, email, password);
        return true;
    }
    return false;
}''',
            "code_b": '''function calculateCompoundInterest(initialAmount: number, interestRate: number, duration: number): number {
    const finalAmount = initialAmount * Math.pow(1 + interestRate, duration);
    const earnedInterest = finalAmount - initialAmount;
    return earnedInterest;
}

function processUserRegistration(userId: string, userEmail: string, userPassword: string): boolean {
    const exists = checkIfUserExists(userId);
    if (!exists) {
        createNewUser(userId, userEmail, userPassword);
        return true;
    }
    return false;
}'''
        },
        {
            "name": "Structural Modifications",
            "threshold": 0.4,
            "code_a": '''class DataProcessor {
    private data: number[] = [];

    addData(value: number): void {
        this.data.push(value);
    }

    calculateAverage(): number {
        if (this.data.length === 0) return 0;
        const sum = this.data.reduce((acc, val) => acc + val, 0);
        return sum / this.data.length;
    }

    getMaxValue(): number {
        return Math.max(...this.data);
    }

    getMinValue(): number {
        return Math.min(...this.data);
    }
}''',
            "code_b": '''class NumberAnalyzer {
    private numbers: number[] = [];

    insertNumber(num: number): void {
        this.numbers.push(num);
    }

    computeMean(): number {
        if (this.numbers.length === 0) return 0;
        const total = this.numbers.reduce((sum, current) => sum + current, 0);
        return total / this.numbers.length;
    }

    findMaximum(): number {
        return Math.max(...this.numbers);
    }

    findMinimum(): number {
        return Math.min(...this.numbers);
    }

    getCount(): number {
        return this.numbers.length;
    }
}'''
        },
        {
            "name": "Different Implementations",
            "threshold": 0.3,
            "code_a": '''function binarySearchIterative(arr: number[], target: number): number {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        
        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}

function sortArray(numbers: number[]): number[] {
    return numbers.sort((a, b) => a - b);
}''',
            "code_b": '''function binarySearchRecursive(arr: number[], target: number, left: number = 0, right: number = arr.length - 1): number {
    if (left > right) {
        return -1;
    }
    
    const mid = Math.floor((left + right) / 2);
    
    if (arr[mid] === target) {
        return mid;
    } else if (arr[mid] < target) {
        return binarySearchRecursive(arr, target, mid + 1, right);
    } else {
        return binarySearchRecursive(arr, target, left, mid - 1);
    }
}

function arrangeNumbers(data: number[]): number[] {
    return data.slice().sort((x, y) => x - y);
}'''
        },
        {
            "name": "Unrelated Code",
            "threshold": 0.1,
            "code_a": '''interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

class HttpClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async get<T>(endpoint: string): Promise<ApiResponse<T>> {
        try {
            const response = await fetch(`${this.baseUrl}/${endpoint}`);
            const data = await response.json();
            
            return {
                data: data,
                status: response.status,
                message: response.ok ? 'Success' : 'Error'
            };
        } catch (error) {
            throw new Error(`Network error: ${error}`);
        }
    }
}''',
            "code_b": '''interface Point {
    x: number;
    y: number;
}

interface Rectangle {
    width: number;
    height: number;
}

class GeometryCalculator {
    static calculateDistance(point1: Point, point2: Point): number {
        const dx = point2.x - point1.x;
        const dy = point2.y - point1.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    static calculateRectangleArea(rectangle: Rectangle): number {
        return rectangle.width * rectangle.height;
    }

    static calculateRectanglePerimeter(rectangle: Rectangle): number {
        return 2 * (rectangle.width + rectangle.height);
    }
}'''
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 40)
        
        # Test Python implementation
        file_a = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        file_b = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        
        try:
            file_a.write(test_case['code_a'])
            file_a.close()
            file_b.write(test_case['code_b'])
            file_b.close()
            
            python_results = analyzer.analyze_code_similarity(file_a.name, file_b.name, test_case['threshold'])
            python_similarity = python_results['similarity_percentage']
            
        finally:
            os.unlink(file_a.name)
            os.unlink(file_b.name)
        
        # Test TypeScript implementation
        file_a_ts = tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False)
        file_b_ts = tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False)
        
        try:
            file_a_ts.write(test_case['code_a'])
            file_a_ts.close()
            file_b_ts.write(test_case['code_b'])
            file_b_ts.close()
            
            # Run TypeScript test
            test_script = f'''
const {{ CodeSimilarityAnalyzer }} = require('./dist/CodeSimilarityAnalyzer');
const analyzer = new CodeSimilarityAnalyzer();
const results = analyzer.analyzeCodeSimilarity('{file_a_ts.name}', '{file_b_ts.name}', {test_case['threshold']});
console.log(JSON.stringify({{ similarity: results.similarityPercentage }}));
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as script_file:
                script_file.write(test_script)
                script_file.close()
                
                try:
                    result = subprocess.run(['node', script_file.name], 
                                          cwd=os.path.join(os.path.dirname(__file__), 'typescript'), 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    
                    if result.returncode == 0:
                        ts_output = json.loads(result.stdout.strip())
                        typescript_similarity = ts_output['similarity']
                    else:
                        print(f"TypeScript error: {result.stderr}")
                        typescript_similarity = 0.0
                        
                finally:
                    os.unlink(script_file.name)
            
        finally:
            os.unlink(file_a_ts.name)
            os.unlink(file_b_ts.name)
        
        # Compare results
        difference = abs(python_similarity - typescript_similarity)
        
        print(f"Python:     {python_similarity:.1f}%")
        print(f"TypeScript: {typescript_similarity:.1f}%")
        print(f"Difference: {difference:.1f}%")
        
        # Determine if results are reasonably close (within 10%)
        status = "✅ CLOSE" if difference <= 10.0 else "⚠️  DIFFERENT"
        print(f"Status:     {status}")
        
        results.append({
            'test': test_case['name'],
            'python': python_similarity,
            'typescript': typescript_similarity,
            'difference': difference,
            'close': difference <= 10.0
        })
    
    print("\n" + "=" * 60)
    print("FINAL COMPARISON SUMMARY")
    print("=" * 60)
    
    close_count = sum(1 for r in results if r['close'])
    total_tests = len(results)
    
    print(f"Tests with similar results: {close_count}/{total_tests}")
    print(f"Implementation consistency: {(close_count/total_tests)*100:.1f}%")
    
    if close_count == total_tests:
        print("\n🎉 SUCCESS: Both implementations behave consistently!")
    else:
        print(f"\n⚠️  {total_tests - close_count} test(s) show significant differences")
        
        for result in results:
            if not result['close']:
                print(f"   - {result['test']}: {result['difference']:.1f}% difference")
    
    return results

if __name__ == "__main__":
    test_both_implementations()
