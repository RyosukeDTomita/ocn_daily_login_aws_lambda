# coding: utf-8
"""
Name: create_cookies.py
Description: Create cookies for login to the "https://www.ocn.ne.jp/"
Usage: python3 create_cookies.py --userid <user_id> --password <password>
Author: Ryosuke D. Tomita
Created: 2023/08/05
"""
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import time
import os
from os.path import join, dirname, abspath, exists
import boto3


def parse_args() -> dict:
    """parse_args.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--userid", help="docomo userID", type=str)
    parser.add_argument("-s", "--password", help="docomo user password", type=str)

    parser.add_argument("-p", "--profile", help="aws cli profile", type=str, default="default")
    parser.add_argument("-b", "--bucket", help="bucket name", type=str)
    p = parser.parse_args()
    args = {"userid": p.userid,
            "password": p.password,
            "profile": p.profile,
            "bucket": p.bucket
            }
    return args


def cookies_file_is_valid(cookies_file_path: str) -> bool:
    """cookies_file_is_valid.
    1. cookies.pklがローカルになければ空のファイルを作成し，Falseを返す。
    2. cookies.pklが空の場合にはFalseを返す。
    3. cookies.pklが存在し，中身がある場合にはtrueを返す。
    """
    if not exists(cookies_file_path):
        print("create cookies.pkl")
        with open(cookies_file_path, 'wb'):
            pass
        return False
    elif os.stat(cookies_file_path).st_size == 0:
        print("cookies.pkl is empty")
        return False
    print("cookies.pkl is valid")
    return True


def fetch_driver():
    """fetch_driver.
    ヘッドレスモードでドライバを取得する。
    """
    options = webdriver.ChromeOptions()
    # headlessモードのchromiumを指定
    options.binary_location = "./selenium_tools/headless/headless-chromium"
    options.add_argument("--headless")
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    # Layersに配置したものは/opt以下に展開される。
    driver = webdriver.Chrome(
        # chromedriverのパスを指定
        executable_path="./selenium_tools/headless/chromedriver",
        options=options
    )
    return driver



def login(driver, user_id, password):
    """login.
    Security codeはコンソールに手動で入力する。
    $"Type security code: "123456

    Args:
        driver:
        user_id:
        password:
    """
    login_button1 = driver.find_element(By.XPATH, '//*[@id="va14-vin-2d"]')

    login_button1.click()
    time.sleep(3)

    # input ID
    id_textbox = driver.find_element(By.XPATH, '//*[@id="Di_Uid"]')
    id_textbox.send_keys(user_id)
    next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[4]/div[1]/form/input[4]')
    next_button.click()

    # input password and security_code
    password_textbox = driver.find_element(By.XPATH, '//*[@id="Di_Pass"]')
    password_textbox.send_keys(password)
    security_code = input("Type security code: ")
    security_code_textbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[6]/form/dl[2]/dd[2]/input')
    security_code_textbox.send_keys(security_code)
    time.sleep(3)

    # login
    login_button2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[6]/form/input[4]')
    login_button2.click()
    time.sleep(5)


def save_cookies(driver, cookies_file_path):
    cookies = driver.get_cookies()
    pickle.dump(cookies, open(cookies_file_path, 'wb'))


def upload_to_s3(bucket_name, cookie, profile):
    """_summary_
    boto3は~/.aws/configにあるプロファイルを読み込む仕様のため
    場所を変更しない。

    """
    session = boto3.Session(profile_name=profile)
    s3 = session.client("s3")
    s3.upload_file(cookie, bucket_name, cookie)  # (local_file, bucket_name, s3_key)


def main():
    """_summary_
    1. コマンドライン引数からid，passwordを取得する。
    2. cookies.pklが存在し，有効か確認する。
    3. driverを取得する。
    4. ログインする。
    5. cookies.pklに保存する。
    """
    args = parse_args()
    user_id = args['userid']
    password = args['password']
    bucket_name = args['bucket'] # s3 bucket
    profile = args['profile'] # aws cli profile
    url = "https://www.ocn.ne.jp/"
    #cookies_file_path = abspath(join(dirname(__file__), 'cookies.pkl'))
    cookies_file_path = "cookies.pkl" # フルパスで指定するとなぜかuploadできない

    if cookies_file_is_valid(cookies_file_path):
        upload_to_s3(bucket_name, cookies_file_path, profile)
        return

    driver = fetch_driver()

    # login
    driver.get(url)
    login(driver, user_id, password)

    save_cookies(driver, cookies_file_path)
    driver.quit()

    upload_to_s3(bucket_name, cookies_file_path, profile)


if __name__ == '__main__':
    main()
