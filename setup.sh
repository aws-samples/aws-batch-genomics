#!/usr/bin/env bash

set -e

echo "Zip Tool Scripts & Create Template Bucket"

### Unpack multi-tenant tools and docker containers for Job/Tasks
zip -r tools.zip ./tools

## To Do
### - specify target bucket
### - separate tools
###     - SSM ECS + docker build/push
###     - batch job definitions
###     - stepfunctions state machine
###     - different pull for common_utils w/o tool pull
###     - reference is defined by docker image
### - Provenance
###     - parameterize Tool version of docker images

## PreReq
### 1. EC2 permissions
###     - SSM
###     - Region set
### 2. Tools zipped 

## Stacks
### 1. batch-genomics-zone  - creates S3 bucket for holding tools & nested stacks
### 2. batch-genomics-tools 
###     - IAM role for Batch
###     - SSM for deploying AMI 
###     - Repo in ECR & build/push docker
### 3. batch-genomics-pipeline (nested)
###     - VPC stack
###     - role stack
###     - batchEnvstack
###     - batchJobstack
###     - statemachinestack

## Resources
### 1. S3: 
###     - batch-genomics-zone-templatesbucket-UID
###     - batch-genomics-pipeline-jobresultsbucket-UID
### 2. SSM: 
###     - batch-genomics-tools-AWSBatchGenomicsBuildAmiSsmDocument-UID
###     - batch-genomics-tools-AWSBatchGenomicsBuildToolsSsmDocument-UID
### 3. AMI: BatchGenomics-TIMESTAMP
### 3a ECR: 
###     - Isaac
###     - SamtoolsStats
###     - SNPEff
###     - Strelka
### 4. VPC:
###     - vpc-UID
###     - VPCGatewayAttachment: batch-VPCGa-UID 
###     - subnets (A,B,C): subnet-UID
###     - SubnetRoutTableAssociation (A,B,C): rtbassoc-UID
###     - RouteTable: rtb-UID
###     - InternetGateway: igw-UID
###     - InternetRoute: batch-Inter-UID
###     - SecurityGroup: sg-UID   
### 5. Roles
###     - IAMRoles
###         BatchServiceRole-UID
###         ECSInstanceRole-UID
###         ECSTaskRole-UID
###         SpotFleetRole-UID
###         StatesExecutionRole-UID
###     - InstanceProfile
###         ECSInstanceRole-UID
### 6. BatchEnvironment
###     - BatchComputeEnv: 
###         GenomicOnDemandEnv-UID
###         GenomicSpotEnv-UID
###     - Batch Job Queue
###         HighPriority
###         LowPriority
### 7. BatchJob Definitions
###     - Isaac:1
###     - SamtoolsStats:1
###     - SNPEff:1
###     - Strelka:1
### 8. StepFunction stateMachine:
###     - GenomicWorkflow-UID

## Notes
### - AWS multi-tenant adapter is common_utils; any updates to it requires a re-build/push to docker

#------- S3 Bucket: (1) Cloudformation Templates (2) Tools folder & ssm agent

aws cloudformation create-stack --stack-name batch-genomics-zone --template-body file://template_cfn.yml --capabilities CAPABILITY_NAMED_IAM --enable-termination-protection --output text;
aws cloudformation wait stack-create-complete --stack-name batch-genomics-zone

echo "Copy Nested Templates to S3 for Deployment"

TEMPLATES_BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name batch-genomics-zone --query 'Stacks[].Outputs[?OutputKey==`TemplatesBucket`].OutputValue' --output text)
TEMPLATES_BUCKET_ARN=$(aws cloudformation describe-stacks --stack-name batch-genomics-zone --query 'Stacks[].Outputs[?OutputKey==`TemplatesBucketArn`].OutputValue' --output text)
aws s3 cp ./pipeline/nested_templates s3://${TEMPLATES_BUCKET_NAME} --recursive

echo "Copy Build Scripts to S3 for Deployment"

aws s3 cp tools.zip s3://${TEMPLATES_BUCKET_NAME}/tools.zip
aws s3 cp ./tools/common_utils/install_ssm_agent.sh s3://${TEMPLATES_BUCKET_NAME}/install_ssm_agent.sh
rm tools.zip

#------- AMI: (1) Build Custom AMI. Tools: (1) Register Tools in ECR, (2) Build & Push each Tool to docker.
cd tools

echo "Deploy SSM Automation Docs for Image and Tools Deployment"

