
"""
GitHub Repository Creator using Anthropic's MCP Client

This script demonstrates how to use the Anthropic Python client to interact with MCP services
for creating GitHub repositories and handling the response properly.
"""

import os
import json
import time
from typing import Dict, Any, Optional
import anthropic  # pip install anthropic

# Configuration
REPO_NAME = "my-awesome-repo"
USERNAME = "byungjunkim12"
DESCRIPTION = "My awesome repository created via Anthropic MCP client"
PRIVATE = False
AUTO_INIT = True

# Anthropic API configuration
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-3-7-sonnet-20250219"  # Use the appropriate model

def create_github_repo_with_anthropic() -> Optional[Dict[str, Any]]:
    """
    Create a GitHub repository using Anthropic's client to access MCP
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Construct the message for repository creation
    system_message = """
    You are a helpful assistant that will create a GitHub repository for the user.
    Use the provided repository name, username, and other parameters to create the repository.
    IMPORTANT: Do not include any explanations or thoughts in your response. 
    Only execute the repository creation and return the raw result.
    """
    
    user_message = f"""
    Create a GitHub repository with these parameters:
    - Repository name: {REPO_NAME}
    - Username: {USERNAME}
    - Description: {DESCRIPTION}
    - Private: {PRIVATE}
    - Initialize with README: {AUTO_INIT}
    """
    
    try:
        # Call the Anthropic API with tool use enabled
        response = client.messages.create(
            model=MODEL,
            system=system_message,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=1024,
            tools=[
                {
                    "name": "create_repository",
                    "description": "Create a new GitHub repository in your account",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Repository name"
                            },
                            "description": {
                                "type": "string",
                                "description": "Repository description"
                            },
                            "private": {
                                "type": "boolean",
                                "description": "Whether the repository should be private"
                            },
                            "autoInit": {
                                "type": "boolean",
                                "description": "Initialize with README.md"
                            }
                        },
                        "required": ["name"]
                    }
                }
            ],
        )
        
        # Process the response
        content = response.content
        
        # Extract the tool use response from the response content
        tool_content = None
        for content_item in content:
            if content_item.type == 'tool_use' or hasattr(content_item, 'tool_use'):
                tool_content = content_item
                break
        
        if not tool_content:
            print("No tool use found in response")
            return None
        
        # Extract repository details from the response
        try:
            repo_details = json.loads(tool_content.tool_use.input)
            print(f"Repository creation request submitted successfully:")
            print(f"- Name: {repo_details.get('name')}")
            print(f"- Description: {repo_details.get('description')}")
            print(f"- Private: {repo_details.get('private')}")
            return repo_details
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing repository details: {e}")
            return None
    
    except Exception as e:
        print(f"Error creating repository: {e}")
        return None

def verify_repository_exists(max_retries=5, delay=2):
    """
    Verify that the repository was created by checking GitHub API directly
    """
    import requests
    
    github_api_url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(github_api_url)
            
            if response.status_code == 200:
                repo_info = response.json()
                print(f"Repository verification successful!")
                print(f"Owner: {repo_info['owner']['login']}")
                print(f"Repo: {repo_info['name']}")
                print(f"URL: {repo_info['html_url']}")
                return True
            
            print(f"Repository not found (attempt {attempt+1}/{max_retries}), retrying in {delay} seconds...")
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            print(f"Error verifying repository: {e}")
            time.sleep(delay)
    
    print("Repository verification failed after multiple attempts.")
    return False

if __name__ == "__main__":
    print(f"Creating repository '{REPO_NAME}' for user '{USERNAME}' using Anthropic MCP client...")
    result = create_github_repo_with_anthropic()
    
    if result:
        # Wait briefly before verification to allow for GitHub to process
        time.sleep(3)
        verify_repository_exists()
    else:
        print("Repository creation request failed. Please check the error messages above.")
