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

# Set proper permissions for SSH files
find ~/.ssh -type f -name "id_*" ! -name "*.pub" -exec chmod 600 {} \;
find ~/.ssh -type f -name "*.pub" -exec chmod 644 {} \;

# Add GitHub's host key to known_hosts
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts 2>/dev/null

# Fix SSH config file if it exists and contains UseKeychain
if [ -f ~/.ssh/config ]; then
    # Remove UseKeychain lines which aren't supported in Linux
    sed -i '/UseKeychain/d' ~/.ssh/config
    echo "Fixed SSH config file (removed UseKeychain option)"
fi

# Set up GitHub SSH configuration
chmod +x .devcontainer/github-ssh-setup.sh
./.devcontainer/github-ssh-setup.sh

# Fix SSH agent socket permissions if needed
if [ -S "$SSH_AUTH_SOCK" ]; then
    # Get the owner of the socket
    SOCKET_USER=$(stat -c '%U' $SSH_AUTH_SOCK 2>/dev/null || stat -f '%Su' $SSH_AUTH_SOCK 2>/dev/null)
    # Get current user
    CURRENT_USER=$(whoami)

    echo "SSH agent socket owned by: $SOCKET_USER"
    echo "Current user: $CURRENT_USER"

    # If socket exists but permissions are wrong, fall back to creating our own key
    if [ "$SOCKET_USER" != "$CURRENT_USER" ]; then
        echo "SSH agent socket permissions issue detected. Creating fallback SSH key..."
        # Generate SSH key if it doesn't exist
        if [ ! -f ~/.ssh/id_ed25519 ]; then
            ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
            echo ""
            echo "================ IMPORTANT ================"
            echo "Add this SSH key to your GitHub account:"
            cat ~/.ssh/id_ed25519.pub
            echo "=========================================="
            echo ""
            # Configure git to use this key
            git config --global core.sshCommand "ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes"
        fi
    fi
fi

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
