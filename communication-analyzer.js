/**
 * COMMUNICATION ANALYZER - Pattern Theory Core Engine
 * Detects manipulation patterns, truth signals, and consciousness levels
 * Powers all 37 consciousness tools
 */

const CommunicationAnalyzer = {

  // Pattern Theory: 15-degree manipulation indicators
  manipulationPatterns: {
    gaslighting: ['you never', 'you always', 'that didn\'t happen', 'you\'re crazy', 'you\'re too sensitive', 'i never said that'],
    loveBombing: ['you\'re the only one', 'no one understands me like you', 'we\'re soulmates', 'i\'ve never felt this way'],
    futureFaking: ['soon', 'when things settle', 'next month', 'i promise', 'trust me', 'just wait'],
    guilTripping: ['after all i\'ve done', 'you owe me', 'how could you', 'i sacrificed'],
    stonewalling: ['whatever', 'i don\'t care', 'fine', 'do what you want'],
    deflection: ['what about when you', 'you do it too', 'that\'s not the point'],
    triangulation: ['everyone thinks', 'they all said', 'even your friends agree'],
    victimPlaying: ['i\'m always the bad guy', 'nothing i do is right', 'you never appreciate'],
    wordSalad: [], // Detected by incoherence score
    silentTreatment: [] // Detected by response patterns
  },

  // Truth Algorithm indicators
  truthSignals: {
    accountability: ['i was wrong', 'i apologize', 'my mistake', 'i should have', 'i take responsibility'],
    clarity: ['specifically', 'for example', 'to be clear', 'what i mean is'],
    consistency: [], // Measured over time
    boundaries: ['i need', 'i feel', 'i won\'t', 'that doesn\'t work for me'],
    directness: ['yes', 'no', 'i don\'t know', 'let me think about it']
  },

  // Consciousness level thresholds
  consciousnessLevels: {
    critical: { min: 0, max: 20, label: 'Critical - High Manipulation' },
    low: { min: 21, max: 40, label: 'Low - Significant Patterns' },
    developing: { min: 41, max: 60, label: 'Developing - Mixed Signals' },
    elevated: { min: 61, max: 80, label: 'Elevated - Mostly Truth' },
    mastery: { min: 81, max: 100, label: 'Mastery - Truth Algorithm Active' }
  },

  /**
   * Main analysis function
   * @param {string} text - Input text to analyze
   * @param {object} context - Optional context (history, relationship type)
   * @returns {object} Analysis results
   */
  analyze(text, context = {}) {
    const normalized = text.toLowerCase();

    // Detect manipulation patterns
    const manipulationResults = this.detectManipulation(normalized);

    // Detect truth signals
    const truthResults = this.detectTruth(normalized);

    // Calculate scores
    const manipulationScore = manipulationResults.totalScore;
    const truthScore = truthResults.totalScore;

    // Calculate consciousness level (truth - manipulation, normalized)
    const rawConsciousness = 50 + (truthScore * 5) - (manipulationScore * 10);
    const consciousnessScore = Math.max(0, Math.min(100, rawConsciousness));

    // Determine algorithm in use
    const algorithm = manipulationScore > truthScore ? 'DECEIT' : 'TRUTH';

    // Get consciousness level label
    const consciousnessLevel = this.getConsciousnessLevel(consciousnessScore);

    // Generate recommended response
    const recommendedResponse = this.generateResponse(manipulationResults, truthResults, algorithm);

    return {
      input: text,
      timestamp: new Date().toISOString(),

      // Core scores
      consciousness_score: consciousnessScore,
      consciousness_level: consciousnessLevel,
      algorithm_detected: algorithm,

      // Pattern detection
      manipulation: {
        score: manipulationScore,
        patterns_found: manipulationResults.patterns,
        confidence: manipulationResults.confidence
      },

      truth: {
        score: truthScore,
        signals_found: truthResults.signals,
        confidence: truthResults.confidence
      },

      // 15-degree turn detection
      fifteen_degree_turns: manipulationResults.patterns.length,

      // Actionable output
      recommended_response: recommendedResponse,

      // Detailed breakdown
      analysis: {
        red_flags: manipulationResults.patterns.map(p => p.type),
        green_flags: truthResults.signals.map(s => s.type),
        primary_concern: manipulationResults.patterns[0]?.type || 'none',
        primary_strength: truthResults.signals[0]?.type || 'none'
      }
    };
  },

  /**
   * Detect manipulation patterns in text
   */
  detectManipulation(text) {
    const patterns = [];
    let totalScore = 0;

    for (const [patternType, phrases] of Object.entries(this.manipulationPatterns)) {
      for (const phrase of phrases) {
        if (text.includes(phrase)) {
          patterns.push({
            type: patternType,
            phrase: phrase,
            severity: this.getSeverity(patternType)
          });
          totalScore += this.getSeverity(patternType);
        }
      }
    }

    // Check for word salad (incoherence)
    const incoherence = this.detectIncoherence(text);
    if (incoherence > 0.6) {
      patterns.push({ type: 'wordSalad', phrase: 'high incoherence', severity: 3 });
      totalScore += 3;
    }

    return {
      patterns,
      totalScore,
      confidence: patterns.length > 0 ? Math.min(0.95, 0.5 + (patterns.length * 0.15)) : 0
    };
  },

  /**
   * Detect truth signals in text
   */
  detectTruth(text) {
    const signals = [];
    let totalScore = 0;

    for (const [signalType, phrases] of Object.entries(this.truthSignals)) {
      for (const phrase of phrases) {
        if (text.includes(phrase)) {
          signals.push({
            type: signalType,
            phrase: phrase,
            strength: 1
          });
          totalScore += 1;
        }
      }
    }

    return {
      signals,
      totalScore,
      confidence: signals.length > 0 ? Math.min(0.95, 0.5 + (signals.length * 0.15)) : 0
    };
  },

  /**
   * Get severity score for manipulation type
   */
  getSeverity(patternType) {
    const severities = {
      gaslighting: 5,
      loveBombing: 3,
      futureFaking: 3,
      guilTripping: 4,
      stonewalling: 3,
      deflection: 3,
      triangulation: 4,
      victimPlaying: 3,
      wordSalad: 3,
      silentTreatment: 3
    };
    return severities[patternType] || 2;
  },

  /**
   * Detect text incoherence (word salad indicator)
   */
  detectIncoherence(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    if (sentences.length < 2) return 0;

    // Simple coherence check: topic consistency
    const words = text.split(/\s+/);
    const uniqueRatio = new Set(words).size / words.length;

    // High unique ratio with long text = potential word salad
    if (words.length > 50 && uniqueRatio > 0.8) return 0.7;

    return 0;
  },

  /**
   * Get consciousness level label from score
   */
  getConsciousnessLevel(score) {
    for (const [key, range] of Object.entries(this.consciousnessLevels)) {
      if (score >= range.min && score <= range.max) {
        return range.label;
      }
    }
    return 'Unknown';
  },

  /**
   * Generate recommended response based on analysis
   */
  generateResponse(manipulation, truth, algorithm) {
    if (algorithm === 'DECEIT') {
      const primary = manipulation.patterns[0];
      if (!primary) return 'Stay neutral. Observe patterns over time.';

      const responses = {
        gaslighting: 'Trust your memory. Document interactions. Do not engage in debate about reality.',
        loveBombing: 'Slow down. Healthy relationships build gradually. Watch for consistency.',
        futureFaking: 'Focus on actions, not promises. Set concrete timelines with consequences.',
        guilTripping: 'You are not responsible for their emotions. Maintain your boundaries.',
        stonewalling: 'Name the behavior. "I notice you\'re shutting down. Let\'s revisit when you\'re ready."',
        deflection: 'Redirect to original topic. "We can discuss that separately. Right now we\'re talking about X."',
        triangulation: 'Verify claims directly. Do not accept secondhand "everyone thinks" statements.',
        victimPlaying: 'Acknowledge feelings without accepting blame. "I hear you\'re frustrated. That doesn\'t change X."',
        wordSalad: 'Request clarity. "I want to understand. Can you give me one specific example?"',
        silentTreatment: 'State your boundary. "I\'m available to talk when you\'re ready. I won\'t chase."'
      };

      return responses[primary.type] || 'Maintain boundaries. Do not JADE (Justify, Argue, Defend, Explain).';
    }

    // Truth algorithm detected
    if (truth.signals.length > 0) {
      return 'Positive signals detected. This communication shows accountability and clarity. Engage openly.';
    }

    return 'Neutral communication. Continue observing for pattern consistency.';
  },

  /**
   * Batch analyze multiple messages
   */
  analyzeBatch(messages) {
    return messages.map((msg, index) => ({
      index,
      ...this.analyze(msg)
    }));
  },

  /**
   * Analyze conversation thread for patterns over time
   */
  analyzeThread(messages) {
    const results = this.analyzeBatch(messages);

    // Calculate trends
    const avgConsciousness = results.reduce((sum, r) => sum + r.consciousness_score, 0) / results.length;
    const totalManipulation = results.reduce((sum, r) => sum + r.manipulation.score, 0);
    const totalTruth = results.reduce((sum, r) => sum + r.truth.score, 0);

    // Pattern frequency
    const patternFrequency = {};
    results.forEach(r => {
      r.manipulation.patterns.forEach(p => {
        patternFrequency[p.type] = (patternFrequency[p.type] || 0) + 1;
      });
    });

    return {
      message_count: messages.length,
      average_consciousness: Math.round(avgConsciousness),
      total_manipulation_score: totalManipulation,
      total_truth_score: totalTruth,
      dominant_algorithm: totalManipulation > totalTruth ? 'DECEIT' : 'TRUTH',
      pattern_frequency: patternFrequency,
      individual_results: results,
      recommendation: avgConsciousness < 50
        ? 'This communication pattern shows consistent manipulation. Consider limiting contact or setting firm boundaries.'
        : 'Communication patterns are generally healthy. Continue with awareness.'
    };
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CommunicationAnalyzer;
}

// Browser global
if (typeof window !== 'undefined') {
  window.CommunicationAnalyzer = CommunicationAnalyzer;
}
