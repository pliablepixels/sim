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
/**
 * A focused code similarity analyzer for detecting similar code within the same programming language.
 * Optimized for accuracy in plagiarism detection and identifying code modifications.
 *
 * This TypeScript implementation mirrors the Python version exactly.
 */
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
     * Normalize a line of code for comparison (mirrors Python version exactly)
     */
    normalizeLine(line) {
        // Remove common comment patterns
        line = line.replace(/\/\/.*$|#.*$|\/\*.*?\*\/|<!--.*?-->/g, '');
        // Normalize whitespace
        line = line.replace(/\s+/g, ' ').trim();
        // Convert to lowercase for comparison
        line = line.toLowerCase();
        return line;
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
     * Calculate sequence similarity similar to Python's difflib.SequenceMatcher
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
     * Calculate string similarity using approach similar to Python's difflib
     */
    calculateStringSimilarity(strA, strB) {
        const len1 = strA.length;
        const len2 = strB.length;
        if (len1 === 0 && len2 === 0)
            return 1.0;
        if (len1 === 0 || len2 === 0)
            return 0.0;
        // Simple longest common subsequence approach
        const dp = Array(len1 + 1).fill(null).map(() => Array(len2 + 1).fill(0));
        for (let i = 1; i <= len1; i++) {
            for (let j = 1; j <= len2; j++) {
                if (strA[i - 1] === strB[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                }
                else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        const lcs = dp[len1][len2];
        return (2 * lcs) / (len1 + len2);
    }
    /**
     * Calculate similarity between two lines of the same programming language (exact Python mirror)
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
        // Skip very short lines (likely generic syntax)
        if (normA.length <= 2 || normB.length <= 2) {
            return normA === normB ? 1.0 : 0.0;
        }
        // Heavily penalize generic single-character or common syntax lines
        const genericPatterns = new Set(['{', '}', '(', ')', '[', ']', ';', ':', ',']);
        if (genericPatterns.has(normA.trim()) || genericPatterns.has(normB.trim())) {
            return normA === normB ? 1.0 : 0.0;
        }
        // Get tokens and features
        const tokensA = this.tokenizeLine(lineA);
        const tokensB = this.tokenizeLine(lineB);
        const featuresA = this.extractStructuralFeatures(lineA);
        const featuresB = this.extractStructuralFeatures(lineB);
        if (tokensA.length === 0 || tokensB.length === 0) {
            return 0.0;
        }
        // Calculate different similarity metrics
        // 1. Token-based Jaccard similarity
        const setA = new Set(tokensA);
        const setB = new Set(tokensB);
        const intersection = new Set([...setA].filter(x => setB.has(x)));
        const union = new Set([...setA, ...setB]);
        const jaccard = union.size > 0 ? intersection.size / union.size : 0.0;
        // 2. Sequence similarity (order matters for code)
        const sequenceSimilarity = this.calculateSequenceSimilarity(tokensA, tokensB);
        // 3. Structural pattern similarity
        const featureIntersection = new Set([...featuresA].filter(x => featuresB.has(x)));
        const featureUnion = new Set([...featuresA, ...featuresB]);
        const structuralSimilarity = featureUnion.size > 0 ? featureIntersection.size / featureUnion.size : 0.0;
        // 4. Literal string similarity (for variable name changes detection)
        const stringSimilarity = this.calculateStringSimilarity(normA, normB);
        // 5. Enhanced structural similarity for plagiarism detection
        // Count shared patterns even if variable names differ
        let enhancedStructural = 0.0;
        if (featuresA.size > 0 && featuresB.size > 0) {
            // Higher weight if lines have similar structural patterns
            const patternOverlap = featureIntersection.size / Math.max(featuresA.size, featuresB.size);
            if (patternOverlap > 0.5) { // Strong structural similarity
                enhancedStructural = patternOverlap;
            }
        }
        // Require minimum meaningful overlap for any similarity
        if (jaccard < 0.1 && sequenceSimilarity < 0.2 && stringSimilarity < 0.3) {
            return 0.0;
        }
        // Adaptive weighted combination based on the type of similarity detected
        let similarity;
        if (stringSimilarity > 0.7) { // High string similarity (likely variable name changes)
            // Emphasize string and structural similarity for plagiarism detection
            similarity = (0.40 * stringSimilarity + // High weight for similar structure
                0.25 * sequenceSimilarity + // Code structure and order
                0.20 * enhancedStructural + // Enhanced structural patterns
                0.15 * jaccard // Token overlap
            );
        }
        else { // Different implementations or unrelated code
            // More balanced approach
            similarity = (0.35 * sequenceSimilarity + // Code structure and order
                0.30 * stringSimilarity + // Overall similarity
                0.20 * jaccard + // Token overlap
                0.15 * structuralSimilarity // Basic structural patterns
            );
        }
        return Math.max(0.0, similarity);
    }
    /**
     * Check if a line is too trivial to be meaningful for comparison
     */
    isTrivialLine(normalizedLine) {
        const trivialPatterns = new Set([
            // Common single characters or simple syntax
            '{', '}', '(', ')', '[', ']', ';', ':', ',',
            // Common single words that appear everywhere
            'else', 'end', 'pass', 'break', 'continue'
        ]);
        const line = normalizedLine.trim();
        if (trivialPatterns.has(line)) {
            return true;
        }
        // Lines with only punctuation or very short
        if (line.length <= 2 || /^\s*$/.test(line)) {
            return true;
        }
        // Lines that are just imports/includes without specific content
        if (/^(import|include|using|from)\s*$/.test(line)) {
            return true;
        }
        return false;
    }
    /**
     * Read and preprocess a file, extracting meaningful code lines
     */
    preprocessFile(filepath) {
        try {
            const content = fs.readFileSync(filepath, 'utf-8');
            const lines = content.split('\n');
            // Filter for meaningful code lines
            const meaningfulLines = [];
            for (const line of lines) {
                const normalized = this.normalizeLine(line);
                // Keep lines that have substantial content and are not trivial
                if (normalized && normalized.length > 3 && !this.isTrivialLine(normalized)) {
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
     * Find similar lines between two sets of lines using optimal matching (exact Python mirror)
     */
    findSimilarLines(linesA, linesB, threshold = 0.7) {
        // Calculate similarity matrix
        const similarityMatrix = [];
        for (let i = 0; i < linesA.length; i++) {
            const row = [];
            for (let j = 0; j < linesB.length; j++) {
                const similarity = this.calculateLineSimilarity(linesA[i], linesB[j]);
                row.push(similarity >= threshold ? similarity : 0.0);
            }
            similarityMatrix.push(row);
        }
        // Find optimal one-to-one matching using greedy approach
        const similarMatches = [];
        const usedBIndices = new Set();
        // Create list of all potential matches above threshold
        const potentialMatches = [];
        for (let i = 0; i < linesA.length; i++) {
            for (let j = 0; j < linesB.length; j++) {
                if (similarityMatrix[i][j] >= threshold) {
                    potentialMatches.push({ i, j, score: similarityMatrix[i][j] });
                }
            }
        }
        // Sort by similarity score (descending) to prioritize best matches
        potentialMatches.sort((a, b) => b.score - a.score);
        // Greedily select non-conflicting matches
        const usedAIndices = new Set();
        for (const { i, j, score } of potentialMatches) {
            if (!usedAIndices.has(i) && !usedBIndices.has(j)) {
                similarMatches.push({
                    lineAIndex: i,
                    lineBIndex: j,
                    score: score
                });
                usedAIndices.add(i);
                usedBIndices.add(j);
            }
        }
        return similarMatches;
    }
    /**
     * Provide interpretation of similarity results
     */
    interpretSimilarity(percentage, avgScore) {
        if (percentage >= 90) {
            return "Very High Similarity - Likely identical or minimal changes";
        }
        else if (percentage >= 70) {
            return "High Similarity - Possible plagiarism or close modification";
        }
        else if (percentage >= 40) {
            return "Moderate Similarity - Some common patterns or logic";
        }
        else if (percentage >= 20) {
            return "Low Similarity - Limited common elements";
        }
        else {
            return "Very Low Similarity - Largely different code";
        }
    }
    /**
     * Analyze similarity between two code files (exact Python mirror)
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
                similarityPercentage: 0.0,
                averageSimilarityScore: 0.0,
                similarityThreshold,
                similarMatches: [],
                similarityDistribution: {},
                interpretation: "Very Low Similarity - Largely different code",
                error: 'One or both files could not be read or contain no meaningful code'
            };
        }
        // Find similar lines
        const similarMatches = this.findSimilarLines(linesA, linesB, similarityThreshold);
        // Calculate statistics with improved similarity percentage (exact Python logic)
        const totalLinesA = linesA.length;
        const totalLinesB = linesB.length;
        const similarLinesCount = similarMatches.length;
        let similarityPercentage;
        // Calculate weighted similarity percentage based on match quality
        if (similarMatches.length > 0) {
            // For plagiarism detection, consider both quantity and quality of matches
            // Weight matches by their similarity scores
            const totalScore = similarMatches.reduce((sum, match) => sum + match.score, 0);
            // Calculate coverage for both files  
            const coverageA = (similarLinesCount / totalLinesA) * 100;
            const coverageB = (similarLinesCount / totalLinesB) * 100;
            // Calculate average match quality
            const avgQuality = totalScore / similarLinesCount;
            // Check characteristics to distinguish plagiarism from structural modifications
            const highCoverage = Math.min(coverageA, coverageB) > 75; // Both files well covered
            const highQuality = avgQuality > 0.7;
            const similarSize = Math.abs(totalLinesA - totalLinesB) / Math.max(totalLinesA, totalLinesB) < 0.25;
            // More nuanced similarity calculation
            if (highCoverage && highQuality && similarSize) {
                // Likely variable name changes (plagiarism) - boost similarity
                const baseSimilarity = Math.max(coverageA, coverageB);
                similarityPercentage = Math.min(100.0, baseSimilarity * avgQuality * 1.1);
            }
            else if (avgQuality > 0.6) {
                // Moderate quality matches - balanced approach
                const avgCoverage = (coverageA + coverageB) / 2;
                similarityPercentage = avgCoverage * avgQuality * 1.05;
            }
            else {
                // Lower quality or structural changes - more conservative
                const avgCoverage = (coverageA + coverageB) / 2;
                similarityPercentage = avgCoverage * avgQuality;
            }
        }
        else {
            similarityPercentage = 0.0;
        }
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
            similarMatches,
            similarityDistribution,
            interpretation: this.interpretSimilarity(similarityPercentage, avgSimilarity)
        };
        return results;
    }
    /**
     * Print a focused similarity analysis report
     */
    printDetailedReport(results) {
        if (results.error) {
            console.log(`Error: ${results.error}`);
            return;
        }
        console.log('='.repeat(80));
        console.log('SAME-LANGUAGE CODE SIMILARITY ANALYSIS');
        console.log('='.repeat(80));
        console.log(`File A: ${results.fileA}`);
        console.log(`File B: ${results.fileB}`);
        console.log(`Threshold: ${results.similarityThreshold}`);
        console.log('-'.repeat(80));
        console.log(`Meaningful Lines A: ${results.linesACount}`);
        console.log(`Meaningful Lines B: ${results.linesBCount}`);
        console.log(`Matching Lines: ${results.similarLinesCount}`);
        console.log(`Similarity: ${results.similarityPercentage}%`);
        console.log(`Average Match Quality: ${results.averageSimilarityScore.toFixed(3)}`);
        console.log(`Interpretation: ${results.interpretation}`);
        console.log('-'.repeat(80));
        if (results.similarMatches && results.similarMatches.length > 0) {
            console.log(`\nTop ${Math.min(10, results.similarMatches.length)} Similar Line Matches:`);
            for (let i = 0; i < Math.min(10, results.similarMatches.length); i++) {
                const match = results.similarMatches[i];
                console.log(`  ${i + 1}. Line ${match.lineAIndex + 1} -> Line ${match.lineBIndex + 1}: ${match.score.toFixed(3)}`);
            }
        }
        console.log('='.repeat(80));
    }
}
exports.CodeSimilarityAnalyzer = CodeSimilarityAnalyzer;
//# sourceMappingURL=CodeSimilarityAnalyzer.js.map