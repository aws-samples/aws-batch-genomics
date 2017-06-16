NAME=isaac
TAG=03.17.03.01

all: build push

build:
	docker build -t $(NAME):$(TAG) -t $(NAME):latest -f Dockerfile ../..
	docker tag $(NAME):latest $(REGISTRY):latest
	docker tag $(NAME):$(TAG) $(REGISTRY):$(TAG)

push:
	docker push $(REGISTRY):$(TAG)
	docker push $(REGISTRY):latest

reference:
	wget --timestamping 'ftp://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz' -O $(WORKDIR)/hg38.fa.gz
	gzip -d $(WORKDIR)/hg38.fa.gz
	docker run --rm -ti -v $(WORKDIR):/scratch --entrypoint=isaac-sort-reference $(REGISTRY):$(TAG) -g /scratch/hg38.fa -o /scratch
