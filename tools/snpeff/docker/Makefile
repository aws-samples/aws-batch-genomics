NAME=snpeff-aws
TAG=4.3p
UNDERSCORE_TAG=4_3p

all: build push

build:
	docker build -t $(NAME):$(TAG) -t $(NAME):latest -f Dockerfile --build-arg VERSION=$(TAG) --build-arg UNDERSCORE_VERSION=$(UNDERSCORE_TAG) ../..
	docker tag $(NAME):latest $(REGISTRY):latest
	docker tag $(NAME):$(TAG) $(REGISTRY):$(TAG)

push:
	docker push $(REGISTRY):$(TAG)
	docker push $(REGISTRY):latest
