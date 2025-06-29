"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const CodeSimilarityAnalyzer_1 = require("./CodeSimilarityAnalyzer");
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
// Create a simple test to verify our TypeScript implementation matches Python behavior
const analyzer = new CodeSimilarityAnalyzer_1.CodeSimilarityAnalyzer();
function createTempFile(content) {
    const tempPath = path.join(os.tmpdir(), `test_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.ts`);
    fs.writeFileSync(tempPath, content);
    return tempPath;
}
function testSimilarity(contentA, contentB, threshold, testName) {
    const fileA = createTempFile(contentA);
    const fileB = createTempFile(contentB);
    try {
        const results = analyzer.analyzeCodeSimilarity(fileA, fileB, threshold);
        console.log(`${testName}: ${results.similarityPercentage.toFixed(1)}%`);
    }
    finally {
        // Clean up temporary files
        if (fs.existsSync(fileA))
            fs.unlinkSync(fileA);
        if (fs.existsSync(fileB))
            fs.unlinkSync(fileB);
    }
}
console.log("Testing New TypeScript Implementation:");
console.log("=".repeat(50));
// Test 1: Structural Modifications (should be ~80% like Python, not 100%)
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
testSimilarity(originalCode, modifiedCode, 0.4, "Structural Modifications");
// Test 2: Different Implementations (should be ~77% like Python, not 100%)
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
testSimilarity(binarySearchIterative, binarySearchRecursive, 0.3, "Different Implementations");
// Test 3: Unrelated Code (should be ~19% like Python, not 51%)
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
}`;
testSimilarity(apiClient, geometryCalculations, 0.1, "Unrelated Code");
console.log("=".repeat(50));
console.log("Expected Python results:");
console.log("Structural Modifications: ~83.4%");
console.log("Different Implementations: ~77.7%");
console.log("Unrelated Code: ~19.1%");
//# sourceMappingURL=quick_test.js.map