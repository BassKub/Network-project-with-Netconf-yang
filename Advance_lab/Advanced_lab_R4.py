from ncclient import manager
import xml.dom.minidom

DEVICE = {
    "host": "192.168.100.4",  
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

        with open("Lab8-config-R4.txt", "w", encoding="utf-8") as file:
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

    R4_config = """
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>R4</hostname>
                <ip>
                    <dhcp>
                        <excluded-address xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                            <low-high-address-list>
                                <low-address>192.168.4.1</low-address>
                                <high-address>192.168.4.10</high-address>
                            </low-high-address-list>
                        </excluded-address>
                        <pool xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                            <id>1</id>
                            <default-router>
                                <default-router-list>192.168.4.1</default-router-list>
                            </default-router>
                            <network>
                                <primary-network>
                                <number>192.168.4.1</number>
                                <mask>255.255.255.0</mask>
                                </primary-network>
                            </network>
                        </pool>
                    </dhcp>
                </ip>
                <interface>
                    <GigabitEthernet>
                        <name>0/0/0</name>
                        <shutdown operation="delete"/>
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
                    <GigabitEthernet>
                        <name>0/0/0.40</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>40</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.40.2</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.70</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>70</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.70.1</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.400</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>400</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.4.1</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <Loopback>
                        <name>0</name>
                        <ip>
                        <address>
                            <primary>
                            <address>4.4.4.4</address>
                            <mask>255.255.255.255</mask>
                            </primary>
                        </address>
                        </ip>
                    </Loopback>
                </interface>
                <router>
                <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                    <ospf>
                        <process-id>
                        <id>1</id>
                        <network>
                            <ip>4.4.4.4</ip>
                            <wildcard>0.0.0.0</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.30.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.40.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.70.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.4.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        </process-id>
                    </ospf>
                    </router-ospf>
                </router>
            </native>
        </config>
    """

    #edit_config(R4_config)

    get_config()
