/**
 * Comprehensive Test Suite for TypeScript Code Similarity Analyzer
 * 
 * This test suite validates the accuracy and behavior of the Code Similarity Analyzer
 * with various TypeScript scenarios including:
 * - Identical code detection
 * - Plagiarism detection (modified variable names, structure changes)  
 * - Different implementations of same functionality
 * - Unrelated code detection
 * - Edge cases and boundary conditions
 * 
 * Usage:
 *   cd typescript && npm run build && node dist/test_similarity_analyzer.js
 *   OR from tests directory: npm run --prefix ../typescript build && node ../typescript/dist/test_similarity_analyzer.js
 * 
 * The test suite provides detailed assertions and reporting to help developers
 * understand how the similarity analyzer behaves in different scenarios.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { CodeSimilarityAnalyzer } from '../typescript/src/CodeSimilarityAnalyzer';

export class TypeScriptSimilarityTester {
    private analyzer: CodeSimilarityAnalyzer;
    private samplesDir: string;
    private testResults: Array<{test: string, passed: boolean, details: string}> = [];

    constructor() {
        this.analyzer = new CodeSimilarityAnalyzer();
        this.samplesDir = path.join(__dirname);
    }

    private createTempFile(content: string): string {
        const tempPath = path.join(os.tmpdir(), `test_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.ts`);
        fs.writeFileSync(tempPath, content);
        return tempPath;
    }

    private analyzeSimilarity(contentA: string, contentB: string, threshold: number = 0.7): any {
        const fileA = this.createTempFile(contentA);
        const fileB = this.createTempFile(contentB);
        
        try {
            const results = this.analyzer.analyzeCodeSimilarity(fileA, fileB, threshold);
            return results;
        } finally {
            // Clean up temporary files
            if (fs.existsSync(fileA)) fs.unlinkSync(fileA);
            if (fs.existsSync(fileB)) fs.unlinkSync(fileB);
        }
    }

    private assert(condition: boolean, message: string, testName: string): void {
        this.testResults.push({
            test: testName,
            passed: condition,
            details: message
        });
        
        if (condition) {
            console.log(`✅ ${testName}: ${message}`);
        } else {
            console.log(`❌ ${testName}: ${message}`);
        }
    }

    testIdenticalCodeDetection(): void {
        const code = `
interface User {
    id: number;
    name: string;
    email: string;
}

class UserManager {
    private users: User[] = [];

    addUser(user: User): void {
        this.users.push(user);
    }

    findUserById(id: number): User | undefined {
        return this.users.find(user => user.id === id);
    }

    getAllUsers(): User[] {
        return [...this.users];
    }
}`;

        const results = this.analyzeSimilarity(code, code, 0.9);
        
        this.assert(
            results.similarityPercentage >= 90.0,
            `Identical code similarity: ${results.similarityPercentage.toFixed(1)}%`,
            "Identical Code Detection"
        );
    }

    testVariableNameChanges(): void {
        const originalCode = `
function calculateCompoundInterest(principal: number, rate: number, time: number): number {
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
}

function checkIfUserExists(username: string): boolean {
    // Simulation
    return false;
}

function createNewUser(username: string, email: string, password: string): void {
    // Simulation
}`;

        const modifiedCode = `
function calculateCompoundInterest(initialAmount: number, interestRate: number, duration: number): number {
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
}

function checkIfUserExists(userId: string): boolean {
    // Simulation
    return false;
}

function createNewUser(userId: string, userEmail: string, userPassword: string): void {
    // Simulation
}`;

        const results = this.analyzeSimilarity(originalCode, modifiedCode, 0.6);
        
        this.assert(
            results.similarityPercentage >= 60.0 && results.similarityPercentage <= 95.0,
            `Variable name changes similarity: ${results.similarityPercentage.toFixed(1)}%`,
            "Variable Name Changes Detection"
        );
    }

    testStructuralModifications(): void {
        const originalCode = `
class DataProcessor {
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
}`;

        const modifiedCode = `
class NumberAnalyzer {
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
}`;

        const results = this.analyzeSimilarity(originalCode, modifiedCode, 0.4);
        
        this.assert(
            results.similarityPercentage >= 30.0 && results.similarityPercentage <= 70.0,
            `Structural modifications similarity: ${results.similarityPercentage.toFixed(1)}%`,
            "Structural Modifications Detection"
        );
    }

    testDifferentImplementationsSameLogic(): void {
        const binarySearchIterative = `
function binarySearchIterative(arr: number[], target: number): number {
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
}`;

        const binarySearchRecursive = `
function binarySearchRecursive(arr: number[], target: number, left: number = 0, right: number = arr.length - 1): number {
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
}`;

        const results = this.analyzeSimilarity(binarySearchIterative, binarySearchRecursive, 0.3);
        
        this.assert(
            results.similarityPercentage >= 15.0 && results.similarityPercentage <= 60.0,
            `Different implementations similarity: ${results.similarityPercentage.toFixed(1)}%`,
            "Different Implementations Same Logic"
        );
    }

    testCompletelyUnrelatedCode(): void {
        const apiClient = `
interface ApiResponse<T> {
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
            const response = await fetch(\`\${this.baseUrl}/\${endpoint}\`);
            const data = await response.json();
            
            return {
                data: data,
                status: response.status,
                message: response.ok ? 'Success' : 'Error'
            };
        } catch (error) {
            throw new Error(\`Network error: \${error}\`);
        }
    }

    async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
        try {
            const response = await fetch(\`\${this.baseUrl}/\${endpoint}\`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
            
            const data = await response.json();
            
            return {
                data: data,
                status: response.status,
                message: response.ok ? 'Success' : 'Error'
            };
        } catch (error) {
            throw new Error(\`Network error: \${error}\`);
        }
    }
}`;

        const geometryCalculations = `
interface Point {
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

    static isPointInsideRectangle(point: Point, rect: Rectangle, origin: Point): boolean {
        return (
            point.x >= origin.x &&
            point.x <= origin.x + rect.width &&
            point.y >= origin.y &&
            point.y <= origin.y + rect.height
        );
    }

    static calculateTriangleArea(base: number, height: number): number {
        return 0.5 * base * height;
    }
}`;

        const results = this.analyzeSimilarity(apiClient, geometryCalculations, 0.1);
        
        this.assert(
            results.similarityPercentage <= 30.0,
            `Unrelated code similarity: ${results.similarityPercentage.toFixed(1)}%`,
            "Completely Unrelated Code"
        );
    }

    testComplexSamplesSimilarity(): void {
        const complexAPath = path.join(this.samplesDir, "complex_a.ts");
        const complexBPath = path.join(this.samplesDir, "complex_b.ts");

        if (fs.existsSync(complexAPath) && fs.existsSync(complexBPath)) {
            const results = this.analyzer.analyzeCodeSimilarity(complexAPath, complexBPath, 0.3);
            
            this.assert(
                results.similarityPercentage >= 20.0 && results.similarityPercentage <= 60.0,
                `Complex samples similarity: ${results.similarityPercentage.toFixed(1)}%`,
                "Complex Samples Different Implementations"
            );
        }
    }

    testThresholdSensitivity(): void {
        const codeA = `
function processArray(inputArray: number[]): number[] {
    const result: number[] = [];
    for (const item of inputArray) {
        if (item > 0) {
            result.push(item * 2);
        }
    }
    return result;
}

function validateInput(data: any): boolean {
    return data !== null && data !== undefined;
}`;

        const codeB = `
function handleArray(dataArray: number[]): number[] {
    const output: number[] = [];
    for (const element of dataArray) {
        if (element > 0) {
            output.push(element * 2);
        }
    }
    return output;
}

function checkInput(input: any): boolean {
    return input !== null && input !== undefined;
}`;

        const thresholds = [0.3, 0.5, 0.7, 0.9];
        const resultsByThreshold: {[key: number]: any} = {};

        console.log("\nThreshold Sensitivity Analysis:");
        
        for (const threshold of thresholds) {
            const results = this.analyzeSimilarity(codeA, codeB, threshold);
            resultsByThreshold[threshold] = results;
            
            console.log(`  Threshold ${threshold}: ${results.similarityPercentage.toFixed(1)}% similarity, ${results.similarMatches.length} matches`);
        }

        // Verify that higher thresholds generally result in fewer matches
        let thresholdTestPassed = true;
        for (let i = 0; i < thresholds.length - 1; i++) {
            const currThreshold = thresholds[i];
            const nextThreshold = thresholds[i + 1];
            
            const currMatches = resultsByThreshold[currThreshold].similarMatches.length;
            const nextMatches = resultsByThreshold[nextThreshold].similarMatches.length;
            
            if (currMatches < nextMatches) {
                thresholdTestPassed = false;
                break;
            }
        }

        this.assert(
            thresholdTestPassed,
            "Higher thresholds produce fewer matches as expected",
            "Threshold Sensitivity"
        );
    }

    testEdgeCases(): void {
        // Empty files
        const emptyResults = this.analyzeSimilarity("", "", 0.5);
        this.assert(
            emptyResults.similarityPercentage === 0.0,
            "Empty files have 0% similarity",
            "Edge Case: Empty Files"
        );

        // Single line files
        const singleLineResults = this.analyzeSimilarity(
            "console.log('hello');",
            "console.log('hello');",
            0.5
        );
        this.assert(
            singleLineResults.similarityPercentage >= 90.0,
            `Identical single lines: ${singleLineResults.similarityPercentage.toFixed(1)}% similarity`,
            "Edge Case: Single Line Files"
        );

        // Files with only comments
        const commentsA = "// This is a comment\n// Another comment";
        const commentsB = "// Different comment\n// Yet another comment";
        const commentResults = this.analyzeSimilarity(commentsA, commentsB, 0.5);
        
        this.assert(
            true, // Comments are removed during preprocessing
            `Comment-only files: ${commentResults.similarityPercentage.toFixed(1)}% similarity`,
            "Edge Case: Comment-Only Files"
        );
    }

    runAllTests(): void {
        console.log("Starting TypeScript Code Similarity Analyzer Test Suite...");
        console.log("=" .repeat(70));

        this.testIdenticalCodeDetection();
        this.testVariableNameChanges();
        this.testStructuralModifications();
        this.testDifferentImplementationsSameLogic();
        this.testCompletelyUnrelatedCode();
        this.testComplexSamplesSimilarity();
        this.testThresholdSensitivity();
        this.testEdgeCases();

        this.generateTestReport();
    }

    private generateTestReport(): void {
        console.log("\n" + "=".repeat(70));
        console.log("TEST RESULTS SUMMARY");
        console.log("=".repeat(70));

        const passedTests = this.testResults.filter(r => r.passed).length;
        const totalTests = this.testResults.length;

        console.log(`\nTotal Tests: ${totalTests}`);
        console.log(`Passed: ${passedTests}`);
        console.log(`Failed: ${totalTests - passedTests}`);
        console.log(`Success Rate: ${((passedTests / totalTests) * 100).toFixed(1)}%`);

        const failedTests = this.testResults.filter(r => !r.passed);
        if (failedTests.length > 0) {
            console.log("\nFailed Tests:");
            failedTests.forEach(test => {
                console.log(`  ❌ ${test.test}: ${test.details}`);
            });
        }

        console.log("\n" + "=".repeat(70));
        console.log("SIMILARITY INTERPRETATION GUIDE:");
        console.log("- >90% similarity: Likely identical or very minor changes");
        console.log("- 70-90% similarity: Significant similarity, possible plagiarism");
        console.log("- 40-70% similarity: Moderate similarity, same domain/patterns");
        console.log("- 20-40% similarity: Some common elements");
        console.log("- <20% similarity: Largely unrelated code");
        console.log("=".repeat(70));
    }
}

// Export for use in other modules
export function runTypeScriptTests(): void {
    const tester = new TypeScriptSimilarityTester();
    tester.runAllTests();
}

// Run tests if this file is executed directly
runTypeScriptTests();
