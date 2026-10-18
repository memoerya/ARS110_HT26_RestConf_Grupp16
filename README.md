# ARS110_HT26_RestConf_Grupp16

A CCNP1 project focused on using RESTCONF and Python to automate Cisco network configuration and verify network settings.

## Project Overview

This repository demonstrates how to interact with Cisco network devices using the RESTCONF API and Python automation scripts. The goal is to simplify repetitive configuration tasks, reduce manual errors, and validate that the network is configured as expected after changes are applied.

The project is intended for learning and practical automation of Cisco device configuration and verification using programmable network interfaces.

## Objectives

- Automate Cisco device configuration using RESTCONF
- Manage network settings through Python scripts
- Retrieve configuration and operational data from devices
- Validate network state after configuration changes
- Improve understanding of network automation workflows

## Technologies Used

- Python
- RESTCONF
- Cisco network devices
- HTTP/HTTPS requests
- JSON-based configuration payloads

## Prerequisites

Before using this project, make sure you have:

- Python 3.9 or later
- Access to a Cisco device with RESTCONF enabled
- Valid credentials for the device
- Network connectivity to the target device
- Python package manager (`pip`)

Install required dependencies:

```bash
pip install requests
```

If your project uses additional libraries, add them to a `requirements.txt` file.

## Repository Structure

```text
ARS110_HT26_RestConf_Grupp16/
├── README.md
├── requirements.txt
├── config/
│   └── device_config.json
├── scripts/
│   ├── get_interface_status.py
│   ├── configure_device.py
│   └── verify_network.py
├── tests/
│   └── test_examples.py
└── docs/
    └── notes.md
```

You can adjust this structure to match your actual project files.

## Configuration

Define the device connection details before running scripts. Example:

```python
DEVICE_IP = "192.168.1.10"
USERNAME = "admin"
PASSWORD = "your_password"
BASE_URL = f"https://{DEVICE_IP}/restconf"
```

Use secure handling for credentials, for example environment variables or a local config file.

## Example Usage

### 1. Connect to a device

```python
import requests
from requests.auth import HTTPBasicAuth

url = "https://192.168.1.10/restconf/data/ietf-interfaces:interfaces"
response = requests.get(
    url,
    auth=HTTPBasicAuth("admin", "your_password"),
    verify=False
)

print(response.status_code)
print(response.text)
```

### 2. Configure an interface

```python
payload = {
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet1",
        "description": "Configured by Python RESTCONF",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True
    }
}
```

### 3. Validate configuration

After applying changes, query the device to confirm the configuration was applied correctly and check operational status.

## Typical Workflow

1. Connect to the Cisco device over HTTPS
2. Authenticate using RESTCONF credentials
3. Send configuration payloads in JSON format
4. Retrieve device data and interface status
5. Verify changes by checking the returned configuration or operational output
6. Handle errors and retry when needed

## Security Notes

- Do not store credentials directly in source code
- Use environment variables or encrypted secrets where possible
- Restrict network access to trusted devices only
- Validate HTTPS certificates in production environments when appropriate

## Possible Use Cases

- Interface configuration
- VLAN setup
- Routing configuration
- Device verification
- Automation of repetitive network tasks
- Learning RESTCONF with Cisco devices

## Future Improvements

- Add command-line arguments for device settings
- Implement error handling and retry logic
- Add a structured logging system
- Support multiple devices
- Add unit tests for script validation
- Create a user-friendly configuration manager

## License

This project is for academic and learning purposes. Add an appropriate license if you plan to share or distribute it publicly.

## Author

Group 16  
ARS110_HT26_RestConf_Grupp16

## Notes

This repository is intended as a practical networking automation project using Python and RESTCONF. You can expand it with your actual scripts, device configurations, and validation logic as the project develops.
