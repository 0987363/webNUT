IMAGE ?= heifeng/webnut
TIMESTAMP := $(shell date +%Y%m%d%H%M%S)
AMD64_PLATFORM := linux/amd64
ARM64_PLATFORM := linux/arm64

.PHONY: docker docker-arm64
docker:
	docker build --platform $(AMD64_PLATFORM) -t $(IMAGE):latest -t $(IMAGE):$(TIMESTAMP) .
	docker push $(IMAGE):latest
	docker push $(IMAGE):$(TIMESTAMP)
	@echo "Pushed $(IMAGE):latest and $(IMAGE):$(TIMESTAMP)"

docker-arm64:
	docker build --platform $(ARM64_PLATFORM) -t $(IMAGE):latest-arm64 -t $(IMAGE):$(TIMESTAMP)-arm64 .
	docker push $(IMAGE):latest-arm64
	docker push $(IMAGE):$(TIMESTAMP)-arm64
	@echo "Pushed $(IMAGE):latest-arm64 and $(IMAGE):$(TIMESTAMP)-arm64"
