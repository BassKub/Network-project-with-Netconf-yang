from ncclient import manager
from xml.dom.minidom import parseString

host='192.168.20.3'
user='admin'
password='cisco'

def get_config():
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        running_config = m.get_config(source='running').data_xml
        pretty_config = parseString(running_config).toprettyxml(indent="  ")
        print("Retrieved Configuration (Formatted):")

        with open("running_config(new).txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

def filter_config(fc):
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        config = m.get_config(source="running", filter=fc)
        pretty_config = parseString(config.xml).toprettyxml()
        print(pretty_config)

if __name__ == "__main__":
    filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <GigabitEthernet>
                    <name>0/0/0</name>
                </GigabitEthernet>
            </interface>
        </native>
    </filter>
    """
    filter_config(filter)
    #get_config()
    
    