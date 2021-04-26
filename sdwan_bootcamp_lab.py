"""
copyright Cisco
created by bshokrol
04/24/2021

"""

# pip install pandas
import pandas as pd
import sys
import getpass
import json
# pip install requests
import requests
# ignore insecure requests warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 2000)

GET_ALL_DEVICES = "dataservice/device"
GET_ALL_DEVICE_TEMPLATES = "dataservice/template/device"
GET_BFD_SESSIONS = "dataservice/device/bfd/sessions?deviceId={0}"


class SdwanBootcamp:
    def __init__(self, vmanage_address: str, vmanage_username: str, vmanage_password: str, verify: bool = False):
        self.session = self.authenticate(
            vmanage_address, vmanage_username, vmanage_password)
        self.vmanage_address = vmanage_address
        self.verify = verify

    @staticmethod
    def authenticate(vmanage_address: str, vmanage_username: str, vmanage_password: str, verify: bool = False) -> requests.session:
        session = requests.session()
        payload = {
            "j_username": vmanage_username,
            "j_password": vmanage_password
        }
        url = f"{vmanage_address}j_security_check"
        response = session.post(url=url, data=payload, verify=verify)
        if "<html>" in str(response.content):
            print("Authentication failed")
            sys.exit(0)
        print("Authenticated")
        session.headers["X-XSRF-TOKEN"] = session.get(
            f"{vmanage_address}dataservice/client/token").content
        session.headers["Content-Type"] = "application/json"
        return session

    def post_request(self, endpoint: str, payload: dict) -> requests.Response:
        data = json.dumps(payload)
        url = f"{self.vmanage_address}{endpoint}"
        return self.session.post(url=url, data=data, verify=self.verify)

    def get_request(self, endpoint: str) -> requests.Response:
        url = f"{self.vmanage_address}{endpoint}"
        return self.session.get(url=url, verify=self.verify)


def main() -> None:
    # instructions fill in the missing code wherever you see a _____
    # 1 initialize class with credentials + authenticate
    vmanage_ip = ""
    vmanage_port = ""
    vmanage_username = ""
    vmanage_password = getpass.getpass("vmanage password: ")
    vmanage_address = f"https://{vmanage_ip}:{vmanage_port}/"
    sdwan_bootcamp = SdwanBootcamp(vmanage_address=vmanage_address,
                                   vmanage_username=vmanage_username, vmanage_password=vmanage_password)
    # 2 get all devices in overlay using get_request
    _____ = sdwan_bootcamp.get_request(endpoint=_____)
    print(_____.status_code)
    all_devices_df = pd.DataFrame(_____.json().get("data"))
    print("All devices dataframe")
    print(all_devices_df)
    # 3 get all device templates in vmange using get_request
    response = sdwan_bootcamp._____(endpoint=GET_ALL_DEVICE_TEMPLATES)
    print(response.status_code)
    all_device_templates_df = pd.DataFrame(response._____._____("data"))
    print("All device templates dataframe")
    print(all_device_templates_df)
    # 4 get current bfd session for a specific device using get_request


if __name__ == "__main__":
    main()
