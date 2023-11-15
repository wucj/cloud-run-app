# cloud-run-app

This is a simple application run on the Google Cloud Run, this project is using python, flask, celery, and redis to demostrate web app on Google Cloud Run.

Since Google Cloud Run supports multiple docker instances run on one service, the concept is just like we can create a pod in k8s. Hence, we can use gcloud cli to create a service first, then export to a service.yaml file, and then add other docker in the service. 

## Setup steps

1. Download the gcloud cli tool
2. Do gcloud init and authentication
3. Create a repo in the GCP Artifact Registry console page to store docker image  
4. Add GCP Artifact repository to local 
```
gcloud auth configure-docker us-east1-docker.pkg.dev
cat ~/.docker/config.json
```
5. Go to IAM page, add `Service Account Token Creator` to current account. 
6. Add a service account on IAM page to allow us push/pull docker image via this service account. And add Artifact registry Admin permission to this service account.
7. Setup below environment variables
. GCP_PROJECT_NAME
. GCP_AR_EDITOR
. GCP_REGION
. GCP_AR_LOCATION
. GCP_AR_NAME
. APP_NAME
8. Run 
    ```./utils.py -d image```
    to verify image can be build and push to GCP Artifact registry
9. Run ```docker-compose up``` to for local development
10. Create a service on Google Cloud run 
```
gcloud run deploy $APP_NAME --image=image_name:current_vesion --set-env-vars=redis_url=localhost --platform managed --allow-unauthenticated --region=$GCP_REGION --project=$GCP_PROJECT_NAME
```
11. Export service to service.yaml via 
```
gcloud run services describe $APP_NAME --format export --region=asia-east1 --project=cj-applications > service.yaml
```
12. Add celery container and redis container to service.yaml
13. Run ```./utils.py -d all``` to build newer version of image and deploy to Cloud Run
14. Check service is running or not
```
curl https://app-name-xxxxx-2.a.run.app
```





