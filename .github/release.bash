#!/bin/bash

echo $1
echo $2

echo "Replace Version inside tfutility"
echo "__version__= \"$2\"" > src/tfutility/__init__.py

echo "Replace Docker image Reference inside README.md"
sed -i "s/tfutility:$1/tfutility:$2/" README.md


echo "Replace pre-commit Reference inside README.md"
sed -i "s/ref: $1/ref: $2/" README.md

echo "Replace Docker image Reference inside pre-commit-hook"
sed -i "s/tfutility:$1/tfutility:$1/" .pre-commit-hooks.yaml