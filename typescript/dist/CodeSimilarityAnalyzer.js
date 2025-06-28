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
exports.CodeSimilarityAnalyzer = void 0;
const fs = __importStar(require("fs"));
class CodeSimilarityAnalyzer {
    constructor() {
        this.structuralKeywords = new Set([
            'if', 'else', 'elif', 'for', 'while', 'do', 'switch', 'case',
            'function', 'def', 'class', 'return', 'break', 'continue',
            'try', 'catch', 'finally', 'throw', 'import', 'from'
        ]);
        this.operators = new Set([
            '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
            '&&', '||', '!', '&', '|', '^', '++', '--'
        ]);
    }
    /**
     * Normalize a line of code for same-language comparison
     */
    normalizeLine(line) {
        let normalized = line;
        // Remove common comment patterns
        normalized = normalized.replace(/\/\/.*$|#.*$|\/\*.*?\*\/|<!--.*?-->/g, '');
        // Normalize whitespace
        normalized = normalized.replace(/\s+/g, ' ').trim();
        // Convert to lowercase for comparison
        normalized = normalized.toLowerCase();
        return normalized;
    }
    /**
     * Extract key structural features from a line of code for same-language comparison
     */
    extractStructuralFeatures(line) {
        const features = new Set();
        const normalized = this.normalizeLine(line);
        // Extract keywords that indicate code structure
        const words = normalized.match(/\b\w+\b/g) || [];
        for (const word of words) {
            if (this.structuralKeywords.has(word)) {
                features.add(`keyword:${word}`);
            }
        }
        // Extract operators
        for (const op of this.operators) {
            if (normalized.includes(op)) {
                features.add(`operator:${op}`);
            }
        }
        // Extract specific patterns for same-language detection
        const patterns = {
            function_call: /\b\w+\s*\(.*?\)/,
            assignment: /\b\w+\s*=/,
            indexing: /\[.*?\]/,
            block_or_object: /\{.*?\}/,
            string_literal: /"[^"]*"|'[^']*'/,
            numeric_literal: /\b\d+(\.\d+)?\b/,
        };
        for (const [feature, pattern] of Object.entries(patterns)) {
            if (pattern.test(normalized)) {
                features.add(feature);
            }
        }
        return features;
    }
    /**
     * Tokenize a line into meaningful code tokens
     */
    tokenizeLine(line) {
        const normalized = this.normalizeLine(line);
        // Extract meaningful tokens (identifiers, operators, literals)
        const tokens = normalized.match(/\w+|[^\w\s]/g) || [];
        // Filter meaningful tokens
        const filteredTokens = [];
        for (const token of tokens) {
            // Keep multi-character tokens, important operators, and numbers
            if (token.length > 1 || this.operators.has(token) || /\d/.test(token)) {
                filteredTokens.push(token);
            }
        }
        return filteredTokens;
    }
    /**
     * Calculate similarity between two lines of the same programming language
     */
    calculateLineSimilarity(lineA, lineB) {
        if (!lineA.trim() || !lineB.trim()) {
            return 0.0;
        }
        // Exact match after normalization
        const normA = this.normalizeLine(lineA);
        const normB = this.normalizeLine(lineB);
        if (normA === normB) {
            return 1.0;
        }
        // Token-based similarity
        const tokensA = this.tokenizeLine(lineA);
        const tokensB = this.tokenizeLine(lineB);
        if (tokensA.length === 0 || tokensB.length === 0) {
            return 0.0;
        }
        // Calculate Jaccard similarity for tokens
        const setA = new Set(tokensA);
        const setB = new Set(tokensB);
        const intersection = new Set([...setA].filter(x => setB.has(x)));
        const union = new Set([...setA, ...setB]);
        const jaccard = union.size > 0 ? intersection.size / union.size : 0.0;
        // Calculate sequence similarity (simple implementation)
        const sequenceSimilarity = this.calculateSequenceSimilarity(tokensA, tokensB);
        // Structural similarity
        const featuresA = this.extractStructuralFeatures(lineA);
        const featuresB = this.extractStructuralFeatures(lineB);
        const featureIntersection = new Set([...featuresA].filter(x => featuresB.has(x)));
        const featureUnion = new Set([...featuresA, ...featuresB]);
        const structuralSimilarity = featureUnion.size > 0 ? featureIntersection.size / featureUnion.size : 0.0;
        // Weighted combination
        const similarity = (0.4 * sequenceSimilarity +
            0.3 * jaccard +
            0.3 * structuralSimilarity);
        return similarity;
    }
    /**
     * Simple sequence similarity calculation (similar to difflib.SequenceMatcher)
     */
    calculateSequenceSimilarity(seqA, seqB) {
        const lenA = seqA.length;
        const lenB = seqB.length;
        if (lenA === 0 && lenB === 0)
            return 1.0;
        if (lenA === 0 || lenB === 0)
            return 0.0;
        // Dynamic programming approach for longest common subsequence
        const dp = Array(lenA + 1).fill(null).map(() => Array(lenB + 1).fill(0));
        for (let i = 1; i <= lenA; i++) {
            for (let j = 1; j <= lenB; j++) {
                if (seqA[i - 1] === seqB[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                }
                else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        const lcs = dp[lenA][lenB];
        return (2 * lcs) / (lenA + lenB);
    }
    /**
     * Read and preprocess a file, returning meaningful lines
     */
    preprocessFile(filepath) {
        try {
            const content = fs.readFileSync(filepath, 'utf-8');
            const lines = content.split('\n');
            // Filter out empty lines and comment-only lines
            const meaningfulLines = [];
            for (const line of lines) {
                const normalized = this.normalizeLine(line);
                if (normalized && normalized.length > 2) { // Ignore very short lines
                    meaningfulLines.push(line.trimEnd());
                }
            }
            return meaningfulLines;
        }
        catch (error) {
            console.error(`Error reading file ${filepath}:`, error);
            return [];
        }
    }
    /**
     * Find similar lines between two sets of lines
     */
    findSimilarLines(linesA, linesB, threshold = 0.7) {
        const similarMatches = [];
        for (let i = 0; i < linesA.length; i++) {
            let bestMatch = { index: -1, score: 0.0 };
            for (let j = 0; j < linesB.length; j++) {
                const similarity = this.calculateLineSimilarity(linesA[i], linesB[j]);
                if (similarity >= threshold && similarity > bestMatch.score) {
                    bestMatch = { index: j, score: similarity };
                }
            }
            if (bestMatch.index !== -1) {
                similarMatches.push({
                    lineAIndex: i,
                    lineBIndex: bestMatch.index,
                    score: bestMatch.score
                });
            }
        }
        return similarMatches;
    }
    /**
     * Analyze similarity between two code files
     */
    analyzeCodeSimilarity(fileA, fileB, similarityThreshold = 0.7) {
        console.log(`Analyzing similarity between ${fileA} and ${fileB}`);
        console.log(`Similarity threshold: ${similarityThreshold}`);
        // Read and preprocess files
        const linesA = this.preprocessFile(fileA);
        const linesB = this.preprocessFile(fileB);
        if (linesA.length === 0 || linesB.length === 0) {
            return {
                fileA,
                fileB,
                linesACount: linesA.length,
                linesBCount: linesB.length,
                similarLinesCount: 0,
                similarityPercentage: 0,
                averageSimilarityScore: 0,
                similarityThreshold,
                similarMatches: [],
                similarityDistribution: {},
                error: 'One or both files could not be read or contain no meaningful code'
            };
        }
        // Find similar lines
        const similarMatches = this.findSimilarLines(linesA, linesB, similarityThreshold);
        // Calculate statistics
        const totalLinesA = linesA.length;
        const totalLinesB = linesB.length;
        const similarLinesCount = similarMatches.length;
        const similarityPercentage = totalLinesA > 0 ? (similarLinesCount / totalLinesA) * 100 : 0;
        // Group matches by similarity score
        const similarityDistribution = {};
        for (const match of similarMatches) {
            const scoreRange = `${Math.floor(match.score * 10) * 10}%-${Math.floor(match.score * 10) * 10 + 9}%`;
            similarityDistribution[scoreRange] = (similarityDistribution[scoreRange] || 0) + 1;
        }
        // Calculate average similarity for matches
        const avgSimilarity = similarMatches.length > 0
            ? similarMatches.reduce((sum, match) => sum + match.score, 0) / similarMatches.length
            : 0.0;
        const results = {
            fileA,
            fileB,
            linesACount: totalLinesA,
            linesBCount: totalLinesB,
            similarLinesCount,
            similarityPercentage: Math.round(similarityPercentage * 100) / 100,
            averageSimilarityScore: Math.round(avgSimilarity * 1000) / 1000,
            similarityThreshold,
            similarMatches: similarMatches.slice(0, 10), // First 10 matches for review
            similarityDistribution
        };
        return results;
    }
    /**
     * Print a detailed similarity analysis report
     */
    printDetailedReport(results) {
        if (results.error) {
            console.log(`Error: ${results.error}`);
            return;
        }
        console.log('='.repeat(80));
        console.log('CODE SIMILARITY ANALYSIS REPORT');
        console.log('='.repeat(80));
        console.log(`File A: ${results.fileA}`);
        console.log(`File B: ${results.fileB}`);
        console.log(`Similarity Threshold: ${results.similarityThreshold}`);
        console.log('-'.repeat(80));
        console.log(`Lines in File A: ${results.linesACount}`);
        console.log(`Lines in File B: ${results.linesBCount}`);
        console.log(`Similar Lines Found: ${results.similarLinesCount}`);
        console.log(`Similarity Percentage: ${results.similarityPercentage}%`);
        console.log(`Average Similarity Score: ${results.averageSimilarityScore}`);
        console.log('-'.repeat(80));
        if (Object.keys(results.similarityDistribution).length > 0) {
            console.log('Similarity Score Distribution:');
            const sortedDistribution = Object.entries(results.similarityDistribution).sort();
            for (const [scoreRange, count] of sortedDistribution) {
                console.log(`  ${scoreRange}: ${count} matches`);
            }
        }
        if (results.similarMatches.length > 0) {
            console.log('\nTop Similar Line Matches (Line A -> Line B, Score):');
            for (const match of results.similarMatches) {
                console.log(`  Line ${match.lineAIndex + 1} -> Line ${match.lineBIndex + 1}: ${match.score.toFixed(3)}`);
            }
        }
        console.log('='.repeat(80));
    }
}
exports.CodeSimilarityAnalyzer = CodeSimilarityAnalyzer;
//# sourceMappingURL=CodeSimilarityAnalyzer.js.map