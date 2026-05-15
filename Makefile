IMAGE ?= heifeng/webnut
TIMESTAMP := $(shell date +%Y%m%d%H%M%S)

.PHONY: docker
docker:
	docker build -t $(IMAGE):latest -t $(IMAGE):$(TIMESTAMP) .
	docker push $(IMAGE):latest
	docker push $(IMAGE):$(TIMESTAMP)
	@echo "Pushed $(IMAGE):latest and $(IMAGE):$(TIMESTAMP)"
