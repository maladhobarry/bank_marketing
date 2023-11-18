.PHONY: docker-build-client
docker-build-client:
	docker build -f Dockerfile.client -t client .

.PHONY: docker-build-server
docker-build-server:
	docker build -f Dockerfile.server -t server .


.PHONY: docker-run-server
docker-run-server:
	docker run --rm \
	-p 127.0.0.1:5000:5000 \
	-v ./models:/models:ro \
	--env TRANSFORMER_PATH=/models/rf_with_minibatch_kmeans/feature_eng_pipeline.joblib \
	-e MODEL_PATH=/models/rf_with_minibatch_kmeans/model.joblib \
	server

.PHONY: docker-run-client
docker-run-client:
	docker run --rm \
	-p 127.0.0.1:8501:8501 \
	-e ECO_SOCIO_DF=/data/external/socio_economic_indices_data.csv \
	-e FUTURE_RES_DF=/data/external/campaign_results_data.csv \
	-e BANK_DB=/data/bank_marketing.db \
	-e SERVER_API_URL=http://172.17.0.2:5000/predict \
	-v ./data:/data:ro \
	client
