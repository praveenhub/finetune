#!/bin/bash
# This script sets up GitHub SSH configuration for multiple accounts

# First, clean up any UseKeychain entries which aren't supported in Linux
if [ -f ~/.ssh/config ]; then
    sed -i '/UseKeychain/d' ~/.ssh/config
    echo "Removed unsupported UseKeychain entries from SSH config"
fi

# Create a clean SSH config for GitHub
cat > ~/.ssh/config.github << EOF
# Default GitHub (praveenhm account)
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_git_praveenhm
  AddKeysToAgent yes
  IdentitiesOnly yes

# Second GitHub account (praveenhub)
Host github-praveenhub
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_git_praveenhub
  AddKeysToAgent yes
  IdentitiesOnly yes
EOF

# Append the GitHub config to the main config or replace it
if [ -f ~/.ssh/config ]; then
    # Remove any existing GitHub configuration
    grep -v -E 'github|praveenhm|praveenhub' ~/.ssh/config > ~/.ssh/config.tmp
    # Add the clean GitHub config
    cat ~/.ssh/config.github >> ~/.ssh/config.tmp
    # Replace the config
    mv ~/.ssh/config.tmp ~/.ssh/config
else
    # Create a new config with just the GitHub config
    cp ~/.ssh/config.github ~/.ssh/config
fi

# Set proper permissions
chmod 600 ~/.ssh/config

echo "GitHub SSH config has been updated."

# Set the remote URL for the current repository
if [ -d "/workspaces/finetune/.git" ]; then
    # For the praveenhub account specifically
    git -C /workspaces/finetune remote set-url origin git@github-praveenhub:praveenhub/finetune.git
    echo "Set Git remote URL to use your github-praveenhub configuration"
fi
