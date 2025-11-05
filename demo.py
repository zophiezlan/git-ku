#!/usr/bin/env python3
"""
Demo script to show Haikommit in action
"""

from haikommit import SyllableCounter, DiffAnalyzer, HaikuGenerator

# Sample diffs to demonstrate different intents
SAMPLE_DIFFS = {
    "Bug Fix": """diff --git a/src/auth/login.js b/src/auth/login.js
index abc123..def456 100644
--- a/src/auth/login.js
+++ b/src/auth/login.js
@@ -10,6 +10,7 @@ export async function loginUser(credentials) {
   try {
     const user = await findUser(credentials.email);
+    if (!user) throw new Error('User not found');
     const token = generateToken(user);
     return { success: true, token };
   } catch (error) {
""",
    
    "New Feature": """diff --git a/src/components/NotificationBell.tsx b/src/components/NotificationBell.tsx
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/src/components/NotificationBell.tsx
@@ -0,0 +1,25 @@
+import React from 'react';
+import { Bell } from 'lucide-react';
+
+export function NotificationBell({ count }) {
+  return (
+    <button className="notification-bell">
+      <Bell size={24} />
+      {count > 0 && <span className="badge">{count}</span>}
+    </button>
+  );
+}
""",
    
    "Refactoring": """diff --git a/src/utils/validators.js b/src/utils/validators.js
index 111222..333444 100644
--- a/src/utils/validators.js
+++ b/src/utils/validators.js
@@ -1,10 +1,5 @@
-export function validateEmail(email) {
-  const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
-  return regex.test(email);
-}
-
-export function validatePassword(password) {
-  return password.length >= 8;
+export const validators = {
+  email: (email) => /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email),
+  password: (pass) => pass.length >= 8
 }
""",
    
    "Test Addition": """diff --git a/tests/validators.spec.js b/tests/validators.spec.js
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/tests/validators.spec.js
@@ -0,0 +1,15 @@
+import { validators } from '../src/utils/validators';
+
+describe('Email Validator', () => {
+  test('accepts valid email', () => {
+    expect(validators.email('test@example.com')).toBe(true);
+  });
+  
+  test('rejects invalid email', () => {
+    expect(validators.email('notanemail')).toBe(false);
+  });
+});
""",
    
    "Documentation": """diff --git a/README.md b/README.md
index 111222..333444 100644
--- a/README.md
+++ b/README.md
@@ -1,5 +1,25 @@
 # My Awesome Project
 
-Simple project description
+## Overview
+
+This project provides a comprehensive solution for managing user authentication
+and authorization in modern web applications.
+
+## Installation
+
+```bash
+npm install awesome-auth
+```
+
+## Quick Start
+
+```javascript
+import { Auth } from 'awesome-auth';
+
+const auth = new Auth({ apiKey: 'your-key' });
+await auth.login(credentials);
+```
""",
}

def main():
    print("=" * 60)
    print("🎋 Haikommit Demo - Haiku Commit Messages 🎋")
    print("=" * 60)
    print()
    
    counter = SyllableCounter()
    analyzer = DiffAnalyzer()
    generator = HaikuGenerator(counter)
    
    for title, diff in SAMPLE_DIFFS.items():
        print(f"\n{'─' * 60}")
        print(f"📝 {title}")
        print('─' * 60)
        
        # Analyze
        analysis = analyzer.analyze(diff)
        
        print(f"Intent: {analysis['intent']}")
        print(f"Files: {', '.join(analysis['files']) if analysis['files'] else 'N/A'}")
        print(f"Keywords: {', '.join(analysis['keywords'][:5]) if analysis['keywords'] else 'N/A'}")
        print()
        
        # Generate haiku
        haiku = generator.generate(analysis)
        
        print("Generated Haiku:")
        print("┌─────────────────────────────────────────┐")
        for line in haiku.split('\n'):
            syllables = counter.count_phrase(line)
            print(f"│ {line:40}│ ({syllables} syllables)")
        print("└─────────────────────────────────────────┘")
        
    print()
    print("=" * 60)
    print("✨ Demo Complete! ✨")
    print("=" * 60)
    print()
    print("To use Haikommit in your project:")
    print("  1. Run: ./install.sh")
    print("  2. Stage changes: git add <files>")
    print("  3. Commit: git commit")
    print("  4. Enjoy your poetic commit messages! 🎋")
    print()

if __name__ == '__main__':
    main()
