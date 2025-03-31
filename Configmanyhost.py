from ncclient import manager

# รายละเอียดอุปกรณ์
routers = [
    {"host": "1.1.1.1", "port": 830, "username": "admin", "password": "cisco", "hostname": "TestR1"},
    {"host": "2.2.2.2", "port": 830, "username": "admin", "password": "cisco", "hostname": "TestR2"}
]

# เทมเพลต XML สำหรับการตั้งค่า hostname
hostname_template = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{hostname}</hostname>
    </native>
</config>
"""

def set_hostname(router):
    try:
        with manager.connect(
            host=router["host"],
            port=router["port"],
            username=router["username"],
            password=router["password"],
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            config_data = hostname_template.format(hostname=router["hostname"])
            response = m.edit_config(target="running", config=config_data)
            print(f"{router['host']}: Hostname changed to {router['hostname']}")
    except Exception as e:
        print(f"Error configuring {router['host']}: {e}")

# ตั้งค่า hostname สำหรับทุกอุปกรณ์
for router in routers:
    set_hostname(router)
