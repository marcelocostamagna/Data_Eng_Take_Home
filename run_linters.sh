#!/bin/bash
set +e
# Repo root directory
REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"

echo "Running linters on DAGs folder"
flake8 --count --max-line-length=110 --statistics $REPO_ROOT_DIR/dags

echo ""
echo "Stylecheck complete!"
echo ""
