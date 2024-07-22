import os
import subprocess

# List of repository names (directories)
repos = [
    'xyz',
    'xyz',
    # add all repository directories here
]

# Base directory where repositories are located
base_dir = '.'

# File paths
file1_path = './file-path'
file2_path = './filepath'

# Branch name for the new changes
branch_name = ''

# Command to add files to the repository
def add_files(repo_dir):
    subprocess.run(['cp', file1_path, repo_dir])
    subprocess.run(['cp', file2_path, repo_dir])
    subprocess.run(['git', 'add', '.'], cwd=repo_dir)

# Command to commit the changes
def commit_changes(repo_dir):
    subprocess.run(['git', 'commit', '-m', '<commit-msg'], cwd=repo_dir)

# Command to push the changes
def push_changes(repo_dir):
    subprocess.run(['git', 'push', 'origin', branch_name], cwd=repo_dir)

# Command to create a new branch and switch to it
def create_branch(repo_dir):
    subprocess.run(['git', 'checkout', '-b', branch_name], cwd=repo_dir)

# Command to create a pull request using GitHub CLI
def create_pull_request(repo_dir):
    subprocess.run(['gh', 'pr', 'create', '--title', '<pr-title>', '--body', '<pr-description>', '--base', 'main'], cwd=repo_dir)

# Main script execution
if __name__ == '__main__':
    for repo_name in repos:
        repo_dir = os.path.join(base_dir, repo_name)

        # Create and switch to the new branch
        create_branch(repo_dir)

        # Add the files
        add_files(repo_dir)

        # Commit the changes
        commit_changes(repo_dir)

        # Push the changes
        push_changes(repo_dir)

        # Create a pull request
        create_pull_request(repo_dir)
