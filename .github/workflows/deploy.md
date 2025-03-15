You can generate the SSH key pair either on your local machine or on your VPS. Let me explain both approaches:

## Option 2: Generate SSH key pair on your VPS

If you prefer to generate the keys directly on your VPS:

1. SSH into your VPS:
   ```bash
   ssh username@your-vps-ip
   ```

2. Generate the SSH key pair:
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy"
   ```

3. Follow the prompts as described above

4. Add the public key to the authorized_keys file:
   ```bash
   cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
   ```

5. Display the private key:
   ```bash
   cat ~/.ssh/id_ed25519
   ```

6. Copy the entire output (including BEGIN and END lines) and add it as a GitHub secret named `SSH_PRIVATE_KEY`

7. For security, consider removing the private key from your VPS after adding it to GitHub:
   ```bash
   rm ~/.ssh/id_ed25519
   ```

## Important Security Considerations:

1. Never share your private key or commit it to your repository
2. Use a dedicated key pair for GitHub Actions deployments
3. Consider restricting the key's permissions on your VPS using the `authorized_keys` file options
4. Regularly rotate your keys for enhanced security

Would you like me to provide more detailed instructions for either of these approaches?
