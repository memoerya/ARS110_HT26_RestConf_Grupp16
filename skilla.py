import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("⋘ 𝓛𝓸𝓪𝓭𝓲𝓷𝓰 𝓭𝓪𝓽𝓪... ⋙")
print("⋘██ 20% *___* ⋙")


# LOGIN + TOPOLOGY
username = "admin"
password = "cisco"

routers = {
    "ISP": {
        "mgmt": "100.100.100.1",
        "lan_ip": "192.168.12.1",
        "loopback": "172.16.0.1",
        "loopback_number": 1,
        "router_id": "1.1.1.1",
        "networks": [
            ("192.168.12.0", "0.0.0.255"),
            ("172.16.0.0", "0.0.255.255")
        ]
    },

    "STO": {
        "mgmt": "100.100.100.2",
        "lan_ip": "192.168.12.2",
        "loopback": "172.17.0.1",
        "loopback_number": 2,
        "router_id": "2.2.2.2",
        "networks": [
            ("192.168.12.0", "0.0.0.255"),
            ("172.17.0.0", "0.0.255.255")
        ]
    },

    "GBG": {
        "mgmt": "100.100.100.3",
        "lan_ip": "192.168.12.3",
        "loopback": "172.18.0.1",
        "loopback_number": 3,
        "router_id": "3.3.3.3",
        "networks": [
            ("192.168.12.0", "0.0.0.255"),
            ("172.18.0.0", "0.0.255.255"),
            ("12.12.12.12", "0.0.0.3")
        ]
    }
}

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# RESTCONF PATCH
def patch(router, path, data, text):

    url = f"https://{routers[router]['mgmt']}/restconf/data/{path}"

    try:
        response = requests.patch(
            url,
            auth=(username, password),
            headers=headers,
            json=data,
            verify=False,
            timeout=10
        )

        if response.status_code in (200, 201, 204):
            print(f"[𝓓𝓞𝓝𝓔] {router}: {text}")
        else:
            print(f"[𝓔𝓡𝓡𝓞𝓡] {router}: {text}")
            print("HTTP:", response.status_code)
            print(response.text)

    except requests.exceptions.RequestException as error:
        print(f"[FEL] {router}: {error}")



# HOSTNAME
def hostname(router):

    data = {
        "Cisco-IOS-XE-native:hostname": router
    }

    patch(
        router,
        "Cisco-IOS-XE-native:native/hostname",
        data,
        f"hostname {router}"
    )


# INTERFACE
def interface(router, name, ip, mask, description):

    path = (
        "ietf-interfaces:interfaces/interface="
        + name.replace("/", "%2F")
    )

    data = {
        "ietf-interfaces:interface": {
            "name": name,
            "description": description,
            "enabled": True,

            "ietf-ip:ipv4": {
                "address": [{
                    "ip": ip,
                    "netmask": mask
                }]
            }
        }
    }

    patch(
        router,
        path,
        data,
        f"{name} -> {ip} | no shutdown"
    )


# LOOPBACK
def loopback(router, number, ip):

    data = {
        "Cisco-IOS-XE-native:interface": {
            "Loopback": [{
                "name": number,
                "ip": {
                    "address": {
                        "primary": {
                            "address": ip,
                            "mask": "255.255.0.0"
                        }
                    }
                }
            }]
        }
    }

    patch(
        router,
        "Cisco-IOS-XE-native:native/interface",
        data,
        f"Loopback{number} -> {ip}/16"
    )


# OSPF
def ospf(router):

    info = routers[router]

    network_list = []

    for network, wildcard in info["networks"]:
        network_list.append({
            "ip": network,
            "wildcard": wildcard,
            "area": 0
        })

    data = {
        "Cisco-IOS-XE-native:router": {
            "Cisco-IOS-XE-ospf:router-ospf": {
                "ospf": {
                    "process-id": [{
                        "id": 1,
                        "router-id": info["router_id"],
                        "network": network_list
                    }]
                }
            }
        }
    }

    patch(
        router,
        "Cisco-IOS-XE-native:native/router",
        data,
        f"OSPF 1 area 0 | router-id {info['router_id']}"
    )


