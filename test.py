from ncclient import manager
from lxml import etree

# Define NETCONF connection parameters
host = '192.168.20.3'
port = 830
username = 'admin'
password = 'cisco'

# New hostname you want to set
new_hostname = "NewRouterName"

# Create NETCONF connection
with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as m:
    
    # XML payload for edit-config operation to change hostname
    config_payload = f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>{new_hostname}</hostname>
        </native>
    </config>
    """
    
    # Send the edit-config request to change the hostname
    response = m.edit_config(target="running", config=config_payload)
    print(response)
