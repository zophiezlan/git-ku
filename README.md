# git-ku (Haikommit)

🎋 A Git hook that generates genuinely useful commit messages that just happen to be 5-7-5 haiku poems.

## Philosophy

> A commit message should be clear. A haiku is art. Your code is art. Therefore, your commit message should be a haiku.

Haikommit reconciles the descriptive need of a commit message with the poetic constraint of a 5-7-5 syllable structure.

## Features

- 🎨 **Automatic Haiku Generation**: Analyzes your staged changes and generates descriptive haiku commit messages
- 🧠 **Intent Detection**: Understands if your commit is a fix, feature, refactor, test, or documentation
- 📝 **Keyword Extraction**: Extracts meaningful terms from filenames and code changes
- 🔢 **Syllable Counting**: Uses a comprehensive syllable counter with support for technical terms
- ⚙️ **Configurable**: Add custom syllable counts for your project's specific jargon
- 🪝 **Git Hook Integration**: Seamlessly integrates with Git's `prepare-commit-msg` hook

## Installation

### Quick Install

From the root of your Git repository, run:

```bash
curl -sSL https://raw.githubusercontent.com/zophiezlan/git-ku/main/install.sh | bash
```

### Manual Install

1. Clone this repository or download the files:
   ```bash
   git clone https://github.com/zophiezlan/git-ku.git
   cd git-ku
   ```

2. Run the installer from your project's root directory:
   ```bash
   ./install.sh
   ```

The installer will:
- Copy `haikommit.py` to your repository root
- Install the `prepare-commit-msg` hook in `.git/hooks/`
- Make the hook executable

## Usage

Once installed, using Haikommit is automatic:

1. Stage your changes:
   ```bash
   git add src/features/new-thing.js
   ```

2. Start a commit:
   ```bash
   git commit
   ```

3. Your editor opens with a generated haiku:
   ```
   New feature added
   The new thing js file here
   Does its job just right
   
   # Please enter the commit message for your changes...
   ```

4. Accept it or modify as needed, then save and close!

### Example Haiku Outputs

**For a bug fix:**
```
Bug fixed in code
Authentication repaired
Working now
```

**For a new feature:**
```
New feature added
Button component is here
Ready to use
```

**For refactoring:**
```
Code cleaned up now
User controller improved
Much better now
```

**For tests:**
```
Tests added here
Validation coverage
All passing now
```

**For documentation:**
```
Documentation
README updated clearly
Now up to date
```

## Configuration

Create a `.haikommitrc` file in your repository root or home directory to add custom syllable counts for project-specific terms:

```json
{
  "syllables": {
    "kubernetes": 4,
    "myproject": 2,
    "graphql": 2,
    "mongodb": 3
  }
}
```

See `.haikommitrc.example` for more examples.

## How It Works

1. **Hook Trigger**: When you run `git commit`, the `prepare-commit-msg` hook is triggered
2. **Diff Analysis**: Haikommit reads `git diff --staged` to see what changed
3. **Intent Detection**: Analyzes the diff to determine if it's a fix, feature, refactor, test, or docs change
4. **Keyword Extraction**: Extracts meaningful terms from:
   - File names (e.g., `userController.js` → "user", "controller")
   - Function/class names (e.g., `function checkAuth` → "check", "auth")
   - Changed code lines
5. **Haiku Generation**: Combines the analysis with syllable counting to generate a proper 5-7-5 haiku
6. **Message Creation**: Prepends the haiku to your commit message file

## Technical Details

### Intent Detection

Haikommit recognizes these commit types:

- **Fix**: Detects patterns like `fix`, `bug`, `patch`, `error`
- **Feature**: Detects patterns like `feat`, `add`, `create`, `new`
- **Refactor**: Detects patterns like `refactor`, `cleanup`, `style`, `optimize`
- **Test**: Detects test files (`.spec.js`, `.test.py`) and test-related terms
- **Docs**: Detects documentation files (`.md`) and doc-related terms
- **Update/Remove**: Falls back based on addition/deletion ratio

### Syllable Counting

The syllable counter uses:

1. **Custom Dictionary**: Your `.haikommitrc` configuration (highest priority)
2. **Technical Terms Dictionary**: Built-in dictionary with 100+ programming terms
3. **Heuristic Algorithm**: Fallback counter for unknown words using vowel patterns

### Requirements

- Python 3.6+
- Git
- A sense of poetic justice

## Uninstall

To remove Haikommit:

```bash
./uninstall.sh
```

Or manually:
```bash
rm .git/hooks/prepare-commit-msg
rm haikommit.py  # optional
```

## Development

### Testing Manually

You can test haiku generation without committing:

```bash
# Stage some changes
git add some-file.js

# Generate a haiku
python3 haikommit.py
```

### Testing with Different Diffs

```bash
# Pass a diff directly
echo "your diff content" | python3 haikommit.py --diff
```

## Contributing

Contributions are welcome! Whether it's:

- Adding more technical terms to the syllable dictionary
- Improving haiku templates
- Enhancing intent detection
- Fixing bugs
- Writing actual documentation

Please submit a Pull Request.

## Future Features

- [ ] Difficulty modes (`--mode=easy`, `--mode=hard`, `--mode=shakespeare`)
- [ ] REST API server (Haiku-as-a-Service)
- [ ] Multiple language support
- [ ] Machine learning-based haiku generation
- [ ] Rhyming mode (because why not?)

## License

MIT License - See LICENSE file for details

## Credits

Inspired by the ancient art of haiku and the modern art of version control.

---

*"In code we trust, through Git we flow, in haiku we commit."* 🎋
