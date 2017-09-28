FROM python:2.7

ARG VERSION="4.3p"
ARG UNDERSCORE_VERSION="4_3p"

# Metadata
LABEL container.base.image="python:2.7"
LABEL software.name="snpeff"
LABEL software.version=${VERSION}
LABEL software.description=""
LABEL software.website=""
LABEL software.documentation=""
LABEL software.license=""
LABEL tags="Genomics"

# System and library dependencies
RUN apt-get -y update && \
    apt-get -y install default-jre unzip && \
    apt-get clean

# Other software dependencies
RUN pip install boto3 awscli

# Application installation
RUN wget -O /snpeff.zip https://downloads.sourceforge.net/project/snpeff/snpEff_v${UNDERSCORE_VERSION}_core.zip && \
    unzip /snpeff.zip && rm /snpeff.zip

RUN java -jar /snpEff/snpEff.jar download hg38

# Application entry point
COPY snpeff/src/run_snpeff.py /run_snpeff.py
COPY common_utils /common_utils

ENTRYPOINT ["python", "/run_snpeff.py"]
