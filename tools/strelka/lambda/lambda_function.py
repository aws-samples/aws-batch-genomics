from __future__ import print_function

import boto3
import json
import traceback

lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    try:
        # Generate output path
        vcf_s3_path = '/'.join([event['resultsS3Path'], event['sampleId'], 'vcf'])
        bam_s3_path = event['bamS3Path']

        depends_on = event['dependsOn'] if 'dependsOn' in event else []

        # Generate run command
        command = [
            '--bam_s3_path', '/'.join([bam_s3_path.rstrip('/'), 'sorted.bam']),
            '--bai_s3_path', '/'.join([bam_s3_path.rstrip('/'), 'sorted.bam.bai']),
            '--reference_s3_path', event['referenceS3Path'],
            '--reference_index_s3_path', '%s.fai' % event['referenceS3Path'],
            '--vcf_s3_path', vcf_s3_path,
            '--working_dir', event['workingDir']
        ]

        if 'cmdArgs' in event['strelka']:
            command.extend(['--cmd_args', event['strelka']['cmdArgs']])

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
                jobDefinition=event['strelka']['jobDefinition'],
                jobName='-'.join(['strelka', event['sampleId']]),
                jobQueue=event['strelka']['jobQueue']
            )))

        response_payload = response['Payload'].read()

        # Update event
        event['vcfS3Path'] = vcf_s3_path
        event['jobId'] = json.loads(response_payload)['jobId']

        return event
    except Exception as e:
        traceback.print_exc()
        raise e
