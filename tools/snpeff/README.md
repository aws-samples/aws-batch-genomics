### A container to run snpeff to annotate VCF files
http://snpeff.sourceforge.net/index.html

- Reads from and writes to S3
- Handles container multitenancy with scratch directories
- Contains a lambda function for deployment to AWS Batch (ideally suited to integrate with AWS Step Functions)

#### To build the container:
- Be sure to add your specific ECR registry in `docker/Makefile`
- Run the Makefile at `docker/Makefile`. Be sure to pass in your `REGISTRY` keyword

#### To run the container:
```
IMAGE=<my accountid>.dkr.ecr.us-east-1.amazonaws.com/snpeff
SCRATCH=/home/ec2-user/scratch
REF=s3://mybucket/reference/hg38/hg38.fa
VCF=s3://mybucket/genomic-workflow/test_results/vcf/output.vcf
ANNO=s3://mybucket/genomic-workflow/test_results/anno/output.anno.vcf

sudo docker run --rm -ti -v $SCRATCH:/scratch $IMAGE --annotated_vcf_s3_path $ANNO \
    --vcf_s3_path $VCF \
    --cmd_args " -t hg38 " \
    --working_dir /scratch

```