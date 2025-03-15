#!/bin/bash

# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh

# Set proper permissions
chmod 700 ~/.ssh

# Add the deploy key to authorized_keys
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAPrKfO8aEYhQQ+oBGbalhsM1kg4ZTjFgdMuezgeeb0t macbook@Macs-MacBook-Pro.local" >> ~/.ssh/authorized_keys

# Set proper permissions for authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Ensure SSH configuration allows key-based authentication
# This part is optional as most SSH servers allow this by default
if [ -f /etc/ssh/sshd_config ]; then
    # Check if we have permission to modify the file
    if [ -w /etc/ssh/sshd_config ]; then
        # Make sure these settings are enabled
        sudo grep -q "^PubkeyAuthentication yes" /etc/ssh/sshd_config || sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
        sudo grep -q "^AuthorizedKeysFile" /etc/ssh/sshd_config || sudo sed -i 's/#AuthorizedKeysFile/AuthorizedKeysFile/' /etc/ssh/sshd_config
        
        # Restart SSH service if we made changes
        sudo systemctl restart sshd
    else
        echo "Warning: Cannot modify /etc/ssh/sshd_config (permission denied)"
        echo "Please ensure PubkeyAuthentication is enabled in your SSH configuration"
    fi
fi

echo "SSH key setup complete!" 