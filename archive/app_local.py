# coding: utf-8
"""
Description: use cookies.pkl stored in S3 and login "https://www.ocn.ne.jp/" to push the ocn daily point button.
Usage: AWS Lambada
Author: Ryosuke D. Tomita
Created: 2023/08/05
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    #bucket_name = os.environ["S3BucketCookie"]
    bucket_name = "cookie-for-iceman"

    # get cookies from s3
    cookies_file = _get_cookies_from_s3(bucket_name)

    driver = _fetch_driver()

    # driverにcookiewをセットしてログイン。
    driver.get(url)
    _set_cookies(driver, cookies_file)
    time.sleep(10)
    driver.get(url)
    time.sleep(10)

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
    #s3 = boto3.resource('s3')
    #object_key = 'cookies.pkl'
    #bucket = s3.Bucket(bucket_name)
    #obj = bucket.Object(object_key)
    #response = obj.get()
    #with open('/tmp/temp_cookies.pkl', 'wb') as tf:
    #    tf.write(response['Body'].read())
    return '/home/tomita/ocn_daily_login/ocn_daily_login_aws_lambda/cookies.pkl'


def _fetch_driver():
    """fetch_driver.
    ヘッドレスモードでドライバを取得する。
    """
    options = webdriver.ChromeOptions()
    # headlessモードのchromiumを指定
    #options.binary_location = "/opt/headless/headless-chromium"
    options.binary_location = "../../selenium_tools/headless/headless-chromium"
    options.add_argument("--headless")
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    # Layersに配置したものは/opt以下に展開される。
    driver = webdriver.Chrome(
        # chromedriverのパスを指定
        #executable_path="/opt/headless/chromedriver",
        executable_path="../../selenium_tools/headless/chromedriver",
        options=options
    )
    return driver


def _set_cookies(driver, cookies_file):
    with open(cookies_file, 'rb') as f:
        cookies = pickle.load(f)
        for c in cookies:
            name = c['name']
            print("name: ", name)
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
    #login_button = driver.find_element(By.XPATH, '//*[@id="pa14-pin-3d"]')
    logout_button = driver.find_element(By.XPATH, '//*[@id="pa14-pout-3d"]')

    point_button = driver.find_element(By.XPATH, '//*[@id="normalget"]/img')
    point_button.click()
    time.sleep(3)


if __name__ == "__main__":
    lambda_handler(None, None)
