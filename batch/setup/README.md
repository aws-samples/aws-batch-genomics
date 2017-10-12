## Creates the AWS Batch environment to run your jobs

We have provided two different ways to set up your core environment. You can use either the provided python script `create_bash_env.py` or use the CloudFormation template `batch_env.template.yaml`. Below, see examples for each.

_N.B. Be sure to replace the following with your specific ARNs, IDs, etc_

### Set up with CloudFormation (recommended as of 8/12/17)
```bash
ACCOUNTID=<your account ID>
REGION=<your region>
SERVICEROLE=arn:aws:iam::${ACCOUNTID}:role/service-role/AWSBatchServiceRole
IAMFLEETROLE=arn:aws:iam::${ACCOUNTID}:role/aws-ec2-spot-fleet-role
INSTANCEROLE=arn:aws:iam::${ACCOUNTID}:role/ecsInstanceRole
JOBROLEARN=arn:aws:iam::${ACCOUNTID}:role/ecsTaskRole

SUBNETS=<comma delimited list of subnets>
SECGROUPS=<comma delimited list of security groups>
SPOTPER=50
IMAGEID=ami-123d5b43
KEYPNAME=<your-key-name>
MINCPU=0
MAXCPU=1024
DESIREDCPU=0
RETRIES=1

REGISTRY=${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com
ISAACIMAGE=${REGISTRY}/isaac
ISAACCPU=32
ISAACMEM=80000
STRELKAIMAGE=${REGISTRY}/strelka
STRELKACPU=32
STRELKAMEM=32000
SNPEFFIMAGE=${REGISTRY}/snpeff
SNPEFFCPU=4
SNPEFFMEM=10000
SAMTOOLSIMAGE=${REGISTRY}/samtools_stats
SAMTOOLSCPU=4
SAMTOOLSMEM=10000

ENV=myenv

# Be sure to escape SubnetIds and SecurityGroupIds as they require a basestring and not a list
aws cloudformation create-stack --stack-name batch-genomics --template-body file://batch_env.template.yaml --parameters \
ParameterKey=BatchServiceRole,ParameterValue=${SERVICEROLE} \
ParameterKey=SpotIamFleetRole,ParameterValue=${IAMFLEETROLE} \
ParameterKey=InstanceRole,ParameterValue=${INSTANCEROLE} \
ParameterKey=JobRoleArn,ParameterValue=${JOBROLEARN} \
ParameterKey=SubnetIds,ParameterValue=\"${SUBNETS}\" \
ParameterKey=SecurityGroupIds,ParameterValue=\"${SECGROUPS}\" \
ParameterKey=BidPercentage,ParameterValue=${SPOTPER} \
ParameterKey=ImageId,ParameterValue=${IMAGEID} \
ParameterKey=KeyPair,ParameterValue=${KEYNAME} \
ParameterKey=MinvCpus,ParameterValue=${MINCPU} \
ParameterKey=DesiredvCpus,ParameterValue=${DESIREDCPU} \
ParameterKey=MaxvCpus,ParameterValue=${MAXCPU} \
ParameterKey=Env,ParameterValue=${ENV} \
ParameterKey=RetryNumber,ParameterValue=${RETRIES} \
ParameterKey=IsaacDockerImage,ParameterValue=${ISAACIMAGE} \
ParameterKey=IsaacVcpus,ParameterValue=${ISAACCPU} \
ParameterKey=IsaacMemory,ParameterValue=${ISAACMEM} \
ParameterKey=StrelkaDockerImage,ParameterValue=${STRELKAIMAGE} \
ParameterKey=StrelkaVcpus,ParameterValue=${STRELKACPU} \
ParameterKey=StrelkaMemory,ParameterValue=${STRELKAMEM} \
ParameterKey=SnpEffDockerImage,ParameterValue=${SNPEFFIMAGE} \
ParameterKey=SnpEffVcpus,ParameterValue=${SNPEFFCPU} \
ParameterKey=SnpEffMemory,ParameterValue=${SNPEFFMEM} \
ParameterKey=SamtoolsStatsDockerImage,ParameterValue=${SAMTOOLSIMAGE} \
ParameterKey=SamtoolsStatsVcpus,ParameterValue=${SAMTOOLSCPU} \
ParameterKey=SamtoolsStatsMemory,ParameterValue=${SAMTOOLSMEM}

```

### Set up with python script (as in the blog series)
```bash
ACCOUNTID=<your account ID>
SERVICEROLE=arn:aws:iam::${ACCOUNTID}:role/service-role/AWSBatchServiceRole
IAMFLEETROLE=arn:aws:iam::${ACCOUNTID}:role/aws-ec2-spot-fleet-role
JOBROLEARN=arn:aws:iam::${ACCOUNTID}:role/ecsTaskRole
SUBNETS=<comma delimited list of subnets>
SECGROUPS=<comma delimited list of security groups>
SPOTPER=50
IMAGEID=ami-123d5b43
INSTANCEROLE=arn:aws:iam::${ACCOUNTID}:role/ecsInstanceRole
REGISTRY=${ACCOUNTID}.dkr.ecr.us-east-1.amazonaws.com
KEYNAME=<your-key-name>
ENV=myenv
MAXCPU=1024

python create_batch_env.py --service_role ${SERVICEROLE} \
    --spot_iam_fleet_role ${IAMFLEETROLE} \
    --job_role_arn ${JOBROLEARN} \
    --subnet_ids ${SUBNETS} \
    --security_group_ids ${SECGROUPS}
    --bid_percentage ${SPOTPER} \
    --image_id ${IMAGEID} \
    --instance_role ${INSTANCEROLE} \
    --registry ${REGISTRY} \
    --key_name ${KEYNAME} \
    --max_vcpu ${MAXCPU} \
    --env ${ENV} \

```
