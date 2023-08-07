# coding: utf-8
"""
Name: cookie_to_s3uploader.py
Description: upload cookies to s3
Usage: python3 create_cookies.py --bucket <bucket_name> --cookie <cookie_file_path> --profile <aws_cli_profile>
Author: Ryosuke D. Tomita
Created: 2023/08/05
"""
import argparse
import boto3


def parse_args():
    """parse_args.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", help="bucket name", type=str)
    parser.add_argument("-c", "--cookie", help="cookie file path", type=str)
    parser.add_argument("-p", "--profile", help="aws cli profile", type=str, default="default")
    p = parser.parse_args()
    args = {"bucket": p.bucket, "cookie": p.cookie, "profile": p.profile}
    return args


def upload_to_s3(bucket_name, cookie, profile):
    """_summary_
    boto3は~/.aws/configにあるプロファイルを読み込む仕様のため
    場所を変更しない。

    """
    session = boto3.Session(profile_name=profile)
    s3 = session.client("s3")
    s3.upload_file(cookie, bucket_name, cookie)  # (local_file, bucket_name, s3_key)
    # boto3.resource('s3').Bucket(bucket_name).upload_file(cookie, cookie)


def main():
    args = parse_args()
    bucket_name = args["bucket"]
    cookie = args["cookie"]
    profile = args["profile"]

    upload_to_s3(bucket_name, cookie, profile)


if __name__ == "__main__":
    main()