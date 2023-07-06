#!/usr/bin/env python3
# A crude way to bump the version of the web app.
# Required in order to upload to the private PyPI repository.
# Otherwise, the upload will fail with the following error: 
# HTTPError: 400 Client Error
import re
import subprocess

# Specify the branch name where the hook should run
target_branch = "gitlab"

# Specify the path to the VERSION.txt file
version_file_path = "VERSION.txt"

# Regular expression pattern to match semantic version
version_pattern = r"(\d+)\.(\d+)\.(\d+)"

def increment_version(version, part="patch"):
    major, minor, patch = version.groups()
    if part == "major":
        major = int(major) + 1
    elif part == "minor":
        minor = int(minor) + 1
    elif part == "patch":
        patch = int(patch) + 1
    else:
        raise ValueError(f"Invalid version part: {part}")
    return f"{major}.{minor}.{patch}"

def main():
    # Executes the following shell command to obtain the branch name
    # git rev-parse --abbrev-ref HEAD
    branch_name = subprocess.check_output(
        "git rev-parse --abbrev-ref HEAD", shell=True
    ).decode("utf-8").strip()

    if not branch_name or not branch_name.endswith(target_branch):
        return

    # Read the current version from the VERSION.txt file
    with open(version_file_path, "r") as file:
        version = file.read().strip()
    
    print(f"Current version: {version}")

    # Increment the minor version
    version = re.sub(version_pattern, increment_version, version)

    # Write the updated version back to the file
    with open(version_file_path, "w") as file:
        file.write(version)

    print(f"Version updated to {version}")
    print("Staging the updated VERSION.txt file...")
    
    exit(subprocess.check_call(["git", "add", version_file_path]))

if __name__ == "__main__":
    main()
