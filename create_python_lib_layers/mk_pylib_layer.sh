#!/bin/bash
# see https://repost.aws/ja/knowledge-center/lambda-layer-simulated-docker
python_version=3.7

cp ../functions/push_ocn_daily_button/requirements.txt requirements.txt

docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python${python_version}" /bin/sh -c "pip install -r requirements.txt -t python/lib/python${python_version}/site-packages/; exit"
zip -r push_ocn_libs.zip python > /dev/null
cp ../functions/push_ocn_daily_button/requirements.txt ./python/requirements.txt
aws lambda publish-layer-version --layer-name push_ocn_libs --description "My python libs" --zip-file fileb://push_ocn_libs.zip --compatible-runtimes  "python${python_version}"
