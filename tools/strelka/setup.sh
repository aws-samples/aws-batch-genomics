#!/usr/bin/env bash

# Build and Deploy Strelka

cd tools/strelka/docker

REPO_URI=$(aws ecr describe-repositories --repository-names strelka --output text --query "repositories[0].repositoryUri")

if [ -z "$REPO_URI" ]
then
    REPO_URI=$(aws ecr create-repository --repository-name strelka  --output text --query "repository.repositoryUri")
    echo "Created repo successfully."
fi

make REGISTRY=${REPO_URI}

cd ../../../