import json, requests
from utils import parsing


class Rpc:
    def __init__(self):
        config = parsing.parse_json('config.json')["rpc"]

        self.rpc_host = config["rpc_host"]
        self.rpc_port = config["rpc_port"]
        self.rpc_user = config["rpc_user"]
        self.rpc_pass = config["rpc_pass"]
        self.serverURL = 'http://' + self.rpc_host + ':' + self.rpc_port
        self.headers = {'content-type': 'application/json'}

    def listtransactions(self, params, count):
        payload = json.dumps({"method": "listtransactions", "params": [params, count], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']

    def getblockchaininfo(self):
        payload = json.dumps({"method": "getblockchaininfo", "params": [], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']

    def getconnectioncount(self):
        payload = json.dumps({"method": "getconnectioncount", "params": [], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']

    def getinfo(self):
        payload = json.dumps({"method": "getinfo", "params": [], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']

    def getnextsuperblock(self):
        payload = json.dumps({"method": "getnextsuperblock", "params": [], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']
		
    def getbudgetprojection(self):
        payload = json.dumps({"method": "getbudgetprojection", "params": [], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']
		
    def getbudgetinfo(self):
        payload = json.dumps({"method": "getbudgetinfo", "params": [], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']
		
    def validateaddress(self, params):
        payload = json.dumps({"method": "validateaddress", "params": [params], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']

    def getaccountaddress(self, account):
        payload = json.dumps({"method": "getaccountaddress", "params": [account], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']

    def sendfrom(self, account, address, amount):
        print ("in rpc")
        payload = json.dumps({"method": "sendfrom", "params": [account, address, amount], "jsonrpc": "2.0"})
        print (payload)
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        print (response)
        return response.json()['result']

    def sendmany(self, account, payments):
        payload = json.dumps({"method": "sendmany", "params": [account, payments], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']
		
    def sendtoaddress(self, address, amount):
        payload = json.dumps({"method": "sendtoaddress", "params": [address, amount], "jsonrpc": "2.0"})
        response = requests.get(self.serverURL, headers=self.headers, data=payload,
                                auth=(self.rpc_user, self.rpc_pass))
        return response.json()['result']
