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
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const readline = __importStar(require("readline"));
const CodeSimilarityAnalyzer_1 = require("./CodeSimilarityAnalyzer");
// Create readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
function question(prompt) {
    return new Promise((resolve) => {
        rl.question(prompt, resolve);
    });
}
async function demoComparison() {
    console.log('=== CODE SIMILARITY ANALYZER DEMO ===');
    const analyzer = new CodeSimilarityAnalyzer_1.CodeSimilarityAnalyzer();
    // Define paths to our sample files
    const currentDir = process.cwd();
    const fileA = path.join(currentDir, 'src', 'samples', 'sample_a.ts');
    const fileB = path.join(currentDir, 'src', 'samples', 'sample_c.ts');
    console.log(`Comparing:\n  File A: ${fileA}\n  File B: ${fileB}\n`);
    // Test with different similarity thresholds
    const thresholds = [0.5, 0.7, 0.9];
    for (const threshold of thresholds) {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`ANALYSIS WITH THRESHOLD: ${threshold}`);
        console.log(`${'='.repeat(60)}`);
        const results = analyzer.analyzeCodeSimilarity(fileA, fileB, threshold);
        analyzer.printDetailedReport(results);
        // Show some example line comparisons
        if (results.similarMatches.length > 0) {
            console.log('\nDetailed Line Comparisons:');
            console.log('-'.repeat(40));
            const linesA = fs.readFileSync(fileA, 'utf-8').split('\n');
            const linesB = fs.readFileSync(fileB, 'utf-8').split('\n');
            // Show first 3 matches in detail
            for (let i = 0; i < Math.min(3, results.similarMatches.length); i++) {
                const match = results.similarMatches[i];
                console.log(`\nMatch ${i + 1} (Score: ${match.score.toFixed(3)}):`);
                console.log(`  A[${match.lineAIndex + 1}]: ${linesA[match.lineAIndex]?.trim()}`);
                console.log(`  B[${match.lineBIndex + 1}]: ${linesB[match.lineBIndex]?.trim()}`);
            }
        }
    }
}
async function interactiveMode() {
    const analyzer = new CodeSimilarityAnalyzer_1.CodeSimilarityAnalyzer();
    console.log('\n=== INTERACTIVE MODE ===');
    console.log('Enter the paths to two files you want to compare:');
    const fileA = await question('Path to file A: ');
    const fileB = await question('Path to file B: ');
    if (!fs.existsSync(fileA.trim())) {
        console.log(`Error: File A '${fileA}' does not exist!`);
        return;
    }
    if (!fs.existsSync(fileB.trim())) {
        console.log(`Error: File B '${fileB}' does not exist!`);
        return;
    }
    const thresholdInput = await question('Similarity threshold (0.0-1.0, default 0.7): ');
    const threshold = thresholdInput.trim() ? parseFloat(thresholdInput.trim()) : 0.7;
    console.log(`\nAnalyzing files with threshold ${threshold}...`);
    const results = analyzer.analyzeCodeSimilarity(fileA.trim(), fileB.trim(), threshold);
    analyzer.printDetailedReport(results);
}
async function main() {
    console.log('Code Similarity Analyzer');
    console.log('1. Run demo with sample files');
    console.log('2. Interactive mode - compare your own files');
    const choice = await question('\nChoose an option (1 or 2): ');
    if (choice.trim() === '1') {
        await demoComparison();
    }
    else if (choice.trim() === '2') {
        await interactiveMode();
    }
    else {
        console.log('Invalid choice. Running demo by default.');
        await demoComparison();
    }
    rl.close();
}
// Main execution
main().catch(console.error);
//# sourceMappingURL=demo.js.map