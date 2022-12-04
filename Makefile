
default:
	@echo "Please specify a make command. help command might be usefull"

reinstall_package:
	@pip uninstall -y brain-signals_api && pip install -e .

hard_uninstall:
	@pip uninstall -yr requirements.txt brain-signals_api

update_registry:
	@gsutil -m cp -nc ${LOCAL_REGISTRY_PATH}/* gs://vape-mri/registry || :
	@gsutil -m cp -nc gs://vape-mri/registry/* ${LOCAL_REGISTRY_PATH}

run_api:
	@uvicorn brainsignals.api:app --reload

deploy_api:
	@docker build --platform linux/amd64 --tag=${GCR_MULTI_REGION}/${PROJECT}/${IMAGE}:prod . && :
	@docker push ${GCR_MULTI_REGION}/${PROJECT}/${IMAGE}:prod && :
	@gcloud run deploy --image ${GCR_MULTI_REGION}/${PROJECT}/${IMAGE}:prod \
		--port=8080 --cpu=2 --min-instances=1 --memory=8Gi --region=europe-west1 \
		--allow-unauthenticated
