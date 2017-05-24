from __future__ import print_function

import boto3
import json
import traceback

lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    try:
        # Create output path
        stats_s3_path = '/'.join([event['resultsS3Path'], event['sampleId'], 'stats', 'bam_stats.dat'])
        bam_s3_path = event['bamS3Path']

        # Create inpute path
        if bam_s3_path[-1] == '/':
            bam_s3_path += 'sorted.bam'

        depends_on = event['dependsOn'] if 'dependsOn' in event else []

        # Generate run command
        command = [
            '--bam_s3_path', bam_s3_path,
            '--reference_s3_path', event['referenceS3Path'],
            '--bam_stats_s3_path', stats_s3_path,
            '--working_dir', event['workingDir']
        ]

        if 'cmdArgs' in event['samtoolsStats']:
            command.extend(['--cmd_args', event['samtoolsStats']['cmdArgs']])

        # Submit payload
        response = lambda_client.invoke(
            FunctionName='batchSubmitJob',
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(dict(
                dependsOn=depends_on,
                containerOverrides={
                    'command': command
                },
                jobDefinition=event['samtoolsStats']['jobDefinition'],
                jobName='-'.join(['samtoolsStats', event['sampleId']]),
                jobQueue=event['samtoolsStats']['jobQueue']
            )))
        response_payload = response['Payload'].read()

        # Update event
        event['bamStatsS3Path'] = stats_s3_path
        event['jobId'] = json.loads(response_payload)['jobId']

        return event
    except Exception as e:
        traceback.print_exc()
        raise e
