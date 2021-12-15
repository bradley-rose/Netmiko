# Connection Handler
from netmiko import Netmiko
from getpass import getpass
import csv

deviceUsername = getpass(prompt='Username: ')
devicePassword = getpass(prompt='Password: ')

device = {
    'username':deviceUsername,
    'password':devicePassword,
    'secret':devicePassword,
    'device_type':'cisco_asa',
    'session_log': 'troubleshooting.txt'
}

with open('asas.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    line_count=0
    for row in reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count +=1
        else:
            device['host'] = row['Management IP']
            connection = Netmiko(**device)
            print(row)
            print(connection.send_command('show version | grep Serial'))