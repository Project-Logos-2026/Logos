#!/usr/bin/env bash
set -e

echo "Paste the GitHub Personal Access Token:"
read -s GH_TOKEN

export GH_TOKEN

echo ""
echo "Running GitHub Project setup..."

bash setup_github_project.sh
