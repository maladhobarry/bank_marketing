# TODO(PARTICIPANT)
# IMPORTANT:
#	UPDATE ALL THE REFERENCES TO THE ID TO YOUR PROJECT ID
#	ivamlops-2023-ptcpt-e-d96584 --> YOUR PROJECT ID
#
# Q: I am a Windows user or don't have make installed
# A: You can copy-paste the commands and change the
#    values to fit your environment.
#
# Q: Why are we repeating ourselves and not putting that
#    id in a variable?
# A: Because we want to make it easy for everyone to read
#    and Makefile syntax is not necessarily the most clear.
#    Feel free (and you are encouraged) to put them in variables
#    so that everything is easier for you.
# Q: How do I get my kubectl context for GKE commands?
# A: Read the commands below
#	1) Install gcloud (https://cloud.google.com/sdk/docs/install)
#	1) Install GKE plugin for https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#install_plugin
#	1) Get credentials for the GKE cluster: `gcloud --account "YOUR_EMAIL@ivamlops.ca" container clusters get-credentials gke-cluster-nane1 --region=northamerica-northeast1`
#	1) Get the context value: `kubectl config get-contexts` (there shou)
#		It should be something like "gke_<your-project-id>_northamerica-northeast1_gke-cluster-nane1"

##############################################
#
# Docker section
#
##############################################

#-------------------------------------
# Tag subsection
# When running a command such as
# make ___ docker-build-server
# Behaviour when ___ matches:
#	(empty)				-> automatic docker tag set to
#						   Git SHA.
#						   (client and server only)
#	TAG=v44				-> docker images are used
#						   with :v44 as docker tag
#						   (client and server only)
#	TAG=				-> no tagging whatsoever
#	NO_TAG=1			-> no tagging whatsoever
#	DOCKER_TAG=			-> no tagging whatsoever
#	ADD_DATETIME=1		-> if using automatic tagging,
#						   datetime used

# Warning: this is far from ideal since each time we run
#          a new make command, the date changes.
#          As always, you can override the ?= variables
#          by providing them on the command line.
DATETIME_NOW ?= $(shell date '+%F-%H-%M-%S')

ifeq ($(origin TAG),undefined)
DOCKER_TAG ::= :$(shell git rev-parse --no-flags --short=8 --tags HEAD)$(if $(ADD_DATETIME),-$(DATETIME_NOW),)
else
DOCKER_TAG ::= $(if $(TAG),:$(TAG),)
endif

ifdef NO_TAG
DOCKER_TAG ::=
endif

.PHONY: show-tag
show-tag:
	@echo $(DOCKER_TAG)

#----------------
# Docker commands
#----------------

.PHONY: docker-build-client
docker-build-client:
	docker build -f Dockerfile.client \
	-t northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/client$(DOCKER_TAG) \
	-t northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/client:latest \
	.

.PHONY: docker-build-server
docker-build-server:
	docker build -f Dockerfile.server \
	-t northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/server$(DOCKER_TAG) \
	-t northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/server:latest \
	.


.PHONY: docker-run-server
docker-run-server:
	docker run --rm \
	-p 127.0.0.1:5000:5000 \
	-v ./models:/models:ro \
	--env TRANSFORMER_PATH=/models/rf_with_minibatch_kmeans/feature_eng_pipeline.joblib \
	-e MODEL_PATH=/models/rf_with_minibatch_kmeans/model.joblib \
	northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/server$(DOCKER_TAG)

.PHONY: docker-run-client
docker-run-client:
	docker run --rm \
	-p 127.0.0.1:8501:8501 \
	-e ECO_SOCIO_DF=/data/external/socio_economic_indices_data.csv \
	-e FUTURE_RES_DF=/data/external/campaign_results_data.csv \
	-e BANK_DB=/data/bank_marketing.db \
	-e SERVER_API_URL=http://172.17.0.2:5000/predict \
	-v ./data:/data:ro \
	northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/client$(DOCKER_TAG)

.PHONY: docker-build-tests
docker-build-tests:
	docker build -f Dockerfile.tests -t northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/tests .

