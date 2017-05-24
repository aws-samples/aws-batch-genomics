### A container to run the Isaac genome aligner
https://github.com/Illumina/Isaac3

- Reads from and writes to S3
- Handles container multitenancy with scratch directories
- Contains a lambda function for deployment to AWS Batch (ideally suited to integrate with AWS Step Functions)

#### To build the container:
- Be sure to add your specific ECR registry in `docker/Makefile`
- Run the Makefile at `docker/Makefile`

#### Generating the reference:
- If you wish to generate yourself, please reference https://github.com/Illumina/Isaac3/blob/master/src/markdown/manual.md in the sorted reference for compute/memory requirements.
- Once the container is built, you can use `make reference REGISTRY=<your registry>` to generate the reference

#### To run the container:
N.B. If running on an EC2 instance, specify `-m 80` to ensure Isaac doesn't take too much memory
```
# To run on an EC2 instance
IMAGE=<my accountid>.dkr.ecr.us-east-1.amazonaws.com/isaac
SCRATCH=/home/ec2-user/scratch
FASTQ1=s3://mybucket/genomic-workflow/fastq/SRR1919605_1.fastq.gz
FASTQ2=s3://mybucket/genomic-workflow/fastq/SRR1919605_2.fastq.gz
REF=s3://mybucket/reference/hg38/isaac/
BAM=s3://mybucket/genomic-workflow/test_results/bam/


sudo docker run --rm -ti -v $SCRATCH:/scratch $IMAGE --bam_s3_folder_path $BAM \
    --fastq1_s3_path $FASTQ1 \
    --fastq2_s3_path $FASTQ2 \
    --reference_s3_path $REF \
    --working_dir /scratch
    --cmd_args " -m 80 "
```