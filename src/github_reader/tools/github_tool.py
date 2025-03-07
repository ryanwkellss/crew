# src/tools/github_tool.py
import requests
import os
from crewai_tools import tool

GITHUB_API_URL = "https://api.github.com"

class GitHubTool:
    def __init__(self, repo_owner, repo_name, access_token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.headers = {"Authorization": f"token {access_token}"}

    @tool("fetch_pull_request_files")
    def fetch_pull_request_files(self, pr_number: int) -> dict:
        """
        Fetches the changed files and their diffs from a GitHub Pull Request.
        """
        url = f"{GITHUB_API_URL}/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            files = response.json()
            return {
                file["filename"]: file["patch"] for file in files if "patch" in file
            }
        else:
            return {"error": f"Failed to fetch PR files. Status: {response.status_code}"}
