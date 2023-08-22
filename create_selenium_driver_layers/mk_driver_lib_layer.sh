#!/bin/bash
# see https://dev.classmethod.jp/articles/aws-lambda-python-selenium-make-env/

# install chromium headless
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip -o headless-chromium.zip -d .

# install headless-chromiun-driver
curl -SL https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip > chromedriver.zip
unzip -o chromedriver.zip -d .

#
mkdir headless
mv -f chromedriver headless/
mv -f headless-chromium headless/
zip -r headless headless

# No CloudFormation then, comment out below.
#aws lambda publish-layer-version --layer-name selenium-driver --description "selenium driver lib" --zip-file fileb://headless.zip --compatible-runtimes  "python3.7"

