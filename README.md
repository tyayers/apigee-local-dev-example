# Apigee local testing example using HttpBin
This is a simple example of two Apigee proxies that can be deployed locally to the [Apigee Emulator](https://cloud.google.com/apigee/docs/api-platform/local-development/overview) and tested using [Bruno](https://www.usebruno.com/).

## Proxies
These proxies are included here in the repository under `src/main/apigee/apiproxies`

-  OAuth-v1 - an OAuth 2.0 token endpoint to get a token using client credentials.
- HttpBinAPI-v1 - a test API that requires an OAuth 2.0 token from the token endpoint to make a test call to https://httpbin.org.

## Prerequisites
- Docker installed locally (or you can use Docker in Google Cloud shell).
- The tool [Bruno](https://www.usebruno.com/) for running API tests is step 5.

## Getting started
After cloning this repository, run these commands to deploy and test the proxies. Take a look, or make changes to any of the scripts below, 

```sh
# start the apigee emulator
./1.start.apigee.emulator.sh
# the emulator container should be pulled and started using the ports 8081 for management and 8082 for API calls.

# deploy the APIs to the emulator
./2.deploy.apis.sh

# make a test API call
curl -i http://localhost:8082/httpbin/get
# should return 401 (unauthorized, no token sent)

# deploy test product and app data to the emulator
./3.deploy.testdata.sh

# verify that the APIs are deployed in the emulator
curl http://localhost:8081/v1/emulator/tree
# it should return both proxy names

# test API with credentials
CLIENT_KEY=$(curl http://localhost:8081/v1/emulator/test/developerapps | jq --raw-output '.[0].credentials.[0].consumerKey')
CLIENT_SECRET=$(curl http://localhost:8081/v1/emulator/test/developerapps | jq --raw-output '.[0].credentials.[0].consumerSecret')
TOKEN=$(curl -X POST http://0:8082/oauth/token \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "grant_type=client_credentials" \
	-d "client_id=$CLIENT_KEY" \
	-d "client_secret=$CLIENT_SECRET" | jq --raw-output '.access_token')
curl http://localhost:8082/httpbin/get -H "Authorization: Bearer $TOKEN"
# should return get info from HttpBin.org, equivalent of calling `curl https://httpbin.org/get`

# run bruno API tests
./4.test.apis.sh
# the tests should run successfully, or see what is wrong in the error results.

# reset emulator
./5.reset.apigee.emulator.sh
```