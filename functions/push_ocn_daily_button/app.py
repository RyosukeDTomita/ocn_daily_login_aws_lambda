# coding: utf-8
"""
Description: use cookies.pkl stored in S3 and login "https://www.ocn.ne.jp/" to push the ocn daily point button.
Usage: AWS Lambada
Author: Ryosuke D. Tomita
Created: 2023/08/05
"""
from selenium import webdriver
import pickle
import time
import os
import json
import boto3


def lambda_handler(event, context):
    """
    実質的なmain関数
    """
    # get environment variables
    url = "https://www.ocn.ne.jp/"
    bucket_name = os.environ["S3BucketCookie"]

    # get cookies from s3
    cookies_file = _get_cookies_from_s3(bucket_name)

    driver = _fetch_driver()

    # driverにcookiewをセットしてログイン。
    _set_cookies(driver, cookies_file)
    driver.get(url)

    # push daily point button.
    _get_daily_point(driver)

    driver.quit()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def _get_cookies_from_s3(bucket_name):
    """
    cookies.pklがS3にない，もしくは空の場合にエラーを返す
    S3からcookies.pklを取得する
    """
    s3 = boto3.resource('s3')
    object_key = 'cookies.pkl'
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(object_key)
    response = obj.get()
    return response['Body'].read()


def _fetch_driver():
    """fetch_driver.
    ヘッドレスモードでドライバを取得する。
    """
    options = webdriver.ChromeOptions()
    # headlessモードのchromiumを指定
    options.binary_location = "/opt/headless/headless-chromium"
    options.add_argument("--headless")
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    # Layersに配置したものは/opt以下に展開される。
    driver = webdriver.Chrome(
        # chromedriverのパスを指定
        executable_path="/opt/headless/chromedriver",
        options=options
    )
    return driver


def _set_cookies(driver, cookies_file):
    cookies = pickle.load(open(cookies_file, 'rb'))
    for c in cookies:
        driver.add_cookie(c)


def _get_daily_point(driver):
    """get_daily_point.
    デイリーボタンを押す。

    Args:
        driver:
    """
    # selenium can only click viewing element, so scroll it.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    point_button = driver.find_element(By.XPATH, '//*[@id="normalget"]/img')
    point_button.click()
    time.sleep(3)
