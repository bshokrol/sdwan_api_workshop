"""
copyright Cisco
created by bshokrol
04/24/2021

"""

from sdwan_bootcamp_lab_answer import SdwanBootcamp
import pandas as pd
from typing import Union
import getpass

SYSTEM_STATISTICS = "dataservice/statistics/system/"
REACHABLE = "reachable"
UNREACHABLE = "unreachable"
HOST_NAME = "host-name"
DEVICE_IP = "deviceIP"
REACHABILITY = "reachability"


class AvgCpuMem:
    def __init__(self, sdwan_bootcamp: SdwanBootcamp):
        self.sdwan_bootcamp = sdwan_bootcamp

    @staticmethod
    def get_component_query_payload(device_ip: str, component: str, hours="24") -> dict:
        return {"query": {"condition": "AND",
                          "rules": [{"value": [hours],
                                     "field": "entry_time",
                                    "type": "date",
                                     "operator": "last_n_hours"},
                                    {"value": [device_ip],
                                     "field": "vdevice_name",
                                     "type": "string",
                                     "operator": "in"}]
                          },
                "fields": ["entry_time",
                           "count",
                           component],
                "sort": [{"field": "entry_time",
                          "type": "date",
                          "order": "asc"}]}

    def get_avg_component_util(self, component: str, device_ip: str, hours: str = "24") -> Union[float, int]:
        query_payload = self.get_component_query_payload(
            device_ip=device_ip, component=component, hours=hours)
        response = self.sdwan_bootcamp.post_request(
            endpoint=SYSTEM_STATISTICS, payload=query_payload)
        df = pd.DataFrame(response.json().get("data"))
        try:
            return df[component].mean()
        except Exception:
            return -99

    def check_memory_cpu_util(self, device_ip: str, hostname: str, hours="24") -> pd.Series:
        cpu_avg = round(self.get_avg_component_util(
            component="cpu_user_new", device_ip=device_ip, hours=hours))
        mem_avg = round(self.get_avg_component_util(
            component="mem_util", device_ip=device_ip, hours=hours) * 100)
        data = {
            "device_ip": device_ip,
            "hostname": hostname,
            "cpu_avg": cpu_avg,
            "mem_avg": mem_avg
        }
        return pd.Series(data=data, index=["device_ip", "hostname", "cpu_avg", "mem_avg"])

    def get_all_devices(self) -> dict:
        devices = self.sdwan_bootcamp.get_request(
            endpoint="dataservice/system/device/vedges").json().get("data")
        return_obj = {REACHABLE: [], UNREACHABLE: []}
        for device in devices:
            if device.get(HOST_NAME) is not None and device.get(DEVICE_IP) is not None:
                return_obj[device[REACHABILITY]].append(
                    (device[DEVICE_IP], device[HOST_NAME]))
        return return_obj

    def check_all_devices_mem_cpu_util(self) -> pd.DataFrame:
        devices = self.get_all_devices()
        df = pd.DataFrame(
            columns=["device_ip", "hostname", "cpu_avg", "mem_avg"])
        for device in devices[REACHABLE]:
            df = df.append(self.check_memory_cpu_util(
                device[0], device[1]), ignore_index=True)
        return df


def main() -> None:
    vmanage_ip = "128.107.222.2"
    vmanage_port = "8443"
    vmanage_username = "admin"
    vmanage_password = getpass.getpass("vmanage password: ")
    vmanage_address = f"https://{vmanage_ip}:{vmanage_port}/"
    sdwan_bootcamp = SdwanBootcamp(vmanage_address=vmanage_address,
                                   vmanage_username=vmanage_username, vmanage_password=vmanage_password)
    avg_cpu_mem = AvgCpuMem(sdwan_bootcamp)
    df = avg_cpu_mem.check_all_devices_mem_cpu_util()
    print(df)


if __name__ == "__main__":
    main()
