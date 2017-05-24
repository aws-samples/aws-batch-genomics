from __future__ import print_function

import boto3
import json
import traceback

lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    try:
        # Generate output put
        bam_s3_path = '/'.join([event['resultsS3Path'], event['sampleId'], 'bam/'])

        depends_on = event['dependsOn'] if 'dependsOn' in event else []

        # Generate run command
        command = [
            '--bam_s3_folder_path', bam_s3_path,
            '--fastq1_s3_path', event['fastq1S3Path'],
            '--fastq2_s3_path', event['fastq2S3Path'],
            '--reference_s3_path', event['isaac']['referenceS3Path'],
            '--working_dir', event['workingDir']
        ]

        if 'cmdArgs' in event['isaac']:
            command.extend(['--cmd_args', event['isaac']['cmdArgs']])

        if 'memory' in event['isaac']:
            command.extend(['--memory', event['isaac']['memory']])

        # Submit Payload
        response = lambda_client.invoke(
            FunctionName='batchSubmitJob',
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(dict(
                dependsOn=depends_on,
                containerOverrides={
                    'command': command,
                },
                jobDefinition=event['isaac']['jobDefinition'],
                jobName='-'.join(['isaac', event['sampleId']]),
                jobQueue=event['isaac']['jobQueue']
            )))

        response_payload = response['Payload'].read()

        # Update event
        event['bamS3Path'] = bam_s3_path
        event['jobId'] = json.loads(response_payload)['jobId']

        return event
    except Exception as e:
        traceback.print_exc()
        raise e
