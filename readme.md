# Netmiko: Various Network CLI Uses
Netmiko is excellent at performing network automation across CLI-based devices. When REST APIs are unavailable, Netmiko is an excellent second option.

# How-to Use
## Encryption / Fernet
1. Create a Python file that you will run.
2. For any credentials / secure strings, create a symmetric encryption key and use the included `decrypt()` function within `Functions/decryption.py` to decrypt the strings. Run the below in an interactive Python shell to obtain your ciphertexts. You should then store the ciphertext within your file, and then call `decrypt(ciphertext)` to obtain the plaintext.

```py
from cryptography.fernet import Fernet
key = Fernet.generate_key()
with open("Functions/encryptionKey.txt","w") as encryptionKeyFile:
    encryptionKeyFile.write(key.decode("UTF-8"))

cipher = Fernet(key)
while True:
    cipherText = cipher.encrypt(input("Input your plaintext string to encrypt (submit \"q\" to exit)").encode("UTF-8"))
    if not cipherText.lower() == "q":
        print("Here is your ciphertext: " + cipherText)
    else:
        break
```

## Inventory
Create an inventory of devices using `inventory.py`. 

- Define an inventory of devices with a hostname and IP address, and if you're not using Cisco IOS devices, a platform as well. I have Netbox as my SSOT / inventory system. You can make one out of YAML, or whatever else you prefer. 
- Create one Device() object for every device you want to run commands against.
  - Once again, ensure that your [platform](http://ktbyers.github.io/netmiko/PLATFORMS.html), hostname, IP address, and authentication credentials are configured properly.

`inventory.py`: 

```py
import inquirer

class Device:
    def __init__(self,*,hostname, ipAddress, platform = "cisco_ios"):
        self.hostname = hostname
        self.ipAddress = ipAddress.split("/")[0]
        self.username = b'Your ciphertext username'
        self.password = b'Your ciphertext password'
        self.platform = platform
```

## Netmiko
Develop your Netmiko function that will apply to each device independently. This will include converting device objects to Netmiko device dictionaries.

Example `getConfig()`:

```py
def getConfig(switch):
    netmikoDevice = {
        "host":switch.ipAddress,
        "username":switch.username,
        "password":switch.password,
        "device_type":switch.platform
    }

    try:
        # Log into the device via SSH!
        with ConnectHandler(**netmikoDevice) as sshSession:
            return [switch.hostname, sshSession.send_command("show run | s line vty")]
    
    except NetmikoTimeoutException as e:
        return ["ERROR: NetmikoTimeoutException on " + switch.hostname + "\n\t" + e]
    except Exception as e:
        return ["ERROR: Exception on " + switch.hostname + "\n\t" + e]
```

## Multithreading
Bring it all together with multithreading using `concurrent.futures`.

Example `main()`:

```py
from Functions.decryption import decrypt
from Functions.inventory import Device
from netmiko import ConnectHandler, NetmikoTimeoutException
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Obtain all target devices. The `devices` variable is an array (List) of Device() objects from `inventory.py`.
devices = obtainDevices()

# Decrypt the credentials at runtime
for device in devices:
    device.username = decrypt(switch.username)
    device.password = decrypt(switch.password)

# Create a log file
with open("Logs/" + datetime.now().strftime("%Y-%m-%d_%Hh%Mm") + "_lineVTY.txt","w") as outputFile:
    # Create a multithreaded process
    with ThreadPoolExecutor(max_workers=10) as execution:
        results = {execution.submit(getConfig, device): device for device in devices}
        for thread in as_completed(results):
            # thread.result() is the results from the Netmiko command sent to the device.
            print(outputFile.write(thread.result())
```

