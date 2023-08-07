# INDEX
- [ABOUT](#ABOUT)
- [ENVIRONMENT](#ENVIRONMENT)
- [PREPARING(Cloud Formation)](#Cloud-Formation)
- [PREPARING(GUI)](#PREPARING(GUI))
- [HOW TO USE](#HOW-TO-USE)
- [REFERENCE](#REFERENCE)
******


# ABOUT
- Using selenium, push [ocn top page](https://www.ocn.ne.jp/) "OCN訪問ポイント" button automatically to get Dpoint.
- This script can save session information to cookies.pkl

![ocn訪問ポイント](./docs/fig/ocn訪問ポイント.png)
******


# ENVIRONMENT
- python 3.7
- see [requirements.txt](./requirements.txt)
******


# PREPARING(Cloud Formation)
## AWS CLI
- Create AWS IAM role for AWS CLI and save AccessKey and SecretAccessKey.
- [install aws cli](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)
- create ~/.aws/config and paste AccessKey, SecretAccessKey.

```
[profile default]
region = ap-northeast-1
aws_access_key_id = <<IAM AccessKey>>
aws_secret_access_key = <<IAM SecretAccessKey>>
```

- check connection 

```shell
aws s3 ls --profile gr360
```

## python(venv)

```shell
# install python3.7
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
 
# install python3.7 venv
sudo apt install python3.7-venv
 
# create python3.7 venv
python3.7 -m venv ~/ocn_daily_login
source ~/ocn_daily_login/bin/activate # activate venv
```

## clone repository

```shell
# download repository
git clone https://github.com:RyosukeDTomita/ocn_dialy_login_aws_lambda.git

# set up
cd ocn_dialy_login_aws_lambda
pip -r requirements.txt

```

## create Lambda Layers

```shell
cd PackageLayers
source mk_lambda_layer.sh
```


## AWS SAM settings

> [how to install](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/install-sam-cli.html)
1. download zip
2. unzip
3. install
4. check

```shell
# install command
sudo ./sam-installation/install
sam --version
```


### build and deploy(WEP)

```shell
sam build
sam deploy --guided
```

```shell
sam delete # delete stack
```

******


# PREPARING(GUI)

## create lambda
Create Lambda Basic Excecution IAM role and Add `AmazonS3ReadOnlyAccess`

### create Lambda Layers

```shell
cd PackageLayers
source mk_lambda_layer.sh
```

## create S3 Bucket
- Bucket Name example: cookie-for-iceman
******


# HOW TO USE
WEP
## create session cookie and save to s3

```shell
python3 create_cookies.py --userid <docomoID> --password <password> --bucket cookie-for-iceman --profile default
```
