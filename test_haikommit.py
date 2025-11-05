#!/usr/bin/env python3
"""
Test suite for Haikommit
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from haikommit import SyllableCounter, DiffAnalyzer, HaikuGenerator


def test_syllable_counter():
    """Test syllable counting functionality"""
    counter = SyllableCounter()
    
    # Test common words
    assert counter.count_syllables('bug') == 1, "bug should be 1 syllable"
    assert counter.count_syllables('feature') == 2, "feature should be 2 syllables"
    assert counter.count_syllables('documentation') == 5, "documentation should be 5 syllables"
    
    # Test tech terms
    assert counter.count_syllables('async') == 2, "async should be 2 syllables"
    assert counter.count_syllables('function') == 2, "function should be 2 syllables"
    assert counter.count_syllables('kubernetes') == 4, "kubernetes should be 4 syllables"
    
    # Test phrases
    assert counter.count_phrase('Code changes made here') == 5, "Should be 5 syllables"
    assert counter.count_phrase('All done now') == 3, "Should be 3 syllables"
    
    print("✓ Syllable counter tests passed")


def test_custom_dictionary():
    """Test custom syllable dictionary"""
    custom = {'testword': 3, 'myapp': 2}
    counter = SyllableCounter(custom)
    
    assert counter.count_syllables('testword') == 3, "Custom word should have 3 syllables"
    assert counter.count_syllables('myapp') == 2, "Custom word should have 2 syllables"
    
    print("✓ Custom dictionary tests passed")


def test_diff_analyzer():
    """Test diff analysis functionality"""
    analyzer = DiffAnalyzer()
    
    # Test fix detection
    fix_diff = """
diff --git a/src/auth.js b/src/auth.js
+++ b/src/auth.js
@@ -10,0 +11 @@
+  if (error) throw new Error('Auth failed');
"""
    result = analyzer.analyze(fix_diff)
    assert result['intent'] == 'fix', f"Should detect fix intent, got {result['intent']}"
    assert 'auth.js' in result['files'], "Should extract filename"
    
    # Test feature detection
    feature_diff = """
diff --git a/src/Button.jsx b/src/Button.jsx
new file mode 100644
+++ b/src/Button.jsx
@@ -0,0 +1,5 @@
+export function Button() {
+  return <button>Click</button>;
+}
"""
    analyzer2 = DiffAnalyzer()
    result = analyzer2.analyze(feature_diff)
    assert result['intent'] == 'feature', f"Should detect feature intent, got {result['intent']}"
    
    # Test docs detection
    docs_diff = """
diff --git a/README.md b/README.md
+++ b/README.md
@@ -1,0 +2,3 @@
+## Installation
+Run `npm install`
"""
    analyzer3 = DiffAnalyzer()
    result = analyzer3.analyze(docs_diff)
    assert result['intent'] == 'docs', f"Should detect docs intent, got {result['intent']}"
    
    print("✓ Diff analyzer tests passed")


def test_haiku_generator():
    """Test haiku generation"""
    counter = SyllableCounter()
    generator = HaikuGenerator(counter)
    
    # Test with different intents
    test_cases = [
        {
            'intent': 'fix',
            'files': ['auth.js'],
            'keywords': ['error', 'token', 'fix']
        },
        {
            'intent': 'feature',
            'files': ['Button.jsx'],
            'keywords': ['button', 'component', 'new']
        },
        {
            'intent': 'docs',
            'files': ['README.md'],
            'keywords': ['readme', 'documentation']
        },
    ]
    
    for test in test_cases:
        haiku = generator.generate(test)
        lines = haiku.split('\n')
        
        assert len(lines) == 3, f"Haiku should have 3 lines, got {len(lines)}"
        
        # Check each line has reasonable length
        for line in lines:
            assert len(line.strip()) > 0, "Line should not be empty"
            assert len(line.strip()) < 100, "Line should not be too long"
        
        print(f"✓ Generated haiku for {test['intent']}:")
        print(f"  {haiku}")
        print()
    
    print("✓ Haiku generator tests passed")


def test_syllable_counts():
    """Test that generated haikus follow 5-7-5 pattern (approximately)"""
    counter = SyllableCounter()
    generator = HaikuGenerator(counter)
    
    analysis = {
        'intent': 'fix',
        'files': ['controller.js'],
        'keywords': ['auth', 'user', 'error']
    }
    
    haiku = generator.generate(analysis)
    lines = haiku.split('\n')
    
    syllable_counts = [counter.count_phrase(line) for line in lines]
    
    print(f"✓ Syllable counts: {syllable_counts}")
    
    # Allow some tolerance (±1 syllable)
    assert 4 <= syllable_counts[0] <= 6, f"First line should be ~5 syllables, got {syllable_counts[0]}"
    assert 6 <= syllable_counts[1] <= 8, f"Second line should be ~7 syllables, got {syllable_counts[1]}"
    assert 4 <= syllable_counts[2] <= 6, f"Third line should be ~5 syllables, got {syllable_counts[2]}"
    
    print("✓ Syllable pattern tests passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running Haikommit Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_syllable_counter()
        test_custom_dictionary()
        test_diff_analyzer()
        test_haiku_generator()
        test_syllable_counts()
        
        print()
        print("=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print()
        print("=" * 50)
        print(f"✗ Test failed: {e}")
        print("=" * 50)
        return 1
    except Exception as e:
        print()
        print("=" * 50)
        print(f"✗ Unexpected error: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
