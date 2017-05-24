#!/usr/bin/env bash

ENV=demo

#aws batch deregister-job-definition --job-definition arn:aws:batch:us-east-1:037062425811:job-definition/snap-${ENV}:1
#aws batch deregister-job-definition --job-definition arn:aws:batch:us-east-1:037062425811:job-definition/platypus-${ENV}:1
#aws batch deregister-job-definition --job-definition arn:aws:batch:us-east-1:037062425811:job-definition/snpeff-${ENV}:1
#aws batch deregister-job-definition --job-definition arn:aws:batch:us-east-1:037062425811:job-definition/samtools_stats-${ENV}:1

for jobQueue in alignment variantCalling otherGenomic
do
    aws batch update-job-queue --job-queue ${jobQueue}-${ENV} --state DISABLED
    sleep 20
    aws batch delete-job-queue --job-queue ${jobQueue}-${ENV}
done
sleep 20
for CE in MemXL-CompXL MemL-CompXL
do
    aws batch update-compute-environment --compute-environment ${CE}-${ENV} --state DISABLED
    sleep 20
    aws batch delete-compute-environment --compute-environment ${CE}-${ENV}
done
