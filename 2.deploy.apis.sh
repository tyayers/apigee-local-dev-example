# zip src apigee directory for deployment
zip -r deployment.zip src
# deploy to the apigee emulator
curl --data-binary @deployment.zip -X POST http://localhost:8081/v1/emulator/deploy?environment=dev
# remove zip file
rm deployment.zip