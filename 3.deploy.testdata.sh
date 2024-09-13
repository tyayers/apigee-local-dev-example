cd src/tests/test_data
zip testdata.zip *
curl --data-binary @testdata.zip -X POST http://localhost:8081/v1/emulator/setup/tests
rm testdata.zip
cd ../../..