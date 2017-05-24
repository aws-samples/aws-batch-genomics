from __future__ import print_function

import os
import shlex
import subprocess
from argparse import ArgumentParser

from common_utils.s3_utils import download_file, upload_file, download_folder, upload_folder
from common_utils.job_utils import generate_working_dir, delete_working_dir


def download_reference(s3_path, working_dir):
    """
    Downloads reference folder that has been configured to run with Isaac
    :param s3_path: S3 path that the folder resides in
    :param working_dir: working directory
    :return: local path to the folder containing the reference
    """

    reference_folder = os.path.join(working_dir, 'reference')

    try:
        os.mkdir(reference_folder)
    except Exception as e:
        pass

    download_folder(s3_path, reference_folder)

    # Update sorted reference
    update_sorted_reference(reference_folder)

    return reference_folder


def download_fastq_files(fastq1_s3_path, fastq2_s3_path, working_dir):
    """
    Downlodas the fastq files
    :param fastq1_s3_path: S3 path containing FASTQ with read1
    :param fastq2_s3_path: S3 path containing FASTQ with read2
    :param working_dir: working directory
    :return: local path to the folder containing the fastq
    """
    fastq_folder = os.path.join(working_dir, 'fastq')

    try:
        os.mkdir(fastq_folder)
    except Exception as e:
        pass

    local_fastq1_path = download_file(fastq1_s3_path, fastq_folder)
    local_fastq2_path = download_file(fastq2_s3_path, fastq_folder)

    # Isaac requires the fastqs to be symlinked as lane1_read1.fastq.gz and lane1_read2.fastq.gz
    os.symlink(local_fastq1_path, os.path.join(fastq_folder, 'lane1_read1.fastq.gz'))
    os.symlink(local_fastq2_path, os.path.join(fastq_folder, 'lane1_read2.fastq.gz'))

    return fastq_folder


def upload_bam(bam_s3_path, local_folder_path):
    """
    Uploads results folder containing the bam file (and associated output)
    :param bam_s3_path: S3 path to upload the alignment results to
    :param local_folder_path: local path containing the alignment results
    """

    upload_folder(bam_s3_path, local_folder_path)


def run_isaac(reference_dir, fastq_folder_path, memory, cmd_args, working_dir):
    """
    Runs Isaac3
    :param reference_dir: local path to directory containing reference
    :param fastq_folder_path: local path to directory containing fastq files
    :param memory: memory in GB
    :param cmd_args: additional command-line arguments to pass in
    :param working_dir: working directory
    :return: path to results
    """

    # Maps to Isaac's folder structure and change working directory
    os.chdir(working_dir)
    bam_folder = os.path.join(working_dir, 'Projects/default/default')

    try:
        os.mkdir(bam_folder)
    except Exception as e:
        pass

    cmd = 'isaac-align -r %s -b %s --base-calls-format fastq-gz -o %s -m %s %s' % \
          (os.path.join(reference_dir, 'sorted-reference.xml'), fastq_folder_path, working_dir, memory, cmd_args)
    print ("Running: %s" % cmd)
    subprocess.check_call(shlex.split(cmd))

    return bam_folder


def update_sorted_reference(reference_dir):
    """
    Updates sorted-reference.xml to map to the correct directory path. Since each analysis occurs in subfolder of the
    working directory, it will change each execution
    :param reference_dir: Reference directory
    """
    with open(os.path.join(reference_dir, 'sorted-reference.xml'), 'r') as infile:
        sorted_reference = infile.read()

    with open(os.path.join(reference_dir, 'sorted-reference.xml'), 'w') as outfile:
        outfile.write(sorted_reference.replace('/scratch', reference_dir))


def main():
    argparser = ArgumentParser()

    file_path_group = argparser.add_argument_group(title='File paths')
    file_path_group.add_argument('--bam_s3_folder_path', type=str, help='BAM s3 path', required=True)
    file_path_group.add_argument('--fastq1_s3_path', type=str, help='FASTQ1 s3 path', required=True)
    file_path_group.add_argument('--fastq2_s3_path', type=str, help='FASTQ2 s3  path', required=True)
    file_path_group.add_argument('--reference_s3_path', type=str, help='reference file', required=True)

    run_group = argparser.add_argument_group(title='Run command args')
    run_group.add_argument('--memory', type=str, help='Memory for Isaac in GB', default='76')
    run_group.add_argument('--cmd_args', type=str, help='Arguments for Isaac', default=' ')

    argparser.add_argument('--working_dir', type=str, default='/scratch')

    args = argparser.parse_args()

    working_dir = generate_working_dir(args.working_dir)

    # Download fastq files and reference files
    print ('Downloading FASTQs')
    fastq_folder_path = download_fastq_files(args.fastq1_s3_path, args.fastq2_s3_path, working_dir)
    print ('Downloading Reference')
    reference_folder_path = download_reference(args.reference_s3_path, working_dir)
    print ('Running Isaac')
    bam_folder_path = run_isaac(reference_folder_path, fastq_folder_path, args.memory, args.cmd_args, working_dir)
    print ('Uploading results to %s' % args.bam_s3_folder_path)
    upload_bam(args.bam_s3_folder_path, bam_folder_path)
    print('Cleaning up working dir')
    delete_working_dir(working_dir)
    print ('Completed')

if __name__ == '__main__':
    main()
