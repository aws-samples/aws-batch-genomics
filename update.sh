#!/usr/bin/env bash

# Copy Nested Templates for Deployment

cd pipeline

TEMPLATES_BUCKET=$(aws cloudformation describe-stacks --stack-name batch-genomics-zone --query 'Stacks[].Outputs[?OutputKey==`TemplatesBucket`].OutputValue' --output text)
aws s3 cp nested_templates s3://${TEMPLATES_BUCKET} --recursive

cd ..

# Update Zone Stack

aws cloudformation update-stack --stack-name batch-genomics-zone --template-body file://zone_template_cfn.yml --capabilities CAPABILITY_NAMED_IAM --output text;aws cloudformation wait stack-create-complete --stack-name batch-genomics-zone

cd tools

# Update Tools Stack

aws cloudformation update-stack --stack-name batch-genomics-tools --template-body file://template_cfn.yml --capabilities CAPABILITY_NAMED_IAM --output text;aws cloudformation wait stack-create-complete --stack-name batch-genomics-zone

cd ..
cd pipeline

# Update Pipeline Stack

IMAGE_ID=$(aws cloudformation describe-stacks --stack-name batch-genomics-pipeline --query 'Stacks[].Outputs[?OutputKey==`ImageId`].OutputValue' --output text)

aws cloudformation update-stack --stack-name batch-genomics-pipeline --template-body file://pipeline/template_cfn.yml --capabilities CAPABILITY_NAMED_IAM --output text --parameters ParameterKey=TemplatesBucket,ParameterValue=${TEMPLATES_BUCKET} ParameterKey=ImageId,ParameterValue=${IMAGE_ID};aws cloudformation wait stack-update-complete --stack-name batch-genomics-pipeline

cd ..