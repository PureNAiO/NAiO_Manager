import os
from pyzabbix.api import ZabbixAPI

## Note ##
# Interface Operational status: 1 is up, 2 is down

class Zabbix:
    def __init__(self, zabbix_url):
        # Create ZabbixAPI class instance
        self.zapi = ZabbixAPI(server=zabbix_url)
        self.zapi.login(api_token='b38f37bf1536fba3f7b591960ab63b51b3b20b5384af15aa8b55bacb55b3625b')
        self.inventory = {host['host']: host['hostid'] for host in self.zapi.host.get(monitored_hosts=1, output='extend')}
        self.data = {}

    def collector_host(self, device_name):
        host_id = self.inventory[device_name]
        result = self.zapi.item.get(hostids=host_id)
        metrics: dict = {info['itemid']: info['name'] for info in result}
        item_list = self.zapi.item.get(hostids=host_id, itemids=list(metrics.keys()))
        for info in item_list:
            item_id = info['itemid']
            item_name = metrics[item_id]
            item_lastvalue = info['lastvalue']
            if item_lastvalue.isdigit():
                value = int(info['lastvalue'])
                self.data[item_name] = value







