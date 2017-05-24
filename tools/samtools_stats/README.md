### A container to run samtools to generate BAM statistics
http://www.htslib.org/doc/samtools.html

- Reads from and writes to S3
- Handles container multitenancy with scratch directories
- Contains a lambda function for deployment to AWS Batch (ideally suited to integrate with AWS Step Functions)

#### To build the container:
- Be sure to add your specific ECR registry in `docker/Makefile`
- Run the Makefile at `docker/Makefile`

#### To run the container:
```

IMAGE=<my accountid>.dkr.ecr.us-east-1.amazonaws.com/samtools_stats
SCRATCH=/home/ec2-user/scratch
REF=s3://mybucket/reference/hg38/hg38.fa
BAM=s3://mybucket/genomic-workflow/test_results/bam/output.bam
STATS=s3://mybucket/genomic-workflow/test_results/bam/output.bam.stats

sudo docker run --rm -ti -v $SCRATCH:/scratch $IMAGE --bam_s3_path $BAM \
    --bam_stats_s3_path $STATS \
    --reference_s3_path $REF \
    --working_dir /scratch

```