aws cloudformation create-stack --stack-name batch-genomics-tools --template-body file://template_cfn.yml --capabilities CAPABILITY_NAMED_IAM --enable-termination-protection --output text --parameters    ParameterKey=TemplatesBucketName,ParameterValue=${TEMPLATES_BUCKET_NAME} ParameterKey=TemplatesBucketArn,ParameterValue=${TEMPLATES_BUCKET_ARN};
aws cloudformation wait stack-create-complete --stack-name batch-genomics-tools

ACCOUNT_ID=$(aws cloudformation describe-stacks --stack-name batch-genomics-tools --query 'Stacks[].Outputs[?OutputKey==`AccountId`].OutputValue' --output text)
BUILD_AMI_DOC_NAME=$(aws cloudformation describe-stacks --stack-name batch-genomics-tools --query 'Stacks[].Outputs[?OutputKey==`BuildAMIDocumentName`].OutputValue' --output text)
BUILD_TOOLS_DOC_NAME=$(aws cloudformation describe-stacks --stack-name batch-genomics-tools --query 'Stacks[].Outputs[?OutputKey==`BuildToolsDocumentName`].OutputValue' --output text)

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
AMI_NAME="BatchGenomics-${TIMESTAMP}"

#---- AMI: wget, ssm, curl, awscli; mount docker_scratch; create image (terminate instance)
echo "Build & Deploy Image with SSM Automation"

EXEC_ID=$(aws ssm start-automation-execution --document-name ${BUILD_AMI_DOC_NAME}  --parameters "TargetAmiName=${AMI_NAME}" --query "AutomationExecutionId" --output text)
echo "SSM ExecId: ${EXEC_ID}"

STATUS="Started"
while [ "$STATUS" != "Success" -a "$STATUS" != "Failed" -a "$STATUS" != "TimedOut" -a "$STATUS" != "Cancelled" ]
do
    STATUS=$(aws ssm describe-automation-executions --query "AutomationExecutionMetadataList[?AutomationExecutionId==\`${EXEC_ID}\`].AutomationExecutionStatus" --output text)
    STEP=$(aws ssm describe-automation-step-executions --automation-execution-id ${EXEC_ID} --query "StepExecutions[?StepStatus=='InProgress'].StepName" --output text)
    echo "${STATUS}:${STEP}"
    sleep 120
done

if [ "$STATUS" != "Success" ]
then
    echo "AMI build '${STATUS}'."
    exit -1
fi

IMAGE_ID=$(aws ec2 describe-images --owners ${ACCOUNT_ID} --filters "Name=name,Values=${AMI_NAME}" --query 'sort_by(Images, &CreationDate)[].ImageId' --output text)
echo "Built ImageId: ${IMAGE_ID}"

#---- Tools
echo "Build & Deploy Tools with SSM Automation"

EXEC_ID=$(aws ssm start-automation-execution --document-name ${BUILD_TOOLS_DOC_NAME} --query "AutomationExecutionId" --output text)

STATUS="Started"
while [ "$STATUS" != "Success" -a "$STATUS" != "Failed" -a "$STATUS" != "TimedOut" -a "$STATUS" != "Cancelled" ]
do
    STATUS=$(aws ssm describe-automation-executions --query "AutomationExecutionMetadataList[?AutomationExecutionId==\`${EXEC_ID}\`].AutomationExecutionStatus" --output text)
    STEP=$(aws ssm describe-automation-step-executions --automation-execution-id ${EXEC_ID} --query "StepExecutions[?StepStatus=='InProgress'].StepName" --output text)
    echo "${STATUS}:${STEP}"
    sleep 120
done

if [ "$STATUS" != "Success" ]
then
    echo "Tools build '${STATUS}'."
    exit -1
fi


#------- Pipeline: (1) Nested Stacks: VPC, Role, BatchEnv, BatchJob, StateMachine (2) Hardcoded example input

echo "Deploy Pipeline Stack"

cd ..
cd pipeline

aws cloudformation create-stack --stack-name batch-genomics-pipeline --template-body file://template_cfn.yml --capabilities CAPABILITY_NAMED_IAM --enable-termination-protection --output text --parameters ParameterKey=TemplatesBucket,ParameterValue=${TEMPLATES_BUCKET_NAME} ParameterKey=ImageId,ParameterValue=${IMAGE_ID};aws cloudformation wait stack-create-complete --stack-name batch-genomics-pipeline

cd ..

FULL_INPUT=$(aws cloudformation describe-stacks --stack-name batch-genomics-pipeline --query 'Stacks[].Outputs[?OutputKey==`FullWorkflowInput`].OutputValue' --output text)

echo "Go to the Step Functions console and run the GenomicsWorkflow-* workflow with this as input:"

echo "${FULL_INPUT}"

echo " "
