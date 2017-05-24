from __future__ import print_function

import os
import shlex
import subprocess
from argparse import ArgumentParser

from common_utils.s3_utils import download_file, upload_folder
from common_utils.job_utils import generate_working_dir, delete_working_dir


def configure_germline_strelka(bam_path, reference_path, cmd_args, working_dir):
    """
    Configures strelka and creates runWorkflow.py
    :param bam_path: Local path to bam file
    :param reference_path: Local path to reference fasta
    :param cmd_args: Additional command-line arguments to pass in
    :param working_dir: Working directory
    :return: path to the workflow runner (runWorkflow.py)
    """
    cmd = 'python /strelka/bin/configureStrelkaGermlineWorkflow.py --bam %s --referenceFasta %s --runDir %s %s' % (
        bam_path, reference_path, working_dir, cmd_args)

    subprocess.check_call(shlex.split(cmd))

    return os.path.join(working_dir, 'runWorkflow.py')


def run_strelka(bam_path, reference_path, memory, cmd_args, working_dir):
    """
    Runs strelka
    :param bam_path: Local path to bam file
    :param reference_path: Local path to reference fasta
    :param memory: Memory in GB to use
    :param cmd_args: Additional command-line arguments to pass in
    :param working_dir: Working directory
    :return: path to the results directory
    """
    run_path = configure_germline_strelka(bam_path, reference_path, cmd_args, working_dir)

    cmd = 'python %s -m local -g %s' % (run_path, memory)
    subprocess.check_call(shlex.split(cmd))

    return os.path.join(working_dir, 'results/')


def main():
    argparser = ArgumentParser()

    file_path_group = argparser.add_argument_group(title='File paths')
    file_path_group.add_argument('--bam_s3_path', type=str, help='BAM s3 path', required=True)
    file_path_group.add_argument('--bai_s3_path', type=str, help='BAM Index s3 path', required=True)
    file_path_group.add_argument('--vcf_s3_path', type=str, help='VCF s3 path', required=True)
    file_path_group.add_argument('--reference_s3_path', type=str, help='Reference file s3 path', required=True)
    file_path_group.add_argument('--reference_index_s3_path', type=str, help='Reference file index s3 path',
                                 required=True)

    run_group = argparser.add_argument_group(title='Run command args')
    run_group.add_argument('--memory', type=str, help='Memory (in GB) for strelka to use', default=28)
    run_group.add_argument('--cmd_args', type=str, help='Additional arguments for platypus', default='')

    argparser.add_argument('--working_dir', type=str, default='/scratch')

    args = argparser.parse_args()

    working_dir = generate_working_dir(args.working_dir)

    print("Downloading bam")
    local_bam_path = download_file(args.bam_s3_path, working_dir)
    local_bai_path = download_file(args.bai_s3_path, working_dir)
    print("BAM and index donwloaded to %s and %s" % (local_bam_path, local_bai_path))
    print("Downloading reference")
    local_reference_path = download_file(args.reference_s3_path, working_dir)
    local_reference_index_path = download_file(args.reference_index_s3_path, working_dir)
    print("Reference downloaded to %s. Index to %s" % (local_reference_path, local_reference_index_path))
    print ("Running Strelka")
    local_vcf_path = run_strelka(local_bam_path, local_reference_path, args.memory, args.cmd_args, working_dir)
    print ("Uploading %s to %s" % (local_vcf_path, args.vcf_s3_path))
    upload_folder(args.vcf_s3_path, local_vcf_path)
    print('Cleaning up working dir')
    delete_working_dir(working_dir)
    print ("Completed")


if __name__ == '__main__':
    main()
