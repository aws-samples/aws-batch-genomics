# Genomics Research on AWS

This project demonstrates how to run a large-scale, genomics secondary-analysis pipeline on [AWS](https://aws.amazon.com/) using [AWS Step Functions](https://aws.amazon.com/step-functions/) and [AWS Batch](https://aws.amazon.com/batch/).  You can learn more about how we used the new AWS Step Functions integration with AWS Batch in our blog post, [Building Simpler Genomics Workflows on AWS Step Functions](https://aws.amazon.com/blogs/compute/building-simpler-genomics-workflows-on-aws-step-functions/). 

![Standard Genomic Secondary-Analysis Workflow](https://docs.opendata.aws/genomics-workflows/images/genomics-workflow.png "Standard Genomic Secondary-Analysis Workflow")


## PREREQUISITES

* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* Admin permissions for deployment
    * SSM
    * Region set
    * teardown: write UpdateTerminationProtection
* Tools zipped 


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
This includes 
1. The S3 bucket with results
2. Roles


````bash
$ teardown.sh
````

## Compute Environment

**Stacks**

 1. batch-genomics-zone  - creates S3 bucket for holding tools & nested stacks
 2. batch-genomics-tools 
     - IAM role for Batch
     - SSM for deploying AMI 
     - Repo in ECR & build/push docker
 3. batch-genomics-pipeline (nested)
     - VPC stack
     - role stack
     - batchEnvstack
     - batchJobstack
     - statemachinestack

**Resources**
 1. S3: 
     - batch-genomics-zone-templatesbucket-UID
     - batch-genomics-pipeline-jobresultsbucket-UID
 2. SSM: 
     - batch-genomics-tools-AWSBatchGenomicsBuildAmiSsmDocument-UID
     - batch-genomics-tools-AWSBatchGenomicsBuildToolsSsmDocument-UID
 3. AMI: BatchGenomics-TIMESTAMP
 4. ECR: 
     - Isaac
     - SamtoolsStats
     - SNPEff
     - Strelka
 5. VPC:
     - vpc-UID
     - VPCGatewayAttachment: batch-VPCGa-UID 
     - subnets (A,B,C): subnet-UID
     - SubnetRoutTableAssociation (A,B,C): rtbassoc-UID
     - RouteTable: rtb-UID
     - InternetGateway: igw-UID
     - InternetRoute: batch-Inter-UID
     - SecurityGroup: sg-UID   
 6.   - IAMRoles
        - BatchServiceRole-UID
        - ECSInstanceRole-UID
        -  ECSTaskRole-UID
        -  SpotFleetRole-UID
        -  StatesExecutionRole-UID
     - InstanceProfile
        -  ECSInstanceRole-UID
 6. BatchEnvironment
     - BatchComputeEnv: 
        -  GenomicOnDemandEnv-UID
        -  GenomicSpotEnv-UID
     - Batch Job Queue
        -  HighPriority
        -  LowPriority
 7. BatchJob Definitions
     - Isaac:1
     - SamtoolsStats:1
     - SNPEff:1
     - Strelka:1
 8. StepFunction stateMachine:
     - GenomicWorkflow-UID

**Notes**
 - AWS multi-tenant adapter is common_utils; any updates to it requires a re-build/push to docker
 - re-running execution overwrites objects in result bucket


