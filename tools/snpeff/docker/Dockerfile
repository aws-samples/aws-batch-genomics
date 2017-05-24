FROM python:2.7

# Metadata
LABEL container.base.image="python:2.7"
LABEL software.name="snpeff"
LABEL software.version="4.3"
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
RUN wget -O /snpeff.zip https://sourceforge.net/projects/snpeff/files/snpEff_v4_3i_core.zip && \
    unzip /snpeff.zip && rm /snpeff.zip

RUN java -jar /snpEff/snpEff.jar download hg38

# Application entry point
COPY snpeff/src/run_snpeff.py /run_snpeff.py
COPY common_utils /common_utils

ENTRYPOINT ["python", "/run_snpeff.py"]
