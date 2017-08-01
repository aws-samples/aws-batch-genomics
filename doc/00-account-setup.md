
# Initial Setup

There are a couple of pre-requisites for this tutorial. Specifically, you need a AWS account and access to a Unix-like development environment to work with the AWS CLI and Docker tools. You can either choose to launch a EC2 instance to develop on, or set up your local machine's development environment.

## Docker development environment

You will need to be able to work with the [Docker](https://www.docker.com/) tools to create the necessary machine images for applications such as [samtools](http://www.htslib.org/). You can refer to the Docker [getting started](https://www.docker.com/community-edition) guides to service this requirement.

Once you have Docker Community Edition running, you should be able to test the installation by issuing the following command and output. New installs should not have any images registered.

```bash
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
$
```

## AWS Development Environment

You will need to have a AWS account in order to do the exercise. You will also need a development environment for working with the [AWS Command Line Interface](https://aws.amazon.com/cli/).

If you are want to dive right into this tutorial, then just follow the [installation instructions for the CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) and test it using the  command `aws ec2 describe-instances`. The output should look like the following:

```bash
$ aws ec2 describe-instances
{
    "Reservations": []
}
```

If you are completely new to AWS, then you may want to follow a couple of introductory exercises to get your feet wet with AWS. We recommend:

* [Launch a Linux Virtual Machine with Amazon EC2](https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/)
* ["Backup Files to Amazon S3 using the AWS CLI"](https://aws.amazon.com/getting-started/tutorials/backup-to-s3-cli/)

Both exercises are only 10 minutes long, and will introduce you to the AWS web console and AWS CLI. 
