import inquirer

class Device:
    def __init__(self,*,hostname, ipAddress):
        self.hostname = hostname
        self.ipAddress = ipAddress.split("/")[0]
        self.username = b'gAAAAABk8kz_p1Elk_xshp9TC5xeTP09vYauN3FI6qinaNcDoN5CA7Mn3eEWU8sX1bYiXDSs-cT0qBsSPfUup-YsGgAL6V_ztw=='
        self.password = b'gAAAAABk8k1Ue_ab_laEBmRVlGApnosii9AAu2WvucX4w_i1N2wSPT01kEYsX0LQ68-rGBQSSQCJ92FQMzI3ULUr4cJK-UQ-qirHKHWDXJwJHEC3W1P9nNg='
        self.platform = "cisco_ios"

def deviceInclusion(devices):
    listOfDeviceNames = []
    listOfDeviceObjects = []
    for device in devices:
        listOfDeviceNames.append(device.hostname)

    questions = [
        inquirer.Checkbox(
            name = "Approved",
            message = "Select the devices to run against. Spacebar to toggle, Enter to confirm.",
            choices=listOfDeviceNames
        )
    ]
    for device in inquirer.prompt(questions)["Approved"]:
        for x in devices:
            if device == x.hostname:
                listOfDeviceObjects.append(x)
    return listOfDeviceObjects