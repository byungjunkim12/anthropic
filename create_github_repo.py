
"""
GitHub Repository Creator using MCP

This script demonstrates how to use MCP (Model Control Protocol) to create a GitHub repository
and handle possible errors that might occur during the process.
"""

import os
import requests
import json
import time

# Configuration
REPO_NAME = "my-awesome-repo"
USERNAME = "byungjunkim12"
DESCRIPTION = "My awesome repository created via MCP"
PRIVATE = False
AUTO_INIT = True

# MCP API details
MCP_BASE_URL = "https://api.mcp-platform.com"  # Replace with actual MCP API URL
MCP_API_KEY = os.environ.get("MCP_API_KEY")  # Store your API key in environment variables

def create_github_repo():
    """
    Create a GitHub repository using MCP API
    """
    if not MCP_API_KEY:
        raise ValueError("MCP_API_KEY environment variable not set")
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MCP_API_KEY}"
    }
    
    # Prepare the GitHub repository creation payload
    payload = {
        "function_name": "create_repository",
        "parameters": {
            "name": REPO_NAME,
            "description": DESCRIPTION,
            "private": PRIVATE,
            "autoInit": AUTO_INIT
        }
    }
    
    try:
        # Send request to MCP API
        response = requests.post(
            f"{MCP_BASE_URL}/github/repositories",
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        print(f"Repository created successfully!")
        print(f"Repository URL: {result.get('html_url', 'URL not available')}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error creating repository: {e}")
        
        # Check if we have response details to provide more context
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                print(f"Error details: {json.dumps(error_details, indent=2)}")
            except:
                print(f"Status code: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
        
        return None

def verify_repository_exists(max_retries=5, delay=2):
    """
    Verify that the repository was created by checking GitHub API directly
    """
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
    print(f"Creating repository '{REPO_NAME}' for user '{USERNAME}'...")
    result = create_github_repo()
    
    if result:
        # Wait briefly before verification to allow for GitHub to process
        time.sleep(3)
        verify_repository_exists()
    else:
        print("Repository creation failed. Please check the error messages above.")
