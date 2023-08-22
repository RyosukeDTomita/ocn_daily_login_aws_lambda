# README for GUI User
## AWS Console(Instead of CloudFormation)
If you use CloudFormation, don't have to this step.

### AWS Lambda
- Create Lambda Basic Excecution IAM role and Add `AmazonS3ReadOnlyAccess`

- create Lambda Layers

```shell
cd create_python_lib_layers
source mk_lambda_layer.sh
cd create_selenium_driver_layers
source mk_driver_lib_layer.sh
```


- paste ./functions/push_ocn_daily_button/app.py
- change lambda settins

|       |       |
|-------|-------|
|timeout|memory |
|1 min  |3007 MB|


### S3 Bucket
- create S3 Bucket to save `cookies.pkl`
> Bucket Name example: cookie-for-iceman

### EventBridge
- Choose `Flexible time window`
> Scheduler invokes your schedule within the time window you specify.
- Cron style schedule settings.

```
0 1 * * ? *
Wed, 09 Aug 2023 01:00:00 (UTC+09:00)
Thu, 10 Aug 2023 01:00:00 (UTC+09:00)
Fri, 11 Aug 2023 01:00:00 (UTC+09:00)
Sat, 12 Aug 2023 01:00:00 (UTC+09:00)
Sun, 13 Aug 2023 01:00:00 (UTC+09:00)
```
