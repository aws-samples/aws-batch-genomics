NAME=strelka
TAG=2.7.1

all: build push

build:
	docker build -t $(NAME):$(TAG) -t $(NAME):latest -f Dockerfile ../..
	docker tag $(NAME):latest $(REGISTRY):latest
	docker tag $(NAME):$(TAG) $(REGISTRY):$(TAG)

push:
	docker push $(REGISTRY):$(TAG)
	docker push $(REGISTRY):latest
