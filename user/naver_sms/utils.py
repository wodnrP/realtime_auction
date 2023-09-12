import os
from pathlib import Path
import environ
import json
import hashlib
import hmac
import base64
import requests
import time

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

NAVER_ACCESS_KEY = env("NAVER_ACCESS_KEY")
NAVER_SECRET_KEY = env("NAVER_SECRET_KEY")
SERVICE_ID = env("SERVICE_ID")
PHONE = env("PHONE")


def make_signature():
    """
    naver clound를 사용하기 위한 signature maker
    """
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    access_key = NAVER_ACCESS_KEY.strip()
    secret_key = NAVER_SECRET_KEY.strip()
    secret_key = bytes(secret_key, "UTF-8")

    method = "POST"
    uri = f"/sms/v2/services/{SERVICE_ID}/messages"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, "UTF-8")
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
    )
    return signingKey, timestamp


def send_sms(signature, timestamp, random_number, phone_number):
    """
    휴대폰 번호 인증 sms 요청
    """
    headers = {
        "content-type": "application/json",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": NAVER_ACCESS_KEY,
        "x-ncp-apigw-signature-v2": signature,
    }
    print("header", headers)
    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": PHONE,
        "content": f" [Realtime Auction] 인증 번호를 입력해주세요. [인증번호:{random_number}]",
        "messages": [{"to": f"{phone_number}"}],
    }

    send_url = f" https://sens.apigw.ntruss.com/sms/v2/services/{SERVICE_ID}/messages"
    res = requests.post(send_url, headers=headers, data=json.dumps(body))
    return res
