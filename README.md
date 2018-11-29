# Genomics Research on AWS

This project demonstrates how to run a large-scale, genomics secondary-analysis pipeline on [AWS](https://aws.amazon.com/) using [AWS Step Functions](https://aws.amazon.com/step-functions/) and [AWS Batch](https://aws.amazon.com/batch/).

![Standard Genomic Secondary-Analysis Workflow](https://docs.opendata.aws/genomics-workflows/images/genomics-workflow.png "Standard Genomic Secondary-Analysis Workflow")


## PREREQUISITES

* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* Admin permissions for deployment

## DEPLOY

*Will build and deploy everything needed to run a secondary-analysis pipeline on AWS.  This includes:*
1. Custom AMI with 1TB scratch volume using the ECS AMI for your region **(10 min)**
2. Isaac, Strelka, Samtools-Stats and SnpEff as Docker images in ECR **(40 min)**
3. AWS Batch queues, compute environments, job definitions and an AWS Step Functions state machine **(10 min)**
4. Roles and buckets needed.

````bash
$ setup.sh 
````

## USAGE

**Run the Workflow**

*Copy the workflow input that was output to the terminal window after the deployment completed.  Use that input to run the pipeline in the StepFunctions console.  You can also find example workflow inputs in the outputs section of the **batch-genomics-pipeline** Cloudformation stack.*

**Update Pipeline Stack**

*Deploy changes made to local Cloudformation templates.*

````bash
$ update.sh
````

**Teardown Pipeline Stack**

*Deletes everything except the custom AMI and ECR images.*

````bash
$ teardown.sh
````


