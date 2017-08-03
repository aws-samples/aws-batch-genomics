# Setting up AWS Batch for an analysis environment

If you followed the [account setup](00-account-setup.md) instructions you should have a working AWS environment for AWS Batch. If you are at all unsure, refer to the ["Setting up With AWS Batch"](http://docs.aws.amazon.com/batch/latest/userguide/get-set-up-for-aws-batch.html) and [AWS Batch Getting Started](http://docs.aws.amazon.com/batch/latest/userguide/Batch_GetStarted.html) guides.

After you have a working environment, you define several types of resources:

* IAM roles that provide service permissions
* A compute environment that launches and terminates compute resources for jobs
* A custom Amazon Machine Image (AMI)
* A job queue to submit the units of work and to schedule the appropriate * resources within the compute environment to execute those jobs
* Job definitions that define how to execute an application

## Creating the necessary IAM roles

To use AWS Batch for genomics analysis,
First, you will want to set up all of your IAM policies and roles with the following command:

```bash
aws cloudformation create-stack --stack-name iam-batch --template-body file://batch/setup/iam.template.yaml --capabilities CAPABILITY_NAMED_IAM
```

You can view the status of the stack creation like so:

```shell
aws cloudformation describe-stacks --stack-name iam-batch
```

Once the `StackStatus` is `CREATE_COMPLETE` you should see the value of several IAM role ARNs.

```shell
$ aws cloudformation describe-stacks --stack-name iam-batch --output json --query "Stacks[].Outputs[]"
[
    {
        "OutputKey": "EcsTaskRole",
        "OutputValue": "arn:aws:iam::123456789012:role/iam-batch-ecsTaskRole-1HIOGLV2TUS4S"
    },
    {
        "OutputKey": "SpotFleetRole",
        "OutputValue": "arn:aws:iam::123456789012:role/iam-batch-spotFleetRole-YU8ZBHRHQD4M"
    },
    {
        "OutputKey": "EcsInstanceRole",
        "OutputValue": "arn:aws:iam::123456789012:role/iam-batch-ecsInstanceRole-5U4YDUCEVQG7"
    },
    {
        "OutputKey": "LambdaBatchExecutionRole",
        "OutputValue": "arn:aws:iam::123456789012:role/iam-batch-lambdaBatchExecutionRole-HD21E5IYV2WU"
    },
    {
        "OutputKey": "BatchServiceRole",
        "OutputValue": "arn:aws:iam::123456789012:role/iam-batch-awsBatchServiceRole-3T98GYE3WWU1"
    }
]
```

You will need these ARNs in a later section.

### Create a custom AMI above

While you can use default Amazon ECS-optimized AMIs with AWS Batch, it is often the case for data heavy workloads like genomics that the default instance does not have enough scratch disk space for use in analysis. To overcome this, you can supply your own AMI image in AW Batch managed compute environments.

We will use this feature to provision additional scratch EBS storage on each of the instances that AWS Batch launches and also to encrypt both the Docker and scratch EBS volumes.

AWS Batch [has the same requirements for your AMI](https://docs.aws.amazon.com/batch/latest/userguide/compute_resource_AMIs.html#batch-ami-spec) as Amazon ECS. To build the custom image, modify the default [Amazon ECS-Optimized Amazon Linux AMI](https://aws.amazon.com/marketplace/fulfillment?productId=52d5fd7f-92c7-4d60-a830-41a596f4d8f3&ref_=dtl_psb_continue&region=us-east-1) in the following ways:

1. Attach a 1 TB scratch volume to `/dev/sdb`
2. Encrypt the Docker and new scratch volumes
3. Mount the scratch volume to `/docker_scratch` by modifying `/etc/fstab`

We will use the AWS Console to launch an instance and add the EBS volume like so:

<b>
<a href='https://aws.amazon.com/marketplace/fulfillment?productId=52d5fd7f-92c7-4d60-a830-41a596f4d8f3&ref_=dtl_psb_continue&region=us-east-1' target='_blank'>  [ Click here to launch ECS Optimized AMI ] </a>
</b>

![Adding a EBS volume as `/dev/sdb`](https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2017/06/01/batch_ecs_setup.png)

Once you have added the volume, SSH to the instance and issue the following commands:

```shell
sudo yum -y update
sudo yum -y install parted
sudo parted /dev/xvdb mklabel gpt
sudo parted /dev/xvdb mkpart primary 0% 100%
sudo mkfs -t ext4 /dev/xvdb1
sudo mkdir /docker_scratch
sudo echo -e '/dev/xvdb1\t/docker_scratch\text4\tdefaults\t0\t0' | sudo tee -a /etc/fstab
sudo mount -a
```

This auto-mounts your scratch volume to /docker_scratch, which is your scratch directory for batch processing.

Next, **[create your new AMI and record the image ID](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html)**.

Once the AMI is created, save the value of the AMI ID.

## Creating the AWS Batch compute environment.

We have provided a python script to configure your batch environment. While you can also do this via the CLI, the script in `batch/setup/create_batch_env.py` will do this for you.

To run the script, your will need to supply:

* the ARNs from the previous step
* A set of VPC Subnets for Batch to deploy resources to
* A set of Security Groups for your S3 and Batch resources
* The base URL for the ECR registries (e.g. for `repositoryUri` = `798375407761.dkr.ecr.us-east-1.amazonaws.com/samtools_stats` then `ECRREGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com` )

```shell
SERVICEROLE=arn:aws:iam::123456789012:role/iam-batch-awsBatchServiceRole-3T98GYE3WWU1
IAMFLEETROLE=arn:aws:iam::123456789012:role/iam-batch-spotFleetRole-YU8ZBHRHQD4M
INSTANCEROLE=arn:aws:iam::123456789012:role/iam-batch-ecsInstanceRole-5U4YDUCEVQG7
JOBROLEARN=arn:aws:iam::123456789012:role/iam-batch-ecsTaskRole-1HIOGLV2TUS4S
ECRREGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com
SUBNETS=<COMMA DELIMITED LIST OF SUBNETS>
SECGROUPS=<COMMA DELIMITED LIST OF SECURITY GROUPS>
SPOTPERCENTAGE=50
IMAGEID=<AMI ID FROM PREVIOUS STEP>
KEYNAME=<YOUR KEY NAME>
ENV=myenv
MAXCPU=160

python create_batch_env.py --service_role ${SERVICEROLE} \
    --spot_iam_fleet_role ${IAMFLEETROLE} \
    --job_role_arn ${JOBROLEARN} \
    --subnet_ids ${SUBNETS} \
    --security_group_ids ${SECGROUPS}
    --bid_percentage ${SPOTPERCENTAGE} \
    --image_id ${IMAGEID} \
    --instance_role ${INSTANCEROLE} \
    --registry ${ECRREGISTRY} \
    --key_name ${KEYNAME} \
    --max_vcpu ${MAXCPU} \
    --env ${ENV} \

```

The above limits AWS Batch to a **maximum** of 160 vCPU. You may need to set this value to more or less depending on your account limits.

The script creates your AWS Batch Environment, including a [Managed Compute Environments](http://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html), [JobQueues](http://docs.aws.amazon.com/batch/latest/userguide/job_queues.html), and [JobDefinitions](http://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) for each of our applications. If you want the details, refer to the [blog post](https://aws.amazon.com/blogs/compute/building-high-throughput-genomic-batch-workflows-on-aws-batch-layer-part-3-of-4/)

## Testing the environment

Assuming it all works, you can test the environment using the following:

```shell
aws batch submit-job --job-name testisaac --job-queue highPriority-${ENV} --job-definition isaac-${ENV}:1 --container-overrides '{
"command": [
			"--bam_s3_folder_path", "s3://mybucket/genomic-workflow/test_batch/bam/",
            "--fastq1_s3_path", "s3://aws-batch-genomics-resources/fastq/ SRR1919605_1.fastq.gz",
            "--fastq2_s3_path", "s3://aws-batch-genomics-resources/fastq/SRR1919605_2.fastq.gz",
            "--reference_s3_path", "s3://aws-batch-genomics-resources/reference/isaac/",
            "--working_dir", "/scratch",
			"—cmd_args", " --exome "]
}'
```
