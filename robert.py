import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = "admin"
password = "cisco"


# TOPOLOGY
routers = {
    "ISP": {
        "mgmt": "100.100.100.1",
        "interface": "192.168.12.1",
        "loop_nr": 1,
        "loop_ip": "172.16.0.1",
        "router_id": "1.1.1.1",
        "priority": 0,
        "routes": ["172.17.0.1", "172.18.0.1", "12.12.12.12"]
    },

    "STO": {
        "mgmt": "100.100.100.2",
        "interface": "192.168.12.2",
        "loop_nr": 2,
        "loop_ip": "172.17.0.1",
        "router_id": "2.2.2.2",
        "priority": 255,
        "routes": ["172.16.0.1", "172.18.0.1", "12.12.12.12", "0.0.0.0"]
    },

    "GBG": {
        "mgmt": "100.100.100.3",
        "interface": "192.168.12.3",
        "loop_nr": 3,
        "loop_ip": "172.18.0.1",
        "router_id": "3.3.3.3",
        "routes": ["172.16.0.1", "172.17.0.1", "0.0.0.0"]
    }
}

headers = {
    "Accept": "application/yang-data+json"
}

fel = 0


# RESTCONF GET
def get(router, path):

    url = f"https://{routers[router]['mgmt']}/restconf/data/{path}"

    try:
        svar = requests.get(
            url,
            auth=(username, password),
            headers=headers,
            verify=False,
            timeout=10
        )

        if svar.status_code == 200:
            return svar.json()

    except requests.exceptions.RequestException:
        pass

    return None


# RESULTAT
def resultat(ok, text):

    global fel

    print(f"[{'✓' if ok else '✕'}] {text}")

    if not ok:
        fel += 1


# HOSTNAME
def kolla_hostname(router):

    data = get(
        router,
        "Cisco-IOS-XE-native:native/hostname"
    )

    ok = (
        data is not None
        and data.get("Cisco-IOS-XE-native:hostname") == router
    )

    resultat(ok, f"{router}: hostname {router}")


# INTERFACE
def kolla_interface(router, namn, ratt_ip):

    path = (
        "ietf-interfaces:interfaces/interface="
        + namn.replace("/", "%2F")
    )

    data = get(router, path)

    resultat(
        data is not None and ratt_ip in str(data),
        f"{router}: {namn} -> {ratt_ip}"
    )


# LOOPBACK
def kolla_loopback(router, nummer, ratt_ip):

    data = get(
        router,
        "Cisco-IOS-XE-native:native/interface"
    )

    hittad = False

    if data:
        loopbacks = (
            data
            .get("Cisco-IOS-XE-native:interface", {})
            .get("Loopback", [])
        )

        for loop in loopbacks:
            if loop.get("name") == nummer:

                ip = (
                    loop.get("ip", {})
                    .get("address", {})
                    .get("primary", {})
                    .get("address")
                )

                hittad = ip == ratt_ip

    resultat(
        hittad,
        f"{router}: Loopback{nummer} -> {ratt_ip}"
    )


# OSPF
def kolla_ospf(router, router_id):

    data = get(
        router,
        "Cisco-IOS-XE-native:native/router"
    )

    text = str(data)

    ok = (
        data is not None
        and "'id': 1" in text
        and router_id in text
        and "'area': 0" in text
    )

    resultat(
        ok,
        f"{router}: OSPF 1 area 0 | router-id {router_id}"
    )


# OSPF PRIORITY / COST
def kolla_ospf_interface(router, interface, value, expected):

    data = get(
        router,
        "Cisco-IOS-XE-native:native/interface"
    )

    hittad = False

    if data:
        portar = (
            data
            .get("Cisco-IOS-XE-native:interface", {})
            .get("GigabitEthernet", [])
        )

        for port in portar:
            if port.get("name") == interface:

                ospf = (
                    port.get("ip", {})
                    .get("Cisco-IOS-XE-ospf:router-ospf", {})
                    .get("ospf", {})
                )

                hittad = ospf.get(value) == expected

    resultat(
        hittad,
        f"{router}: OSPF {value} {expected} på Gi{interface}"
    )


# DEFAULT ROUTE
def kolla_default(router, loopback):

    data = get(
        router,
        "Cisco-IOS-XE-native:native/ip/route"
    )

    text = str(data)

    resultat(
        data is not None
        and "0.0.0.0" in text
        and loopback in text,
        f"{router}: default route -> {loopback}"
    )


# ROUTING TABLE
def kolla_route(router, route):

    data = get(
        router,
        "Cisco-IOS-XE-fib-oper:fib-oper-data"
    )

    resultat(
        data is not None and route in str(data),
        f"{router}: route {route}"
    )


# CHECK ALL ROUTERS
for router, info in routers.items():

    print(f"\n.·:*¨༺ {router} ༻¨*:·.")

    kolla_hostname(router)

    kolla_interface(
        router,
        "GigabitEthernet0/0/0",
        info["interface"]
    )

    kolla_loopback(
        router,
        info["loop_nr"],
        info["loop_ip"]
    )

    kolla_ospf(
        router,
        info["router_id"]
    )

    for route in info["routes"]:
        kolla_route(router, route)


# SPECIAL REQUIREMENTS
kolla_ospf_interface(
    "ISP",
    "0/0/0",
    "priority",
    0
)

kolla_default(
    "ISP",
    "Loopback1"
)

kolla_ospf_interface(
    "STO",
    "0/0/0",
    "priority",
    255
)

kolla_interface(
    "GBG",
    "GigabitEthernet0/0/1",
    "12.12.12.13"
)

kolla_ospf_interface(
    "GBG",
    "0/0/1",
    "cost",
    14
)


# RESULTAT
print("\n.·:*¨¨* ≈☆≈ *¨¨*:·.")

if fel == 0:
    print("𝓑𝓻𝓪 𝓳𝓸𝓫𝓫𝓪𝓽! 𝓐𝓵𝓵𝓽 𝓼𝓮𝓻 𝓻ä𝓽𝓽 𝓾𝓽 𝓽𝓳𝓮𝓳𝓮𝓻 :)")
else:
    print(f"𝓗ä𝓻 𝓱𝓪𝓻 𝓷𝓲 𝓰𝓳𝓸𝓻𝓽 𝓯𝓮𝓵, 𝓪𝓳𝓪 𝓫𝓪𝓳𝓪! :( ({fel} 𝓯𝓮𝓵 𝓱𝓲𝓽𝓽𝓪𝓭𝓮𝓼)")

print(".·:*¨¨* ≈☆≈ *¨¨*:·.")
