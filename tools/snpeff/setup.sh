#!/usr/bin/env bash

# Build and Deploy SNPEff

cd tools/snpeff/docker

REPO_URI=$(aws ecr describe-repositories --repository-names snpeff --output text --query "repositories[0].repositoryUri")

if [ -z "$REPO_URI" ]
then
    REPO_URI=$(aws ecr create-repository --repository-name snpeff  --output text --query "repository.repositoryUri")
    echo "Created repo successfully."
fi

make REGISTRY=${REPO_URI}

cd ../../../