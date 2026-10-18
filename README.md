# ARS110_HT26_RestConf_Grupp16

CCNP1 project using RESTCONF and Python to automate Cisco network configuration and verify network settings.

## Overview

This repository contains Python-based automation scripts for interacting with Cisco network devices using RESTCONF. The goal is to simplify configuration tasks and verify that the applied settings match the expected network state.

## Repository Structure

```text
ARS110_HT26_RestConf_Grupp16/
├── LICENSE
├── README.md
├── robert.py
├── skilla.py
```

## Files

- `robert.py` – Python script for RESTCONF automation and device interaction
- `skilla.py` – Python script for additional automation and network verification tasks
- `LICENSE` – MIT license for the project

## Requirements

- Python 3
- Access to a Cisco device with RESTCONF enabled
- Valid credentials for the device
- Network connectivity to the target device

Optional dependency:

```bash
pip install requests
```

## Usage

Run the scripts from the repository root:

```bash
python robert.py
python skilla.py
```

Make sure your device connection details and authentication information are configured correctly before running the scripts.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Notes

This repository is intended for learning and practical automation of Cisco network configuration using RESTCONF and Python. It can be expanded with additional scripts and validation logic as the project grows.
