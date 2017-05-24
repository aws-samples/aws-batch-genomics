from __future__ import print_function

import os
import shlex
import subprocess
from argparse import ArgumentParser

from common_utils.s3_utils import download_file, upload_file
from common_utils.job_utils import generate_working_dir, delete_working_dir


def run_snpeff(in_vcf_path, cmd_args, working_dir):
    """
    Runs snpEff
    :param in_vcf_path: Local path to vcf file
    :param cmd_args: Additional command-line arguments to pass in
    :param working_dir: Working directory
    :return: path to the output vcf (annotated_vcf_path)
    """
    annotated_vcf_path = os.path.join(working_dir, 'annotated.vcf')

    cmd = 'java -Xmx4g -jar /snpEff/snpEff.jar -c /snpEff/snpEff.config %s %s' % (cmd_args, in_vcf_path)

    print(cmd)
    with open(annotated_vcf_path, 'w') as out_file:
        subprocess.check_call(shlex.split(cmd), stdout=out_file)

    return annotated_vcf_path


def main():
    argparser = ArgumentParser()

    argparser.add_argument('--vcf_s3_path', type=str, help='VCF s3 path', required=True)
    argparser.add_argument('--annotated_vcf_s3_path', type=str, help='Annotated vcf s3 path', required=True)
    argparser.add_argument('--working_dir', type=str, default='/scratch')
    argparser.add_argument('--cmd_args', type=str, help='arguments/options for snpeff', default='-t')

    args = argparser.parse_args()

    working_dir = generate_working_dir(args.working_dir)

    print ('Downloading vcf')
    local_vcf_path = download_file(args.vcf_s3_path, working_dir)
    print ('Running snpeff')
    annotated_vcf_path = run_snpeff(local_vcf_path, args.cmd_args, working_dir)
    print ('Uploading %s to %s' % (annotated_vcf_path, args.annotated_vcf_s3_path))
    upload_file(args.annotated_vcf_s3_path, annotated_vcf_path)
    print ('Cleaning up working dir')
    delete_working_dir(working_dir)
    print ('Completed')


if __name__ == '__main__':
    main()
