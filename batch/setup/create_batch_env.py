from __future__ import print_function
import boto3
import time
from argparse import ArgumentParser

batch_client = boto3.client('batch')


def create_compute_environments(env, service_role, bid_percentage, image_id, instance_role, key_name, max_vcpus,
                                security_group_ids, spot_iam_fleet_role, subnet_ids):
    """
    Creates managed compute environments for the different parts of the batch workflow
    :param env: Environment you are running in (e.g. dev, test, prod)
    :param service_role: Batch service role
    :param bid_percentage: Percent of on-demand for your spot instance bid
    :param image_id: AMI to be used for the compute environments
    :param instance_role: Batch instance role
    :param key_name: Key for instances in the compute environments
    :param max_vcpus: Max vCPUs in the compute environments
    :param security_group_ids: Security Group IDs for batch to run in
    :param spot_iam_fleet_role: IAM Role ARN for Spot Fleet
    :param subnet_ids: List of subnet IDs for batch environment to run in
    :return: Dictionary, Response from the CreateComptueEnvironment API Call.
             If already created, just returns a dictionary of the CE name
    """
    compute_environments = ['genomicsEnv']
    try:
        return [
            batch_client.create_compute_environment(
                computeEnvironmentName='-'.join([compute_environment_name, env]),
                serviceRole=service_role,
                type='MANAGED',
                state='ENABLED',
                computeResources=dict(
                    bidPercentage=bid_percentage,
                    ec2KeyPair=key_name,
                    imageId=image_id,
                    instanceRole=instance_role,
                    instanceTypes=['optimal'],
                    maxvCpus=max_vcpus,
                    minvCpus=0,
                    securityGroupIds=security_group_ids,
                    spotIamFleetRole=spot_iam_fleet_role,
                    subnets=subnet_ids,
                    type='SPOT'
                )
            ) for compute_environment_name in compute_environments
        ]
    except Exception as e:
        print (e)
        return [{'computeEnvironmentName': _} for _ in compute_environments]


def create_job_queues(env):
    """
    Creates the appropriate job queues
    :param env: String, Name of the environment (e.g. dev, demo, test)
    :return: List, Responses from the CreateJobQueue API Call
    """
    job_queue_responses = list()
    # Alignment and Variant Calling
    job_queue_responses.append(create_job_queue('highPriority-%s' % env, ['genomicsEnv-%s' % env], 1000))
    # Other (such as variant annotation)
    job_queue_responses.append(create_job_queue('lowPriority-%s' % env, ['genomicsEnv-%s' % env], 1))


def create_job_queue(job_queue_name, compute_environments, priority):
    """
    Creates a job queue
    :param job_queue_name: String, Name of job queue
    :param compute_environments: String, Order of compute environments for the job queue
    :param priority: Integer, Priority of the job queue
    :return: response from the CreateJobQueue API
    """
    # Create order of compute environments
    compute_environment_order = [{
        'computeEnvironment': compute_environment,
        'order': i
    } for i, compute_environment in enumerate(compute_environments)]
    response = batch_client.create_job_queue(
        computeEnvironmentOrder=compute_environment_order,
        jobQueueName=job_queue_name,
        priority=priority,
        state='ENABLED'
    )
    return response


def register_isaac(image, job_role_arn, retry_number, env):
    """
    Registers a job definition for the snap aligner
    :param image: Docker image
    :param job_role_arn: Job Role Arn
    :param retry_number: Number of retries
    :param env: String, Name of the environment (e.g. dev, demo, test)
    :return: response from the RegisterJobDefinition API
    """
    response = batch_client.register_job_definition(
        containerProperties={
            'image': image,
            'jobRoleArn': job_role_arn,
            'memory': 80000,
            'mountPoints': [
                {
                    'containerPath': '/scratch',
                    'readOnly': False,
                    'sourceVolume': 'docker_scratch'
                }
            ],
            'volumes': [{
                'name': 'docker_scratch',
                'host': {
                    'sourcePath': '/docker_scratch'
                }
            }],
            'vcpus': 32
        },
        retryStrategy={'attempts': retry_number},
        jobDefinitionName='isaac-%s' % env,
        type='container'
    )
    return response


def register_strelka(image, job_role_arn, retry_number, env):
    """
    Registers a job definition for the platypus variant caller
    :param image: Docker image
    :param job_role_arn: Job Role Arn
    :param retry_number: Number of retries
    :param env: String, Name of the environment (e.g. dev, demo, test)
    :return: response from the RegisterJobDefinition API
    """
    response = batch_client.register_job_definition(
        containerProperties={
            'image': image,
            'jobRoleArn': job_role_arn,
            'memory': 32000,
            'mountPoints': [
                {
                    'containerPath': '/scratch',
                    'readOnly': False,
                    'sourceVolume': 'docker_scratch'
                }
            ],
            'volumes': [{
                'name': 'docker_scratch',
                'host': {
                    'sourcePath': '/docker_scratch'
                }
            }],
            'vcpus': 32
        },
        retryStrategy={'attempts': retry_number},
        jobDefinitionName='strelka-%s' % env,
        type='container'
    )
    return response


