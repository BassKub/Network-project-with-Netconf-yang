from ncclient import manager
import xml.dom.minidom

host='192.168.100.1'
user='admin'
password='cisco'

def edit_config(nc):
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        m.edit_config(target="running", config=nc)
    print("Configuration Updated")

def get_config():
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        config = m.get_config(source="running").data_xml

        pretty_config = xml.dom.minidom.parseString(config).toprettyxml(indent="  ")

        with open("Lab2-config.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

        print("Config Saved")

if __name__ == "__main__":
    hostname_config = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>Test1234</hostname>
        </native>
    </config>
    """

    edit_config(hostname_config)
    
    get_config()