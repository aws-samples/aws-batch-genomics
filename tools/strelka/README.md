### A container to run the strelka variant caller
https://github.com/Illumina/strelka

- Reads from and writes to S3
- Handles container multitenancy with scratch directories
- Contains a lambda function for deployment to AWS Batch (ideally suited to integrate with AWS Step Functions)

#### To build the container:
- Be sure to add your specific ECR registry in `docker/Makefile`
- Run the Makefile at `docker/Makefile`

#### To run the container:
```
IMAGE=<my accountid>.dkr.ecr.us-east-1.amazonaws.com/strelka
SCRATCH=/home/ec2-user/scratch
REF=s3://mybucket/reference/hg38/hg38.fa
REFINDEX=s3://mybucket/reference/hg38/hg38.fa.fai
BAM=s3://mybucket/genomic-workflow/test_results/bam/sorted.bam
BAI=s3://mybucket/genomic-workflow/test_results/bam/sorted.bam.bai
VCF=s3://mybucket/genomic-workflow/test_results/vcf/

sudo docker run --rm -ti -v $SCRATCH:/scratch $IMAGE --bam_s3_path $BAM \
    --bai_s3_path $BAI \
    --reference_s3_path $REF \
    --reference_index_s3_path $REFINDEX \
    --vcf_s3_path $VCF \
    --working_dir /scratch

```