# This code is modified from the batch-submit-job-python27 Lambda blueprint
from __future__ import print_function

import json
import boto3

batch_client = boto3.client('batch')


def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))
    # Get parameters for the SubmitJob call
    # http://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html
    job_name = event['jobName']
    job_queue = event['jobQueue']
    job_definition = event['jobDefinition']

    # containerOverrides, dependsOn, and parameters are optional
    container_overrides = event['containerOverrides'] if event.get('containerOverrides') else {}
    parameters = event['parameters'] if event.get('parameters') else {}
    depends_on = event['dependsOn'] if event.get('dependsOn') else []

    try:
        response = batch_client.submit_job(
            dependsOn=depends_on,
            containerOverrides=container_overrides,
            jobDefinition=job_definition,
            jobName=job_name,
            jobQueue=job_queue,
            parameters=parameters
        )
        # Log response from AWS Batch
        print("Response: " + json.dumps(response, indent=2))
        # Return the jobId
        event['jobId'] = response['jobId']
        return event
    except Exception as e:
        print(e)
        message = 'Error getting Batch Job status'
        print(message)
        raise Exception(message)

