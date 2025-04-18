# Anthropic Repository

This repository contains simple examples and projects related to Anthropic's technology.

## Files

- **test.py**: A simple Python script that demonstrates a basic function to print "Hello, Anthropic!".
- **create_github_repo.py**: A script that demonstrates how to use MCP (Model Control Protocol) to create a GitHub repository.
- **mcp_github_client.py**: A script that uses the Anthropic Python client to interact with MCP services for creating GitHub repositories.

## Usage

### Basic Test

To run the test.py file:

```bash
python test.py
```

This will output: `Hello, Anthropic!`

### Using MCP to Create GitHub Repositories

To use the GitHub repository creation scripts, you need to set up the appropriate environment variables first:

#### For create_github_repo.py:

```bash
export MCP_API_KEY="your_mcp_api_key_here"
python create_github_repo.py
```

#### For mcp_github_client.py:

```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
python mcp_github_client.py
```

## Troubleshooting MCP GitHub Repository Creation

If you encounter issues with repository creation, here are some common problems and solutions:

1. **Truncated Responses**: Ensure you're properly handling the complete response from the MCP service.
2. **Error Parsing**: Add proper error handling and verify the response structure.
3. **API Key Issues**: Confirm your API keys are valid and have the necessary permissions.
4. **Response Verification**: Always verify that the repository was successfully created by checking directly with the GitHub API.

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/byungjunkim12/anthropic.git
   ```

2. Navigate to the project directory:
   ```bash
   cd anthropic
   ```

3. Install required dependencies:
   ```bash
   pip install requests anthropic
   ```

4. Set required environment variables:
   ```bash
   export ANTHROPIC_API_KEY="your_key_here"
   export MCP_API_KEY="your_mcp_key_here"
   ```

5. Run one of the scripts:
   ```bash
   python mcp_github_client.py
   ```