def register_snpeff(image, job_role_arn, retry_number, env):
    """
    Registers a job definition for snpeff (variant annotator)
    :param image: Docker image
    :param job_role_arn: Job Role Arn
    :param retry_number: Number of retries
    :param env: String, Name of the environment (e.g. dev, demo, test)
    :return: response from the RegisterJobDefinition API
    """
    response = batch_client.register_job_definition(
        containerProperties={
            'image': image,
            'jobRoleArn': job_role_arn,
            'memory': 10000,
            'mountPoints': [
                {
                    'containerPath': '/scratch',
                    'readOnly': False,
                    'sourceVolume': 'docker_scratch'
                }
            ],
            'volumes': [{
                'name': 'docker_scratch',
                'host': {
                    'sourcePath': '/docker_scratch'
                }
            }],
            'vcpus': 4
        },
        retryStrategy={'attempts': retry_number},
        jobDefinitionName='snpeff-%s' % env,
        type='container'
    )
    return response


def register_samtools_stats(image, job_role_arn, retry_number, env):
    """
    Registers a job definition for the samtools statistics from BAM
    :param image: Docker image
    :param job_role_arn: Job Role Arn
    :param retry_number: Number of retries
    :param env: String, Name of the environment (e.g. dev, demo, test)
    :return: response from the RegisterJobDefinition API
    """
    response = batch_client.register_job_definition(
        containerProperties={
            'image': image,
            'jobRoleArn': job_role_arn,
            'memory': 10000,
            'mountPoints': [
                {
                    'containerPath': '/scratch',
                    'readOnly': False,
                    'sourceVolume': 'docker_scratch'
                }
            ],
            'volumes': [{
                'name': 'docker_scratch',
                'host': {
                    'sourcePath': '/docker_scratch'
                }
            }],
            'vcpus': 4
        },
        retryStrategy={'attempts': retry_number},
        jobDefinitionName='samtools_stats-%s' % env,
        type='container'
    )
    return response


def main():
    argparser = ArgumentParser()

    iam_group = argparser.add_argument_group(title='iam')
    iam_group.add_argument('--service_role', type=str, help='Batch Service Role', required=True)
    iam_group.add_argument('--spot_iam_fleet_role', type=str, help='Spot Fleet ARN', required=True)
    iam_group.add_argument('--job_role_arn', type=str, help='Job Role ARN the container can assume', required=True)

    ce_group = argparser.add_argument_group(title='compute environment resources')
    ce_group.add_argument('--subnet_ids', type=str,
                           help='Subnet IDs for Compute Environment to run in. Comma delimited.', required=True)
    ce_group.add_argument('--security_group_ids', type=str,
                           help='Security Group IDs for Compute Environment. Comma delimited.', required=True)
    ce_group.add_argument('--bid_percentage', type=int, help='Maximum spot percent of on-demand', default=100)
    ce_group.add_argument('--image_id', type=str, help='AMI you want your batch instances to use', required=True)
    ce_group.add_argument('--instance_role', type=str, help='Instance Role ARN  to use', required=True)
    ce_group.add_argument('--registry', type=str, help='Docker registry your images reside in', required=True)
    ce_group.add_argument('--key_name', type=str, help='Compute Environment Key Name', required=True)
    ce_group.add_argument('--max_vcpus', type=int, help='Max vCPUs for your CE to scale to', required=True)
    ce_group.add_argument('--env', type=str, help='Environment you are running in (e.g. Dev or Prod)', required=True)

    argparser.add_argument('--retry_number', type=int, help='Number of retries', default=3)

    args = argparser.parse_args()

    print ('Creating Compute Environments')
    compute_env_responses = create_compute_environments(args.env, args.service_role, args.bid_percentage, args.image_id,
                                                        args.instance_role, args.key_name, args.max_vcpus,
                                                        args.security_group_ids.split(','), args.spot_iam_fleet_role,
                                                        args.subnet_ids.split(','))

    print (compute_env_responses)
    # Wait 60 sec to ensure CEs are appropriately created
    time.sleep(60)

    print ('Creating Job Queues')
    job_queue_responses = create_job_queues(args.env)
    print (job_queue_responses)

    print ('Registering Isaac')
    isaac_response = register_isaac('/'.join([args.registry, 'isaac']), args.job_role_arn, args.retry_number,
                                    args.env)
    print (isaac_response)

    print ('Registering Strelka')
    strelka_response = register_strelka('/'.join([args.registry, 'strelka']), args.job_role_arn, args.retry_number,
                                        args.env)
    print (strelka_response)

    print ('Registering snpEff')
    snpeff_response = register_snpeff('/'.join([args.registry, 'snpeff']), args.job_role_arn, args.retry_number,
                                      args.env)
    print (snpeff_response)

    print ('Registering samtools stats')
    samtools_response = register_samtools_stats('/'.join([args.registry, 'samtools_stats']), args.job_role_arn,
                                                args.retry_number, args.env)
    print (samtools_response)

    print ('Finished setting up Batch Environments')


if __name__ == "__main__":
    main()
