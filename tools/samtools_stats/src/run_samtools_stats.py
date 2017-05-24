from __future__ import print_function

import os
import shlex
import subprocess
from argparse import ArgumentParser

from common_utils.s3_utils import download_file, upload_file
from common_utils.job_utils import generate_working_dir, delete_working_dir


def run_samtools_stats(bam_path, reference_path, cmd_args, working_dir):
    """
    Runs samtools stats package
    :param bam_path: Local path to bam file
    :param reference_path: Local path to reference file
    :param cmd_args: Additional command-line arguments to pass in
    :param working_dir: Working directory
    :return: path to the output (stats_path)
    """
    stats_path = os.path.join(working_dir, 'sequencing_stats.txt')

    cmd = 'samtools stats %s --reference %s %s' % (cmd_args, reference_path, bam_path)

    with open(stats_path, 'w') as out_file:
        subprocess.check_call(shlex.split(cmd), stdout=out_file)

    return stats_path


def main():
    argparser = ArgumentParser()

    file_path_group = argparser.add_argument_group(title='File paths')
    file_path_group.add_argument('--bam_s3_path', type=str, help='BAM s3 path', required=True)
    file_path_group.add_argument('--reference_s3_path', type=str, help='reference file', required=True)
    file_path_group.add_argument('--bam_stats_s3_path', type=str, help='S3 Path to upload stats', required=True)

    run_group = argparser.add_argument_group(title='Run command args')
    run_group.add_argument('--cmd_args', type=str, help='Arguments for platypus', default='')

    argparser.add_argument('--working_dir', type=str, default='/scratch')

    args = argparser.parse_args()

    working_dir = generate_working_dir(args.working_dir)

    print("Downloading bam")
    local_bam_path = download_file(args.bam_s3_path, working_dir)
    print("BAM downloaded to %s" % local_bam_path)
    print("Downloading reference")
    local_reference_path = download_file(args.reference_s3_path, working_dir)
    print("Reference downloaded to %s." % local_reference_path)
    print ("Running samtools stats")
    local_stats_path = run_samtools_stats(local_bam_path, local_reference_path, args.cmd_args, working_dir)
    print ("Uploading %s to %s" % (local_stats_path, args.bam_stats_s3_path))
    upload_file(args.bam_stats_s3_path, local_stats_path)
    print('Cleaning up working dir')
    delete_working_dir(working_dir)
    print ("Completed")


if __name__ == '__main__':
    main()