.PHONY: docker-run-tests
docker-run-tests:
	docker run --rm -t \
	-v ./data:/data:ro \
	northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/tests \
	tests \
	. --db /data/bank_marketing.db --sed /data/external/socio_economic_indices_data.csv

.PHONY: docker-run-coverage
docker-run-coverage:
	docker run --rm -t \
	-v ./data:/data:ro \
	-v ./out:/app/out \
	northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/tests \
	tests \
	--cov-config .coveragerc \
	--db /data/bank_marketing.db --sed /data/external/socio_economic_indices_data.csv

.PHONY: docker-push-images
docker-push-images: docker-push-client docker-push-server docker-push-tests

.PHONY: docker-push-client docker-push-server docker-push-tests
docker-push-client:
	docker push northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/client$(DOCKER_TAG)
docker-push-server:
	docker push northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/server$(DOCKER_TAG)
docker-push-tests:
	docker push northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/tests

.PHONY: docker-push-images-to-minikube
docker-push-images-to-minikube:
	@minikube image load northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/server$(DOCKER_TAG)
	@minikube image load northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/client$(DOCKER_TAG)
	@minikube image load northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/tests

.PHONY: docker-show-image-digests
docker-show-image-digests:
	docker image ls --digests northamerica-northeast1-docker.pkg.dev/ivamlops-2023-ptcpt-e-d96584/bank-marketing/*

##############################################
#
# HELPERS
#
##############################################
.PHONY: quicktrain
quicktrain:
	jupyter nbconvert --execute notebooks/Modeling.ipynb --to notebook --inplace


##############################################
#
# Requirements section
#
##############################################


.PHONY: generate-requirements
generate-requirements: requirements.txt $(addprefix requirements/, $(addsuffix .requirements.txt, server client data-science testing all)) requirements/local.txt

# Note: there is a way to make this DRY, but it is less readable
# and for code that doesn't change that much, such an approach
# is too overkill and is actually counter productive.
requirements/server.requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra server --output-file requirements/server.requirements.txt
requirements/client.requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra client --output-file requirements/client.requirements.txt
requirements/data-science.requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra data-science --output-file requirements/data-science.requirements.txt
requirements/testing.requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra testing --output-file requirements/testing.requirements.txt
requirements/style.requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra style --output-file requirements/style.requirements.txt
requirements/all.requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra all --output-file requirements/all.requirements.txt
requirements.txt: pyproject.toml setup.cfg setup.py
	pip-compile --strip-extras --extra all --output-file requirements.txt 
requirements/local.txt:
	pip-compile --strip-extras --output-file requirements/local.txt requirements/local.in

# These commands are the most usable without pip tools.
.PHONY: freeze-requirements-no-editable freeze-requirements-no-bank_marketing
freeze-requirements-no-editable:
	pip freeze --exclude-editable -l
freeze-requirements-no-bank_marketing:
	pip freeze --exclude bank_marketing -l


##############################################
#
# GKE DEPLOY COMMANDS
#
##############################################
# To get your kubectl context you can execute the command:
#	$ kubectl config get-contexts
# And then look for a string containg your PROJECT ID and your cluster name
.PHONY: scale-deployments-to-zero
scale-deployments-to-zero:
	kubectl --context=gke_ivamlops-2023-ptcpt-e-d96584_northamerica-northeast1_gke-cluster-nane1 scale --replicas=0 deploy/frontend deploy/backend

# This command is necessary to make a local (your laptop) folder be available/mounted in
# the minikube nodes (the "VMs").
.PHONY: mount-minikube-pv
mount-minikube-pv:
	@minikube -p ivado mount --port=40855 /var/tmp/ivamlops:/data/ivamlops

.PHONY: deploy-minikube
deploy-minikube:
	@kubectl --context=ivado apply \
	-f 'manifests/base/*.yaml' \
	-f 'manifests/local/*.yaml'

# Important: modify to use your own context
.PHONY: deploy-gke
deploy-gke:
	@kubectl --context=gke_ivamlops-2023-ptcpt-e-d96584_northamerica-northeast1_gke-cluster-nane1 apply \
	-f 'manifests/base/*.yaml' \
	-f 'manifests/cloud/*.yaml'
