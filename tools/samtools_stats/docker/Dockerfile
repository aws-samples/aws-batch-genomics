FROM python:2.7

# Metadata
LABEL container.base.image="python:2.7"
LABEL software.name="SAMtools"
LABEL software.version="1.5"
LABEL software.description="Utilities for the Sequence Alignment/Map (SAM/BAM/CRAM) formats"
LABEL software.website="http://www.htslib.org"
LABEL software.documentation="http://www.htslib.org/doc/samtools.html"
LABEL software.license="MIT/Expat"
LABEL tags="Genomics"

# System and library dependencies
RUN apt-get -y update && \
    apt-get -y install unzip gcc libncurses5-dev && \
    apt-get clean

# Other software dependencies
RUN pip install boto3 awscli

# Application installation
RUN wget -O /samtools-1.5.tar.bz2 \
  https://github.com/samtools/samtools/releases/download/1.5/samtools-1.5.tar.bz2 && \
  tar xvjf /samtools-1.5.tar.bz2 && rm /samtools-1.5.tar.bz2

RUN cd /samtools-1.5 && make && make install

# Application entry point
COPY samtools_stats/src/run_samtools_stats.py /run_samtools_stats.py
COPY common_utils /common_utils

ENTRYPOINT ["python", "/run_samtools_stats.py"]
