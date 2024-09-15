# Apigee Local Development Minikube Example
This is an example Apigee local development environment using Minikube to run both the Apigee Emulator and a local microservice with APIs. No cloud services are used in this example.

## Getting started
You can run this on a local linux system with Docker installed, or in the [Google Cloud Shell](https://shell.cloud.google.com), where Docker is installed by default.

After cloning this repository, run these instructions to walk through the local development process.

```sh
# install minikube, if not already installed, as documented here: https://minikube.sigs.k8s.io/docs/start
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

# build the energy-trading-service example microservice from the services/energy-trading-service-v1 directory
cd services/energy-trading-service-v1
docker build -t energy-trading-service .
cd ../..

# load the energy-trading-service container to minikube
minikube image load energy-trading-service:latest

# deploy both the apigee emulator and the energy-trading-service to minikube
kubectl apply -f ./kubernetes/apigee.deployment.yaml
kubectl apply -f ./kubernetes/energy.svc.deployment.yaml

# now check the services to make sure that they are running
kubectl get svc
# WAIT and retry until you see the apigee-emulator and energy-trading-service running

# get the svc url to reach the apigee-emulator
minikube service apigee-emulator --url
# the two URLs are the endpoints to reach the apigee emulator

# set the env variable APIGEE_CTL to the first URL
# set the env variable APIGEE_HOST to the second URL
APIGEE_CTL=http://192.168.49.2:31623
APIGEE_HOST=http://192.168.49.2:30256

# zip the src proxy directory and upload to the apigee-emulator
zip -r deployment.zip src
curl --data-binary @deployment.zip -X POST "$APIGEE_CTL/v1/emulator/deploy?environment=dev"
rm deployment.zip
# you should get a revision: 2 response, and not an error

# now deploy test data to test the APIs with
cd src/tests/test_data
zip testdata.zip *
curl --data-binary @testdata.zip -X POST "$APIGEE_CTL/v1/emulator/setup/tests"
rm testdata.zip
cd ../../..
# you should get an empty reponse, so error

# call the emulator status API to see the currently deployed proxies (OAuth and Trading)
curl "$APIGEE_CTL/v1/emulator/tree"

# try calling the energy-service/trades API
curl -i "$APIGEE_HOST/energy-service/trades"
# you should get a 401 invalid access token response

# get and save the client key and secret from the test data app
APP_OUTPUT=$(curl "$APIGEE_CTL/v1/emulator/test/developerapps")
CLIENT_KEY=$(echo "$APP_OUTPUT" | jq --raw-output '.[0].credentials[0].consumerKey')
CLIENT_SECRET=$(echo "$APP_OUTPUT" | jq --raw-output '.[0].credentials[0].consumerSecret')
echo "$CLIENT_KEY $CLIENT_SECRET"
# you should see a client key and secret displayed

# get OAuth access token using client key and secret
TOKEN=$(curl -X POST "$APIGEE_HOST/oauth/token" \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "grant_type=client_credentials" \
	-d "client_id=$CLIENT_KEY" \
	-d "client_secret=$CLIENT_SECRET" | jq --raw-output '.access_token')

# call energy-service/trades with OAuth token
curl "$APIGEE_HOST/energy-service/trades" -H "Authorization: Bearer $TOKEN"
# you should get the test trades data returned from our python microservice

# stop minikube
minikube stop
```