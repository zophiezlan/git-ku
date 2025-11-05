#!/bin/bash
#
# Haikommit installer
# Installs the prepare-commit-msg hook into your local .git/hooks directory
#

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}Error: Not in a git repository root directory${NC}"
    echo "Please run this script from the root of your git repository"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy the Python script to the repository root (if not already there)
if [ ! -f "./haikommit.py" ]; then
    echo -e "${YELLOW}Copying haikommit.py to repository root...${NC}"
    cp "$SCRIPT_DIR/haikommit.py" ./haikommit.py
fi

# Install the hook
HOOK_PATH=".git/hooks/prepare-commit-msg"

if [ -f "$HOOK_PATH" ]; then
    echo -e "${YELLOW}Warning: prepare-commit-msg hook already exists${NC}"
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation cancelled${NC}"
        exit 1
    fi
    # Backup existing hook
    cp "$HOOK_PATH" "$HOOK_PATH.backup"
    echo -e "${GREEN}Backed up existing hook to $HOOK_PATH.backup${NC}"
fi

# Copy and make executable
cp "$SCRIPT_DIR/prepare-commit-msg" "$HOOK_PATH"
chmod +x "$HOOK_PATH"

echo -e "${GREEN}✓ Haikommit installed successfully!${NC}"
echo ""
echo "Usage:"
echo "  1. Stage your changes: git add <files>"
echo "  2. Commit: git commit"
echo "  3. Your editor will open with a generated haiku!"
echo ""
echo "Configuration:"
echo "  Create a .haikommitrc file to add custom syllable counts:"
echo '  {"syllables": {"myword": 3, "kubernetes": 4}}'
echo ""
echo "To uninstall:"
echo "  rm .git/hooks/prepare-commit-msg"
echo ""

exit 0
