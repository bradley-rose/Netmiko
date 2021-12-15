# Connection Handler
from netmiko import Netmiko
from getpass import getpass

devicePassword = getpass()

device = {
    'username':'cisco',
    'password':devicePassword,
    'device_type':'cisco_asa'
}

devices = ('addressA','addressB','addressC')
for x in devices:
    device['host'] = x
    print(device['host'])
    print(devicePassword)


""" connection = Netmiko(**device)
connection.enable('cisco')
print(connection.find_prompt())
print(connection.send_command('show version | grep Serial')) """