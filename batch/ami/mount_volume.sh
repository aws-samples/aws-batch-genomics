#!/usr/bin/env bash

sudo yum -y update
sudo parted /dev/xvdb mklabel gpt
sudo parted /dev/xvdb mkpart primary 0% 100%
sudo mkfs -t ext4 /dev/xvdb1
sudo mkdir /docker_scratch
sudo echo -e '/dev/xvdb1\t/docker_scratch\text4\tdefaults\t0\t0' | sudo tee -a /etc/fstab
sudo mount -a