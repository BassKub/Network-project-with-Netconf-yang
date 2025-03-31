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

        with open("Lab1-config.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

        print("Config Saved")

if __name__ == "__main__":
    interface_config = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <GigabitEthernet>
                    <name>0/0/0</name>
                    <shutdown operation="delete"/>
                    <description>Configured by NETCONF</description>
                    <ip>
                        <address>
                            <primary>
                                <address>192.168.1.1</address>
                                <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                    </ip>
                </GigabitEthernet>
            </interface>
        </native>
    </config>
    """

    edit_config(interface_config)

    get_config()