# Create a workflow orchestration engine with AWS Step Functions

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

For information about AWS Step Functions, see https://aws.amazon.com/step-functions/.