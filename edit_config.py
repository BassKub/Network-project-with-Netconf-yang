from ncclient import manager

host='192.168.20.3'
user='admin'
password='cisco'

def edit_config(nc):
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        m.edit_config(target="running", config=nc)
    print("Configuration Updated")

if __name__ == "__main__":
    new_config = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <GigabitEthernet>
                    <name>0/0/0</name>
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

    edit_config(new_config)