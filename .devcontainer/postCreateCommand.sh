#!/bin/bash
set -e

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks

# Setup SSH for GitHub - using SSH agent forwarding
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add GitHub's host key to known_hosts
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts 2>/dev/null

# Check if SSH agent forwarding is working
ssh-add -l > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "SSH agent forwarding is working. Your local SSH keys are available."
else
    echo ""
    echo "================ SSH AGENT FORWARDING NOTICE ================"
    echo "SSH agent forwarding might not be set up correctly."
    echo ""
    echo "To enable it on your host machine:"
    echo "1. Start the SSH agent:"
    echo "   - Windows: Set-Service ssh-agent -StartupType Automatic && Start-Service ssh-agent"
    echo "   - Linux:   eval \"\$(ssh-agent -s)\""
    echo "   - macOS:   ssh-agent is usually running by default"
    echo ""
    echo "2. Add your SSH key to the agent:"
    echo "   ssh-add ~/.ssh/your_github_key"
    echo ""
    echo "3. Rebuild the devcontainer"
    echo "============================================================="
    echo ""
fi
