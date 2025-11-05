#!/bin/bash
#
# Haikommit uninstaller
# Removes the prepare-commit-msg hook from your local .git/hooks directory
#

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}Error: Not in a git repository root directory${NC}"
    echo "Please run this script from the root of your git repository"
    exit 1
fi

HOOK_PATH=".git/hooks/prepare-commit-msg"

if [ ! -f "$HOOK_PATH" ]; then
    echo -e "${YELLOW}No prepare-commit-msg hook found${NC}"
    exit 0
fi

# Check if there's a backup
if [ -f "$HOOK_PATH.backup" ]; then
    echo -e "${YELLOW}Found backup of previous hook${NC}"
    read -p "Do you want to restore it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mv "$HOOK_PATH.backup" "$HOOK_PATH"
        echo -e "${GREEN}✓ Restored previous hook${NC}"
        exit 0
    fi
fi

# Remove the hook
rm "$HOOK_PATH"
echo -e "${GREEN}✓ Haikommit hook removed${NC}"

# Optionally remove haikommit.py
if [ -f "./haikommit.py" ]; then
    read -p "Do you also want to remove haikommit.py? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm ./haikommit.py
        echo -e "${GREEN}✓ Removed haikommit.py${NC}"
    fi
fi

exit 0
