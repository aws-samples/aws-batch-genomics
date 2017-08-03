# Create AWS Lambda and AWS Step Functions

Now that we have Docker images in ECR ([Step 1](01-creating-docker-images.md)) and a working AWS Batch Environment ([Step 2](02-creating-batch-env.md)) you will need to create the individual AWS Lambda functions to execute single applications, and the AWS Step Functions necessary to orchastrate the full workflow.

## Creating the individual AWS Lambda functions

First, you will need to create Lambda functions that execute each tool contained in a Docker image, as well as get the status of a jobs. They can be found at:

| Name                        | File location                                     |
| :-------------------------- | :------------------------------------------------ |
| batchSubmitJob              |  `batch/runner/batch_submit_job.py`               |
| batchGetJobStatus           |  `batch/runner/batch_get_job_status.py`           |
| batchSubmitIsaacJob         |  `tools/isaac/lambda/lambda_function.py`          |
| batchSubmitStrelkaJob       |  `tools/strelka/lambda/lambda_function.py`        |
| batchSubmitSamtoolsStatsJob |  `tools/samtools_stats/lambda/lambda_function.py` |
| batchSubmitSnpeffJob        |  `tools/snpeff/lambda/lambda_function.py`         |


For the next step you will need to capture the ARNs from the newly created Lambda functions and use that information within the AWS Step Functions.

Here is an example of creating a Lamda function for running SAMtools using the AWS CLI. We give the command line the `LambdaBatchExecutionRole` IAM Role that was created in the previous step.

```shell
# cd <repo_root>/tools/samtools_stats/lambda/

zip lambda_function.zip lambda_function.py

aws lambda create-function --function-name batchSubmitSamtoolsStatsJob \
  --runtime python2.7 \
  --role "arn:aws:iam::123456789012:role/iam-batch-lambdaBatchExecutionRole-HD21E5IYV2WU" \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://./lambda_function.zip 
```

Now repeat for the other functions that are needed. If you forget to jot down the Lambda function ARNs you can query for them using the CLI

```shell
aws lambda list-functions --output json --query "Functions[].[FunctionName, FunctionArn]"
```
