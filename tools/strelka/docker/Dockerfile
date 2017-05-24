# https://github.com/Illumina/strelka/blob/master/docs/userGuide/installation.md

FROM python:2.7

LABEL container.base.image="python:2.7"
LABEL software.name="Strelka"
LABEL software.version="2.7.1"
LABEL software.description="Somatic and germline small variant caller for mapped sequencing data"
LABEL software.website="https://github.com/Illumina/strelka"
LABEL software.documentation="https://github.com/Illumina/strelka/blob/master/docs/userGuide/README.md"
LABEL software.license="GPLv3"
LABEL tags="Genomics"

RUN apt-get -y update && \
    apt-get -y install zlib1g-dev wget && \
    apt-get clean

RUN pip install boto3 awscli

RUN wget https://github.com/Illumina/strelka/releases/download/v2.7.1/strelka-2.7.1.centos5_x86_64.tar.bz2 \
    -O strelka-2.7.1.centos5_x86_64.tar.bz2 && tar xvjf strelka-2.7.1.centos5_x86_64.tar.bz2 && \
    rm strelka-2.7.1.centos5_x86_64.tar.bz2 && mv strelka-2.7.1.centos5_x86_64 strelka

ENV LD_LIBRARY_PATH="/strelka/lib:/usr/local/lib:/usr/lib:${LD_LIBRARY_PATH}"
ENV PATH="/strelka/bin:$PATH"

COPY strelka/src/run_strelka.py .
COPY common_utils common_utils

ENTRYPOINT ["python", "/run_strelka.py"]