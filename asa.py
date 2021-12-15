# Import Netmiko library for network automation
from netmiko import Netmiko
# Import getpass to pass credentials with no output shown to the terminal
from getpass import getpass
# Import CSV tools
import csv

# Prompt for credentials locally at the terminal
deviceUsername = getpass(prompt='Username: ')
devicePassword = getpass(prompt='Password: ')

# Create a device object with the required properties for Netmiko. 
# Assumption for enable password is that it is identical to the user's password. Change this if this does not apply to you.
# Outputs a running log of ALL output from the interaction between Netmiko and the target Cisco ASA to `./troubleshooting.txt`
device = {
    'username':deviceUsername,
    'password':devicePassword,
    'secret':devicePassword,
    'device_type':'cisco_asa',
    'session_log': 'troubleshooting.txt'
}

# Open the CSV and read it.
with open('asas.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    # Set a line_count variable to 0 because you need to differentiate between the CSV's column headers and the actual items.
    # Ex. Row 0 contains "Management IP". Row 1 -> EOF is expected to be IP addresses. You can't SSH to "Management IP".
    line_count=0
    for row in reader:
        if line_count == 0:
            # Print out the column headers to the terminal.
            print(f'Column names are {", ".join(row)}')
            line_count +=1
        else:
            # Add the target IP address to the Netmiko object.
            device['host'] = row['Management IP']
            # Establish the connection through Netmiko.
            connection = Netmiko(**device)
            # Print out the CSV row in order to keep track of the outputs.
            print(row)
            # Remotely inserts the "show version | grep Serial" command and presents the output to the terminal.
            print(connection.send_command('show version | grep Serial'))

# EOF marks a closing of the SSH session.