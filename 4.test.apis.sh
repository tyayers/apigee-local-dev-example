# go to tests directory
cd tests/Bruno

# get current client credentials from emulator
CLIENT_KEY=$(curl http://localhost:8081/v1/emulator/test/developerapps | jq --raw-output '.[0].credentials.[0].consumerKey')
CLIENT_SECRET=$(curl http://localhost:8081/v1/emulator/test/developerapps | jq --raw-output '.[0].credentials.[0].consumerSecret')

# run bruno tests with credentials
bru run --env local --env-var client_id=$CLIENT_KEY --env-var client_secret=$CLIENT_SECRET

cd ../..