import json
from datetime import datetime, timedelta

import requests


class Client:

    def __init__(self):
        self.username = ""
        self.password = ""
        self.bearer_expiry = None
        self.bearer = None

        self.userinfo = None
        self.customer = None
        self.consumption = None

    def set_credential(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self):
        url = "https://apicskh.evnhanoi.com.vn/connect/token"
        payload = {
            'username': self.username,
            'password': self.password,
            'grant_type': 'password',
            'client_id': 'httplocalhost4500',
            'client_secret': 'secret'
        }
        # payload_encoded = urllib.parse.urlencode(payload)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url=url, headers=headers, data=payload)

        # if not response.status_code == 200:
        #     return response.status_code
        self.bearer = response.json()["access_token"]
        self.bearer_expiry = datetime.now() + timedelta(seconds=response.json()["expires_in"])
        # print(self.bearer)
        # print(self.bearer_expiry)

    def is_authenticated(self) -> bool:
        return (self.bearer is not None) and (self.bearer_expiry > datetime.now())

    def auth(self):
        if not self.is_authenticated():
            self.login()

    def get_user_info(self):
        self.auth()

        url = "https://apicskh.evnhanoi.com.vn/connect/userinfo"
        headers = {
            'Authorization': f'Bearer {self.bearer}'
        }
        response = requests.get(url=url, headers=headers)

        self.userinfo = response.json()
        return self.userinfo

    def get_customer(self) -> dict:
        self.auth()
        if self.userinfo is None:
            self.get_user_info()

        url = f"https://evnhanoi.vn/api/TraCuu/GetKhachHang?maDvQly={self.userinfo['maDvql']}" \
              f"&maKh={self.userinfo['maKhachHang']}"
        headers = {
            'Authorization': 'Bearer ' + self.bearer
        }
        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            return response.json()
        self.customer = {k: v for k, v in response.json()['data'].items() if v is not None}
        return self.customer

    def get_consumption(self, year: int):
        self.auth()
        if self.userinfo is None:
            self.get_user_info()

        url = "https://evnhanoi.vn/api/TraCuu/GetTinhHinhTieuThuDien"
        payload = json.dumps({
            "maDViQLy": self.userinfo['maDvql'],
            "maKhachHang": self.userinfo['maKhachHang'],
            "nam": year
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.bearer
        }
        response = requests.post(url=url, headers=headers, data=payload)

        if response.status_code != 200:
            return response.json()
        self.consumption = response.json()['data']
        return self.consumption
