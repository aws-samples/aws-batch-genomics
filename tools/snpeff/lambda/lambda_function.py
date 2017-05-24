from __future__ import print_function

import boto3
import json
import traceback

lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    try:
        # Create output path
        annotated_vcf_s3_path = '/'.join([
            event['resultsS3Path'], event['sampleId'], 'annotated_vcf', 'output.annotated.vcf'])

        vcf_s3_path = '/'.join([event['vcfS3Path'], 'variants', 'variants.vcf.gz'])

        depends_on = event['dependsOn'] if 'dependsOn' in event else []

        # Generate run command
        command = [
            '--vcf_s3_path', vcf_s3_path,
            '--annotated_vcf_s3_path', annotated_vcf_s3_path,
            '--working_dir', event['workingDir']
        ]

        if 'cmdArgs' in event['snpEff']:
            command.extend(['--cmd_args', event['snpEff']['cmdArgs']])

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
                jobDefinition=event['snpEff']['jobDefinition'],
                jobName='-'.join(['snpEff', event['sampleId']]),
                jobQueue=event['snpEff']['jobQueue']
            )))

        response_payload = response['Payload'].read()

        # Update event
        event['annotatedVcfS3Path'] = annotated_vcf_s3_path
        event['jobId'] = json.loads(response_payload)['jobId']

        return event
    except Exception as e:
        traceback.print_exc()
        raise e
