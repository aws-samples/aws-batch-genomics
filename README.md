# Genomics Research on AWS

## A tutorial on how to package and deploy a bioinformatics  workflow on AWS using AWS Batch

This tutorial will cover the material presented within the "Genomics Workflows on AWS"  blog post series that covers the basics of bootstrappign a bioinformatics analysis pipeline on AWS. We break down the tutorial roughly as follows:

1. Setting up your AWS account (if you do not already have one)
2. Package a set of bioinformatics applications using Docker
3. Create a AWS Batch environment for analysis
4. Define and deploy AWS Step Functions to control the data processing steps
5. Initiate a workflow

## Step 1. Set up an AWS account and the AWS Command Line Interface

If you don't already have a AWS account, please follow the ["Backup Files to Amazon S3 using the AWS CLI"](https://aws.amazon.com/getting-started/tutorials/backup-to-s3-cli/) 10 minute tutorial to make sure you have a working AWS environment needed for this tutorial.

We will also assume that you are working on a system that can build Docker images. If not, please refer to the Docker [getting started](https://www.docker.com/community-edition) guides.

To ensure that you are logged into your Amazon ECR repos, type `eval $(aws ecr get-login)` into your terminal

## Step 2. Building Docker images for applications

Each individual application used in the tutorial has been packaged as a Docker container. The Docker container packaging methodology is described in Part 2 of the tutorial. We have provided a Makefile to build all of the necessary Docker images for this demonstration project, as well as deploy each container to a AWS EC2 Container Registry (ECR). Below is an example to enable you to build and deploy the Docker container image for Isaac.  Prior to installing Isaac please review the license [here](https://github.com/Illumina/Isaac3/blob/master/COPYRIGHT) and verify it is acceptable to you for your use.
```bash
# From the root of the repository directory
cd tools/isaac/docker

# Create a ECR repository for Isaac, then copy the `repositoryUri` into a variable
REPO_URI=$(aws ecr create-repository --repository-name isaac \
  --output text --query "repository.repositoryUri")

# If the repository already exists, then
# query ECR for the `repositoryUri`
REPO_URI=$(aws ecr describe-repositories \
  --repository-names snap \
  --output text --query "repositories[0].repositoryUri")

# execute the build supplying the repositoryUri
make REGISTRY=$(REPO_URI)
```

Repeat the above for SAMtools (license [here](https://github.com/samtools/htslib/blob/develop/LICENSE)), Strelka (license [here](https://github.com/Illumina/strelka/blob/master/LICENSE.txt)), and SnpEff (license is LGPLv3, as referenced [here](http://snpeff.sourceforge.net/download.html)).

## Step 3. Setting up AWS Batch for an analysis environment

First, you will want to set up all of your IAM policies and roles with the following command:

```bash
aws cloudformation create-stack --stack-name iam-batch --template-body file://batch/setup/iam.template.yaml --capabilities CAPABILITY_NAMED_IAM
```

We have provided a python script to configure your batch environment. While you can also do this via the CLI, the script in `batch/setup/create_batch_env.py` will do this for you. Please see the README.md in `batch/setup` for additional information on how to run this set up script. Effectively, this script creates your compute environments, job queues, and then job definitions.

## Step 4. Define and deploy AWS Step Functions to control the data processing steps

First, you will need to create Lambda functions (python2.7) for each tool to submit the jobs, as well as get the status of a jobs. They can be found at:
- batchSubmitJob: `batch/runner/batch_submit_job.py`
- batchSubmitIsaacJob: `tools/isaac/lambda/lambda_function.py`
- batchSubmitStrelkaJob: `tools/strelka/lambda/lambda_function.py`
- batchSubmitSamtoolsStatsJob: `tools/samtools_stats/lambda/lambda_function.py`
- batchSubmitSnpeffJob: `tools/snpeff/lambda/lambda_function.py`
- batchGetJobStatus: `batch/runner/batch_get_job_status.py`

Next, capture the ARNs from the newly created Lambda functions and use that information in your to deploy the CloudFormation stack for the workflow.
```bash
aws cloudformation create-stack --stack-name genomics-workflow \
--template-body file://workflow/deploy_state_machine.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters <list of parameters with the above ARNs>
```

Record the arn of the state machine that was created.

## Step 5. Initiate a workflow
Modify the file `workflow/test.input.json` to direct to the appropriate paths in your own account.

Next, execute the following CLI command:
```bash
aws stepfunctions start-execution --state-machine-arn <your-arn> --input file://workflow/test.input.json
```

You can then navigate to the AWS Step Functions console to monitor your workflow's progress.
