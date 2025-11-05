# Contributing to Haikommit

Thank you for your interest in contributing to Haikommit! 🎋

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Provide a clear description of the problem
- Include example diffs that produce unexpected haikus
- Mention your Python version and OS

### Suggesting Enhancements

- Explain the use case and benefit
- Provide examples if possible
- Consider backward compatibility

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-haiku`)
3. Make your changes
4. Run the test suite (`python3 test_haikommit.py`)
5. Commit your changes (ideally with a haiku!)
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/git-ku.git
cd git-ku

# Install in your local repo for testing
./install.sh

# Run tests
python3 test_haikommit.py

# Run demo
python3 demo.py
```

## Code Style

- Follow PEP 8 for Python code
- Add docstrings to new functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

## Testing

- Add tests for new features
- Ensure all existing tests pass
- Test with various diff types (fix, feature, refactor, etc.)
- Test syllable counting with edge cases

## Areas for Contribution

### High Priority

- **Syllable Dictionary**: Add more technical terms and their syllable counts
- **Haiku Templates**: Create more varied and natural-sounding templates
- **Intent Detection**: Improve accuracy of commit type detection
- **Edge Cases**: Handle unusual diffs better

### Medium Priority

- **Configuration Options**: Add more customization options
- **Error Handling**: Improve error messages and graceful failures
- **Performance**: Optimize for large diffs
- **Documentation**: Improve examples and guides

### Future Features

- Difficulty modes (easy/hard/shakespeare)
- REST API server
- Multiple language support
- Machine learning-based generation
- Integration with GitHub Actions

## Technical Terms Dictionary

When adding to the syllable dictionary in `haikommit.py`, please:

1. Verify syllable counts (use https://www.howmanysyllables.com/ or similar)
2. Add common variations (singular/plural, tenses)
3. Group related terms together
4. Keep alphabetical order within groups

Example:
```python
'react': 2,      # Re-act
'redux': 2,      # Re-dux
'reducer': 3,    # Re-du-cer
```

## Haiku Quality Guidelines

A good commit haiku should:

1. Follow 5-7-5 syllable pattern (±1 syllable acceptable)
2. Be descriptive of the actual change
3. Use relevant keywords from the diff
4. Sound natural when read aloud
5. Maintain the poetic spirit

Example of a good haiku:
```
Bug fixed in auth
User validation added
Login works now
```

Example of a bad haiku:
```
The the code changed now
Modified to work better
The working well now
```

## Pull Request Guidelines

- Title should clearly describe the change
- Include "Fixes #issue" if applicable
- Add examples of new haikus generated
- Update README if adding features
- Update tests if changing behavior

## Questions?

Feel free to open an issue for questions or join discussions in existing issues.

---

Thank you for helping make commit messages more poetic! 🎋
