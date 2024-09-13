docker pull gcr.io/apigee-release/hybrid/apigee-emulator:1.12.1
docker run -d -p 8081:8080 -p 8998:8998 gcr.io/apigee-release/hybrid/apigee-emulator:1.12.1