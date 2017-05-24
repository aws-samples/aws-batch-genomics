# This code is modified from the batch-get-job-python27 Lambda blueprint
from __future__ import print_function

import boto3
import json

print('Loading function')

batch_client = boto3.client('batch')


def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))
    # Get jobId from the event
    job_id = event['jobId']

    try:
        response = batch_client.describe_jobs(
            jobs=[job_id]
        )
        job_status = response['jobs'][0]['status']
        return job_status
    except Exception as e:
        print(e)
        message = 'Error getting Batch Job status'
        print(message)
        raise Exception(message)