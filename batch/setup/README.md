### Creates the AWS Batch environment to run your jobs

To run:
```
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
