import os
import subprocess
import requests

# List of repository names (directories)
repos = [
    'xyz',
    'xyz',
    # List repos 
]

# Base directory where repositories are located
base_dir = '.'

# File paths
file1_path = './file_path'
file2_path = './file_path'

# Branch name for the new changes
branch_name = 'branch-name'

# GitLab server information
gitlab_url = 'your-gitlab url'
gitlab_token = 'your-gitlab-token'

# Command to add files to the repository
def add_files(repo_dir):
    print(f'Adding files to {repo_dir}')
    subprocess.run(['cp', file1_path, repo_dir])
    subprocess.run(['cp', file2_path, repo_dir])
    # Add subproccess if needed
    subprocess.run(['git', 'add', '.'], cwd=repo_dir)

# Command to commit the changes
def commit_changes(repo_dir):
    print(f'Committing changes in {repo_dir}')
    subprocess.run(['git', 'commit', '-m', 'commit-msg'], cwd=repo_dir)

# Command to push the changes
def push_changes(repo_dir):
    print(f'Pushing changes from {repo_dir}')
    subprocess.run(['git', 'push', 'origin', branch_name], cwd=repo_dir)

# Command to create a new branch and switch to it
def create_branch(repo_dir):
    print(f'Creating branch in {repo_dir}')
    subprocess.run(['git', 'checkout', '-b', branch_name], cwd=repo_dir)

# Command to create a merge request using GitLab API
def create_merge_request(repo_name, repo_dir):
    print(f'Creating merge request for {repo_name}')
    project_id = get_project_id(repo_name)
    if project_id:
        mr_url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests'
        headers = {
            'Private-Token': gitlab_token
        }
        data = {
            'title': '<your-pr-title>',
            'description': '<your-pr-description>',
            'source_branch': branch_name,
            'target_branch': 'main'
        }
        response = requests.post(mr_url, headers=headers, data=data)
        if response.status_code == 201:
            print(f'Merge request created for {repo_name}')
        else:
            print(f'Failed to create merge request for {repo_name}: {response.content}')

# Function to get the project ID from the GitLab server
def get_project_id(repo_name):
    project_url = f'{gitlab_url}/api/v4/projects'
    headers = {
        'Private-Token': gitlab_token
    }
    params = {
        'search': repo_name
    }
    response = requests.get(project_url, headers=headers, params=params)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project['path'] == repo_name:
                return project['id']
    print(f'Project ID not found for {repo_name}')
    return None

# Main script execution
if __name__ == '__main__':
    for repo_name in repos:
        repo_dir = os.path.join(base_dir, repo_name)
        if not os.path.exists(repo_dir):
            print(f'Directory {repo_dir} does not exist. Skipping...')
            continue

        # Create and switch to the new branch
        create_branch(repo_dir)

        # Add the files
        add_files(repo_dir)

        # Commit the changes
        commit_changes(repo_dir)

        # Push the changes
        push_changes(repo_dir)

        # Create a merge request
        create_merge_request(repo_name, repo_dir)
