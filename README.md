# Package and deploy a bioinformatics workflow on AWS using AWS Step Functions and AWS Batch

This tutorial will cover the material presented within the "Building High-Throughput Genomics Batch Workflows on AWS" blog post series

* [Introduction (Part 1 of 4)](https://aws.amazon.com/blogs/compute/building-high-throughput-genomics-batch-workflows-on-aws-introduction-part-1-of-4/)
* [The Job Layer (Part 2 of 4)](https://aws.amazon.com/blogs/compute/building-high-throughput-genomics-batch-workflows-on-aws-job-layer-part-2-of-4/)
* [The Batch Layer (Part 3 of 4)](https://aws.amazon.com/blogs/compute/building-high-throughput-genomic-batch-workflows-on-aws-batch-layer-part-3-of-4/)
* [The Workflow Layer (Part 4 of 4)](https://aws.amazon.com/blogs/compute/building-high-throughput-genomics-batch-workflows-on-aws-workflow-layer-part-4-of-4/)

These posts cover the basics of bootstrapping a bioinformatics analysis pipeline on AWS. We break down the tutorial roughly as follows:

1. [Setting up your AWS account](./doc/00-account-setup.md) (if you do not already have one)
2. [Package a set of bioinformatics applications using Docker](./doc/01-creating-docker-images.md)
3. [Create a AWS Batch environment for analysis](./doc/02-creating-batch-env.md)
4. [Creating AWS Lambda Functions] for each application
5. [Creating AWS  Step Functions](./doc/04-creating-step-functions.md) to control the data processing steps
5. [Initiate a workflow](./doc/05-initiate-worflow.md)
