#!/usr/bin/env python3
"""
Haikommit - Generate haiku commit messages from git diffs
"""

import sys
import re
import subprocess
from typing import List, Tuple, Dict, Optional
import json
import os

# Simple syllable counting using dictionary and heuristics
class SyllableCounter:
    """Count syllables in words using a dictionary and fallback heuristics"""
    
    def __init__(self, custom_dict: Optional[Dict[str, int]] = None):
        """Initialize with optional custom dictionary"""
        self.custom_dict = custom_dict or {}
        # Common programming terms with syllable counts
        self.tech_dict = {
            'async': 2, 'await': 2, 'const': 1, 'let': 1, 'var': 1,
            'function': 2, 'class': 1, 'import': 2, 'export': 2,
            'return': 2, 'lambda': 2, 'def': 1, 'jsx': 3, 'tsx': 3,
            'api': 3, 'json': 1, 'xml': 3, 'html': 4, 'css': 3,
            'js': 2, 'ts': 2, 'py': 1, 'npm': 3, 'git': 1,
            'test': 1, 'tests': 1, 'spec': 1, 'mock': 1,
            'boolean': 3, 'string': 1, 'integer': 3, 'array': 2,
            'object': 2, 'null': 1, 'undefined': 4, 'true': 1, 'false': 1,
            'button': 2, 'component': 3, 'controller': 3, 'model': 2,
            'view': 1, 'router': 2, 'service': 2, 'utils': 2,
            'config': 2, 'error': 2, 'token': 2, 'auth': 1,
            'login': 2, 'logout': 2, 'user': 2, 'admin': 2,
            'database': 3, 'schema': 2, 'query': 2, 'cache': 1,
            'redux': 2, 'react': 2, 'vue': 1, 'angular': 3,
            'typescript': 3, 'javascript': 4, 'python': 2,
            'docker': 2, 'kubernetes': 4, 'deploy': 2,
            'build': 1, 'compile': 2, 'bundle': 2, 'webpack': 2,
            'eslint': 2, 'prettier': 3, 'babel': 2,
            'readme': 2, 'license': 2, 'changelog': 2,
            'refactor': 3, 'cleanup': 2, 'optimize': 3,
            'feature': 2, 'bugfix': 2, 'hotfix': 2, 'patch': 1,
            'added': 2, 'removed': 2, 'updated': 3, 'fixed': 1,
            'changed': 1, 'created': 3, 'deleted': 3,
            'tested': 2, 'passed': 1, 'failed': 1, 'working': 2,
            'better': 2, 'improved': 2, 'modified': 3, 'complete': 2,
            'ready': 2, 'apply': 2, 'applied': 2,
        }
    
    def count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        if not word:
            return 0
        
        # Normalize the word
        word_lower = word.lower().strip()
        
        # Remove common programming symbols
        word_clean = re.sub(r'[^a-z]', '', word_lower)
        if not word_clean:
            return 0
        
        # Check custom dictionary first
        if word_clean in self.custom_dict:
            return self.custom_dict[word_clean]
        
        # Check tech dictionary
        if word_clean in self.tech_dict:
            return self.tech_dict[word_clean]
        
        # Fallback to heuristic counting
        return self._heuristic_count(word_clean)
    
    def _heuristic_count(self, word: str) -> int:
        """Use heuristic rules to count syllables"""
        if len(word) <= 1:
            return 1
        
        # Count vowel groups
        vowels = 'aeiouy'
        syllables = 0
        previous_was_vowel = False
        
        for i, char in enumerate(word):
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllables += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e') and syllables > 1:
            syllables -= 1
        
        # Adjust for common patterns
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            syllables += 1
        
        # Ensure at least 1 syllable
        return max(1, syllables)
    
    def count_phrase(self, phrase: str) -> int:
        """Count syllables in a phrase"""
        words = re.findall(r'[a-zA-Z]+', phrase)
        return sum(self.count_syllables(word) for word in words)


