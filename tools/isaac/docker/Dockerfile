FROM python:2.7

# Metadata
LABEL container.base.image="python:2.7"
LABEL software.name="iSAAC"
LABEL software.version="03.17.03.01"
LABEL software.description="Aligner for sequencing data"
LABEL software.website="https://github.com/Illumina/Isaac3"
LABEL software.documentation="https://github.com/Illumina/Isaac3/blob/master/src/markdown/manual.md"
LABEL software.license="GPLv3"
LABEL tags="Genomics"

RUN apt-get -y update && \
    apt-get -y install zlib1g-dev gnuplot && \
    apt-get clean

RUN pip install boto3 awscli

RUN git clone https://github.com/Illumina/Isaac3.git && cd /Isaac3 && git checkout 6f0191a4e0d4b332e8f34b7ced57dc6e6eb4f2f1
RUN mkdir /iSAAC-build /isaac
WORKDIR /iSAAC-build
RUN /Isaac3/src/configure --prefix=/isaac && \
 make && \
 make install && \
 cd / && \
 rm -rf /Isaac3 /iSAAC-build

RUN chmod -R +x /isaac/bin/

ENV PATH="/isaac/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/lib:/usr/lib:/isaac/libexec:${LD_LIBRARY_PATH}"

COPY isaac/src/run_isaac.py /
COPY common_utils /common_utils

ENTRYPOINT ["python", "/run_isaac.py"]
