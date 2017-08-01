## Creating the AWS Step Functions

Once you have created the all of Lambda functions for individual workflow steps, you can utilize them as state machine components to quickly build flexible workflows that can process genomes in multiple ways.

We have provided a [CloudFormation template](../tools/workflow/deploy_state_machine.yaml) that you can use in the [CloudFormation Console](https://console.aws.amazon.com/cloudformation)

![CloudFormation console](https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2017/06/02/cfn_parameters.png )


You could also opt to use the AWS CLI to create the Step Functions using the ARNs from the newly created Lambda function and use that information in your to deploy the CloudFormation stack for the workflow.

```shell
aws cloudformation create-stack --stack-name genomics-workflow \
--template-body file://workflow/deploy_state_machine.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters <list of parameters with the above ARNs>
```

Where parameters are a space seperated set of strings of the form

```
ParameterKey=SamtoolsStatsLambdaArn,ParameterValue=arn:aws:lambda:us-east-1:123456789012:function:batchSubmitSamtoolsStatsJob
```

The set of template parameters are

```json
Parameters:
  - IsaacLambdaArn
  - StrelkaLambdaArn
  - SamtoolsStatsLambdaArn
  - SnpeffLambdaArn
  - BatchGetJobStatusLambdaArn
```

Once the CloudFormation stack is finished deploying, you should be able to see the following image of your state machine in the [Step Functions console](https://console.aws.amazon.com/states)

![Step Function Genomics Workflow](https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2017/06/02/statemachine_workflow.png)