class DiffAnalyzer:
    """Analyze git diff to extract intent and keywords"""
    
    # Intent patterns
    FIX_PATTERNS = [
        r'\bfix\b', r'\bbug\b', r'\bpatch\b', r'\berror\b',
        r'\bissue\b', r'\brepair\b', r'\bcorrect\b'
    ]
    
    FEATURE_PATTERNS = [
        r'\bfeat\b', r'\badd\b', r'\bcreate\b', r'\bnew\b',
        r'\bimplement\b', r'\bintroduce\b'
    ]
    
    REFACTOR_PATTERNS = [
        r'\brefactor\b', r'\bcleanup\b', r'\bstyle\b',
        r'\brestructure\b', r'\bimprove\b', r'\boptimize\b'
    ]
    
    TEST_PATTERNS = [
        r'\btest\b', r'\.spec\.', r'\.test\.', r'__test__'
    ]
    
    DOCS_PATTERNS = [
        r'\bdoc\b', r'\breadme\b', r'\.md$', r'\bcomment\b'
    ]
    
    def __init__(self):
        self.intent = 'change'  # default
        self.files = []
        self.keywords = []
        
    def analyze(self, diff_output: str) -> Dict[str, any]:
        """Analyze the git diff and extract information"""
        # Reset state
        self.intent = 'change'
        self.files = []
        self.keywords = []
        
        self._detect_intent(diff_output)
        self._extract_files(diff_output)
        self._extract_keywords(diff_output)
        
        return {
            'intent': self.intent,
            'files': self.files,
            'keywords': self.keywords
        }
    
    def _detect_intent(self, diff: str):
        """Detect the primary intent of the changes"""
        diff_lower = diff.lower()
        
        # Check in order of priority
        if any(re.search(pattern, diff_lower) for pattern in self.TEST_PATTERNS):
            self.intent = 'test'
        elif any(re.search(pattern, diff_lower) for pattern in self.DOCS_PATTERNS):
            self.intent = 'docs'
        elif any(re.search(pattern, diff_lower) for pattern in self.FIX_PATTERNS):
            self.intent = 'fix'
        elif any(re.search(pattern, diff_lower) for pattern in self.FEATURE_PATTERNS):
            self.intent = 'feature'
        elif any(re.search(pattern, diff_lower) for pattern in self.REFACTOR_PATTERNS):
            self.intent = 'refactor'
        else:
            # Check if mostly additions
            additions = len(re.findall(r'^\+[^+]', diff, re.MULTILINE))
            deletions = len(re.findall(r'^-[^-]', diff, re.MULTILINE))
            if additions > deletions * 2:
                self.intent = 'feature'
            elif deletions > additions * 2:
                self.intent = 'remove'
            else:
                self.intent = 'update'
    
    def _extract_files(self, diff: str):
        """Extract modified file names"""
        # Match file paths in diff headers
        file_pattern = r'(?:diff --git a/|[\+\-]{3} [ab]/)([^\s]+)'
        files = re.findall(file_pattern, diff)
        
        # Get unique files and extract meaningful names
        seen = set()
        for file_path in files:
            if file_path != '/dev/null':
                # Get just the filename
                filename = os.path.basename(file_path)
                if filename not in seen:
                    seen.add(filename)
                    self.files.append(filename)
    
    def _extract_keywords(self, diff: str):
        """Extract keywords from the diff"""
        keywords = set()
        
        # Extract from filenames
        for filename in self.files:
            # Split on common delimiters
            parts = re.split(r'[._\-/]', filename)
            for part in parts:
                if len(part) > 2:  # Skip very short parts
                    keywords.add(part.lower())
        
        # Extract function/class names
        function_pattern = r'(?:function|def|class|const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        functions = re.findall(function_pattern, diff)
        keywords.update(f.lower() for f in functions if len(f) > 2)
        
        # Extract from added/modified lines (lines starting with +)
        added_lines = re.findall(r'^\+(.*)$', diff, re.MULTILINE)
        for line in added_lines:
            # Extract identifiers
            identifiers = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]{2,})\b', line)
            keywords.update(i.lower() for i in identifiers[:3])  # Limit per line
        
        # Keep most relevant keywords (limit to 10)
        self.keywords = list(keywords)[:10]


