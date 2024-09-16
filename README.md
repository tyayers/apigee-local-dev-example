# Apigee Local Development Minikube Example
✨✨ A simpler version of this project is in the [http-bin-example branch](https://github.com/tyayers/apigee-local-dev-example/tree/http-bin-example) with just a single container calling the httpbin.org endpoint (no minikube or microservice needed).

This is an example Apigee local development environment using Minikube to run both the Apigee Emulator and a local microservice with APIs. No cloud services are used in this example.

## Getting started
You can run this on a local linux system with Docker and minikube installed, or in the [Google Cloud Shell](https://shell.cloud.google.com), where everything is installed by default.

After cloning this repository, run these instructions to walk through the local development process.

```sh
# start minikube on your local machine
minikube start

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
kubectl get pod
# WAIT and retry until the apigee-emulator and energy-trading-service pods are running

# get the svc url endpoints to reach the apigee-emulator
APIGEE_URLS=$(minikube service apigee-emulator --url)
APIGEE_URLS=($APIGEE_URLS)
APIGEE_CTL=${APIGEE_URLS[0]}
APIGEE_HOST=${APIGEE_URLS[1]}

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

# run bruno tests
npm install -g @usebruno/cli
cd tests/bruno
bru run --env local --env-var client_id=$CLIENT_KEY --env-var client_secret=$CLIENT_SECRET --env-var baseUrl=$APIGEE_HOST
cd ../..
# you should see 3 tests passed for OAuth get token and get trades

# stop minikube
minikube stop
```