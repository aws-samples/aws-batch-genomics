#!/usr/bin/env bash

# Get Bucket Names from Stacks

TEMPLATES_BUCKET=$(aws cloudformation describe-stacks --stack-name batch-genomics-zone --query 'Stacks[].Outputs[?OutputKey==`TemplatesBucket`].OutputValue' --output text); echo ${TEMPLATES_BUCKET}
RESULTS_BUCKET=$(aws cloudformation describe-stacks --stack-name batch-genomics-pipeline --query 'Stacks[].Outputs[?OutputKey==`JobResultsBucket`].OutputValue' --output text); echo ${RESULTS_BUCKET}

# Clear Buckets

aws s3 rm --recursive s3://${TEMPLATES_BUCKET}/
aws s3 rm --recursive s3://${RESULTS_BUCKET}/

# Disable Termination Protection on Stacks

aws cloudformation update-termination-protection --no-enable-termination-protection --stack-name batch-genomics-tools
aws cloudformation update-termination-protection --no-enable-termination-protection --stack-name batch-genomics-pipeline
aws cloudformation update-termination-protection --no-enable-termination-protection --stack-name batch-genomics-zone

# Delete Stacks

aws cloudformation delete-stack --stack-name batch-genomics-tools; aws cloudformation wait stack-delete-complete --stack-name batch-genomics-tools
aws cloudformation delete-stack --stack-name batch-genomics-pipeline; aws cloudformation wait stack-delete-complete --stack-name batch-genomics-pipeline
aws cloudformation delete-stack --stack-name batch-genomics-zone; aws cloudformation wait stack-delete-complete --stack-name batch-genomics-zone
