# Environment Setup Guide

This guide explains how to configure environment variables for the Kiwi SQL Generation project.

## Quick Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your actual values:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Set the required API key:**
   ```bash
   # For ModelScope (recommended)
   export MODELSCOPE_API_KEY="your-actual-api-key"
   
   # Or for OpenAI
   export OPENAI_API_KEY="your-actual-api-key"
   ```

## Required Environment Variables

### ModelScope Configuration (Primary)
- `MODELSCOPE_API_KEY`: Your ModelScope API key (required)
- `MODELSCOPE_API_BASE`: API base URL (default: https://api-inference.modelscope.cn/v1/)
- `MODELSCOPE_MODEL`: Model name (default: Qwen/Qwen2.5-32B-Instruct)

### OpenAI Configuration (Alternative)
- `OPENAI_API_KEY`: Your OpenAI API key (if not using ModelScope)

## Security Best Practices

### ✅ Do:
- Use environment variables for all sensitive data
- Keep your `.env` file local and never commit it
- Use different API keys for development and production
- Regularly rotate your API keys

### ❌ Don't:
- Hardcode API keys in source code
- Commit `.env` files to version control
- Share API keys in chat or email
- Use production keys in development

## Getting API Keys

### ModelScope API Key
1. Visit [ModelScope](https://modelscope.cn/)
2. Create an account or log in
3. Go to your profile settings
4. Generate an API token
5. Copy the token to your `.env` file

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or log in
3. Go to API Keys section
4. Create a new secret key
5. Copy the key to your `.env` file

## Verification

Test your configuration:

```bash
# Check if environment variables are loaded
python -c "import os; print('MODELSCOPE_API_KEY:', 'SET' if os.getenv('MODELSCOPE_API_KEY') else 'NOT SET')"

# Run the application
python src/kiwi/kiwi_app.py
```

## Troubleshooting

### Error: "MODELSCOPE_API_KEY environment variable is required"
- Make sure you've set the `MODELSCOPE_API_KEY` environment variable
- Check that your `.env` file is in the project root directory
- Verify the API key is valid and not expired

### Error: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Error: API authentication failed
- Verify your API key is correct
- Check if your API key has the necessary permissions
- Ensure you're using the correct API base URL

## Development vs Production

### Development
```bash
# .env file
MODELSCOPE_API_KEY=dev-api-key
FLASK_ENV=development
FLASK_DEBUG=true
```

### Production
```bash
# Set environment variables directly
export MODELSCOPE_API_KEY="prod-api-key"
export FLASK_ENV=production
export FLASK_DEBUG=false
```

## Docker Configuration

If using Docker, pass environment variables:

```bash
# Using .env file
docker run --env-file .env kiwi-app

# Using individual variables
docker run -e MODELSCOPE_API_KEY="your-key" kiwi-app
```

## CI/CD Configuration

For GitHub Actions or other CI/CD:

```yaml
env:
  MODELSCOPE_API_KEY: ${{ secrets.MODELSCOPE_API_KEY }}
```

Remember to add your API keys to your CI/CD secrets, not to the repository files.