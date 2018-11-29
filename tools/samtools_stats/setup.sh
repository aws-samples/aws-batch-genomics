#!/usr/bin/env bash

# Build and Deploy SamtoolsStats

cd tools/samtools_stats/docker

REPO_URI=$(aws ecr describe-repositories --repository-names samtools-stats --output text --query "repositories[0].repositoryUri")

if [ -z "$REPO_URI" ]
then
    REPO_URI=$(aws ecr create-repository --repository-name samtools-stats  --output text --query "repository.repositoryUri")
    echo "Created repo successfully."
fi

make REGISTRY=${REPO_URI}

cd ../../../
