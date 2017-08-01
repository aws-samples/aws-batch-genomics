NAME=samtools_stats
TAG=1.5

all: build tag push

build:
	docker build -t $(NAME):latest -f Dockerfile ../..

tag:
	docker tag $(NAME):latest $(NAME):$(TAG)
	docker tag $(NAME):latest $(REGISTRY):latest
	docker tag $(NAME):latest $(REGISTRY):$(TAG)

push:
	docker push $(REGISTRY):$(TAG)
	docker push $(REGISTRY):latest
