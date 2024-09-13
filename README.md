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

# deploy test product and app data to the emulator
./3.deploy.testdata.sh

# verify that the APIs are deployed in the emulator
curl http://localhost:8081/v1/emulator/tree
# it should return both proxy names

# run bruno API tests
./4.test.apis.sh

# reset emulator
./5.reset.apigee.emulator.sh
```