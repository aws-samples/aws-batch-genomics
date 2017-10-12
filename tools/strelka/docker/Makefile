NAME=strelka
TAG=2.8.3

all: build push

build:
	docker build -t $(NAME):$(TAG) -t $(NAME):latest -f Dockerfile --build-arg VERSION=$(TAG) ../..
	docker tag $(NAME):latest $(REGISTRY):latest
	docker tag $(NAME):$(TAG) $(REGISTRY):$(TAG)

push:
	docker push $(REGISTRY):$(TAG)
	docker push $(REGISTRY):latest