class HaikuGenerator:
    """Generate haiku based on analysis"""
    
    def __init__(self, syllable_counter: SyllableCounter):
        self.counter = syllable_counter
        
        # Templates for different intents
        self.templates = {
            'fix': [
                ("{problem}", "{action}", "{result}"),
                ("Bug found in {file}", "{action} applied to fix", "{result}"),
                ("{problem} no more", "{action} solves the issue", "{result}"),
            ],
            'feature': [
                ("{feature} added", "{description}", "Now complete"),
                ("New {feature}", "{description}", "{benefit}"),
                ("{feature} is here", "{description}", "Ready to use"),
            ],
            'refactor': [
                ("Code cleaned up now", "{description}", "{benefit}"),
                ("Refactored {file}", "{description}", "Much better now"),
                ("{description}", "Structure improved throughout", "Cleaner code now"),
            ],
            'test': [
                ("Tests added here", "{description}", "All passing now"),
                ("New test coverage", "{description}", "Safety improved"),
                ("{description}", "Validating the new code", "Tests all pass now"),
            ],
            'docs': [
                ("Documentation", "{description}", "Now up to date"),
                ("README updated", "{description}", "Much clearer now"),
                ("{description}", "Documentation improved here", "Better explained"),
            ],
            'update': [
                ("Updated {file}", "{description}", "Changes applied"),
                ("{description}", "Modified to improve flow", "Update complete"),
                ("Code updated now", "{description}", "Working better"),
            ],
            'remove': [
                ("Removed {file}", "{description}", "Cleanup complete"),
                ("{description}", "Unused code removed now", "Cleaner codebase"),
                ("Deleted old code", "{description}", "Simpler now"),
            ],
        }
        
        # Filler words/phrases for syllable adjustment
        self.fillers_5 = [
            "Code updated now", "Changes applied", "Working better",
            "Much better now", "All done here now", "Ready to use",
            "Update complete", "Fixed the bug now", "Added new code",
            "Cleanup complete", "Tests pass now", "All working well",
        ]
        
        self.fillers_7 = [
            "Applied to fix the problem", "Modified to improve flow",
            "Validating the new code", "Structure improved throughout",
            "Documentation improved here", "Better than before for sure",
            "Ready for use in production", "All the changes work as planned",
            "Everything is fixed and good", "Added to enhance the project",
        ]
        
    def generate(self, analysis: Dict) -> str:
        """Generate a haiku from the analysis"""
        intent = analysis['intent']
        files = analysis['files']
        keywords = analysis['keywords']
        
        # Get template
        templates = self.templates.get(intent, self.templates['update'])
        
        # Build haiku lines
        lines = self._build_haiku(intent, files, keywords, templates)
        
        return '\n'.join(lines)
    
    def _build_haiku(self, intent: str, files: List[str], keywords: List[str], templates: List[Tuple[str, str, str]]) -> List[str]:
        """Build a 5-7-5 haiku"""
        
        # Extract useful terms
        file_name = files[0] if files else 'code'
        file_base = os.path.splitext(file_name)[0] if files else 'file'
        keyword1 = keywords[0] if len(keywords) > 0 else 'change'
        keyword2 = keywords[1] if len(keywords) > 1 else 'update'
        
        # Try each template
        for template in templates:
            try:
                lines = self._try_template(template, intent, file_base, file_name, keyword1, keyword2)
                if lines:
                    return lines
            except:
                continue
        
        # Fallback to simple haiku
        return self._generate_simple_haiku(intent, file_base, keyword1)
    
    def _try_template(self, template: Tuple[str, str, str], intent: str, file_base: str, file_name: str, keyword1: str, keyword2: str) -> Optional[List[str]]:
        """Try to fill a template and adjust to 5-7-5"""
        
        # Substitution mapping
        subs = {
            '{problem}': f"{keyword1} error",
            '{action}': f"Fixed {keyword2}",
            '{result}': "Working now",
            '{feature}': keyword1,
            '{description}': f"{keyword2} in {file_base}",
            '{benefit}': "Improved code",
            '{file}': file_base,
        }
        
        lines = []
        target_syllables = [5, 7, 5]
        
        for i, line_template in enumerate(template):
            target = target_syllables[i]
            
            # Substitute variables
            line = line_template
            for var, value in subs.items():
                if var in line:
                    line = line.replace(var, value)
            
            # Adjust syllables
            line = self._adjust_syllables(line, target)
            if line is None:
                return None
            lines.append(line)
        
        return lines
    
    def _adjust_syllables(self, line: str, target: int) -> Optional[str]:
        """Adjust line to target syllable count"""
        current = self.counter.count_phrase(line)
        
        if current == target:
            return line
        
        # Try minor adjustments
        if current > target:
            diff = current - target
            # Try removing articles or shortening
            if diff >= 1 and ' the ' in line:
                line = line.replace(' the ', ' ', 1)
                line = re.sub(r'\s+', ' ', line).strip()
            elif diff >= 1 and ' a ' in line:
                line = line.replace(' a ', ' ', 1)
                line = re.sub(r'\s+', ' ', line).strip()
            elif diff >= 1 and ' an ' in line:
                line = line.replace(' an ', ' ', 1)
                line = re.sub(r'\s+', ' ', line).strip()
            
            # Check if we've matched target
            current = self.counter.count_phrase(line)
            if current == target:
                return line
        
        elif current < target:
            diff = target - current
            # Try adding words
            words = line.split()
            if len(words) > 0 and diff == 1:
                # Add 'now' at the end if appropriate
                if not line.endswith(' now'):
                    test_line = f"{line} now"
                    if self.counter.count_phrase(test_line) == target:
                        return test_line
        
        # If close enough, return the line
        if abs(current - target) <= 1:
            return line
        
        return None
    
    def _generate_simple_haiku(self, intent: str, subject: str, keyword: str) -> List[str]:
        """Generate a simple fallback haiku"""
        
        # Build context-aware lines
        if intent == 'fix':
            line1 = "Bug fixed in code"
            line2 = f"Fixed {keyword} {subject}"
            line3 = "Working well now"
        elif intent == 'feature':
            line1 = f"Added {keyword}"
            line2 = f"New {subject} is ready now"
            line3 = "Feature complete"
        elif intent == 'refactor':
            line1 = "Code cleaned up now"
            line2 = f"Refactored {subject}"
            line3 = "Better code now"
        elif intent == 'test':
            line1 = "Tests added here"
            line2 = f"Testing {subject} now"
            line3 = "All passing now"
        elif intent == 'docs':
            line1 = "Docs updated now"
            line2 = f"Improved {subject} readme"
            line3 = "Much clearer now"
        elif intent == 'remove':
            line1 = "Removed old code"
            line2 = f"Deleted {subject} file"
            line3 = "Cleanup complete"
        else:  # update
            line1 = "Code updated now"
            line2 = f"Modified {subject}"
            line3 = "Changes applied"
        
        # Adjust each line
        line1 = self._adjust_syllables(line1, 5) or "Code changes made here"
        line2 = self._adjust_syllables(line2, 7) or "Modified to work better now"
        line3 = self._adjust_syllables(line3, 5) or "Working well now"
        
        return [line1, line2, line3]


def load_custom_dict() -> Dict[str, int]:
    """Load custom syllable dictionary from .haikommitrc"""
    config_paths = [
        '.haikommitrc',
        os.path.expanduser('~/.haikommitrc'),
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    return data.get('syllables', {})
            except:
                pass
    
    return {}


def get_staged_diff() -> str:
    """Get the staged git diff"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def main():
    """Main entry point"""
    # Get diff from stdin or command line argument
    if len(sys.argv) > 1 and sys.argv[1] == '--diff':
        diff = sys.stdin.read() if len(sys.argv) == 2 else ' '.join(sys.argv[2:])
    else:
        diff = get_staged_diff()
    
    if not diff.strip():
        print("No changes staged")
        sys.exit(1)
    
    # Load custom dictionary
    custom_dict = load_custom_dict()
    
    # Initialize components
    counter = SyllableCounter(custom_dict)
    analyzer = DiffAnalyzer()
    generator = HaikuGenerator(counter)
    
    # Analyze and generate
    analysis = analyzer.analyze(diff)
    haiku = generator.generate(analysis)
    
    # Output the haiku
    print(haiku)


if __name__ == '__main__':
    main()