# OSPF PRIORITY
def ospf_priority(router, priority):

    data = {
        "Cisco-IOS-XE-native:interface": {
            "GigabitEthernet": [{
                "name": "0/0/0",
                "ip": {
                    "Cisco-IOS-XE-ospf:router-ospf": {
                        "ospf": {
                            "priority": priority
                        }
                    }
                }
            }]
        }
    }

    patch(
        router,
        "Cisco-IOS-XE-native:native/interface",
        data,
        f"OSPF priority {priority} på Gi0/0/0"
    )


# OSPF COST
def ospf_cost(router, cost):

    data = {
        "Cisco-IOS-XE-native:interface": {
            "GigabitEthernet": [{
                "name": "0/0/1",
                "ip": {
                    "Cisco-IOS-XE-ospf:router-ospf": {
                        "ospf": {
                            "cost": cost
                        }
                    }
                }
            }]
        }
    }

    patch(
        router,
        "Cisco-IOS-XE-native:native/interface",
        data,
        f"OSPF cost {cost} på Gi0/0/1"
    )


# DEFAULT ROUTE + OSPF DEFAULT
def default_route():

    data = {
        "Cisco-IOS-XE-native:route": {
            "ip-route-interface-forwarding-list": [{
                "prefix": "0.0.0.0",
                "mask": "0.0.0.0",
                "fwd-list": [{
                    "fwd": "Loopback1"
                }]
            }]
        }
    }

    patch(
        "ISP",
        "Cisco-IOS-XE-native:native/ip/route",
        data,
        "default route -> Loopback1"
    )


def default_information():

    data = {
        "Cisco-IOS-XE-native:router": {
            "Cisco-IOS-XE-ospf:router-ospf": {
                "ospf": {
                    "process-id": [{
                        "id": 1,
                        "default-information": {
                            "originate": {}
                        }
                    }]
                }
            }
        }
    }

    patch(
        "ISP",
        "Cisco-IOS-XE-native:native/router",
        data,
        "default-information originate"
    )


# CONFIGURE ALL THREE ROUTERS
for router in ["ISP", "STO", "GBG"]:

    info = routers[router]

    print(f"\n.·:*¨༺  {router} ༻¨*:·.")

    hostname(router)

    interface(
        router,
        "GigabitEthernet0/0/0",
        info["lan_ip"],
        "255.255.255.0",
        "Till-Switch"
    )

    loopback(
        router,
        info["loopback_number"],
        info["loopback"]
    )

    ospf(router)


# SPECIAL REQUIREMENTS

# ISP får aldrig bli DR/BDR
ospf_priority("ISP", 0)

# STO ska ha högsta möjliga priority
ospf_priority("STO", 255)

# GBG -> PC
interface(
    "GBG",
    "GigabitEthernet0/0/1",
    "12.12.12.13",
    "255.255.255.252",
    "Till-PC"
)

# OSPF cost till PC = 14
ospf_cost("GBG", 14)

# Default route finns bara på ISP
default_route()

# ISP annonserar default route via OSPF
default_information()


# KLAR
print("\n‿︵‿︵୨˚̣̣̣͙୧ - - ୨˚̣̣̣͙୧‿︵‿︵ ")
print("⋘ 𝓒𝓸𝓷𝓰𝓻𝓪𝓽𝓼! 𝓒𝓸𝓷𝓯𝓲𝓰𝓾𝓻𝓪𝓽𝓲𝓸𝓷 𝓭𝓸𝓷𝓮 :) ⋙")
print("‿︵‿︵୨˚̣̣̣͙୧ - - ୨˚̣̣̣͙୧‿︵‿︵ ")
