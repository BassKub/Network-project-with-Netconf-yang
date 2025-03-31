from ncclient import manager
import xml.dom.minidom

DEVICE = {
    "host": "192.168.100.2", 
    "port": 830,          
    "username": "admin",   
    "password": "cisco",  
    "hostkey_verify": False, 
}

def connect_to_device():
    return manager.connect(**DEVICE, timeout=30)

def get_config():
    with connect_to_device() as m:
        config = m.get_config(source="running").data_xml
        
        pretty_config = xml.dom.minidom.parseString(config).toprettyxml(indent="  ")

        with open("Lab6-config-R2.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

        print("Config Saved")

def filter_config(xpath):
    with connect_to_device() as m:
        filter_criteria = f"<filter>{xpath}</filter>"
        config = m.get_config(source="running", filter=filter_criteria).data_xml
        print("### Filtered Configuration ###")
        print(config)

def edit_config(xml_config):
    with connect_to_device() as m:
        response = m.edit_config(target="running", config=xml_config)
        print("### Edit Config Response ###")
        print(response)

        save_response = m.copy_config(source="running", target="startup")
        print("### Save Config Response ###")
        print(save_response)

if __name__ == "__main__":

    #filter_config('<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"><interface/></native>')


    Basic_route_R2 = """
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                    <GigabitEthernet>
                        <name>0/0/0</name>
                        <shutdown operation="delete"/>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.20</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>20</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.20.1</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.30</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>30</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.30.2</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                </interface>
                <ip>
                    <route>
                        <ip-route-interface-forwarding-list>
                        <prefix>192.168.10.0</prefix>
                        <mask>255.255.255.0</mask>
                        <fwd-list>
                            <fwd>192.168.30.1</fwd>
                        </fwd-list>
                        </ip-route-interface-forwarding-list>
                    </route>
                </ip>
            </native>
        </config>
    """

    #edit_config(Basic_route_R2)

    get_config()
