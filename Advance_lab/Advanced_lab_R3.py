#ncclient เป็นไลบรารี Python ที่ใช้สำหรับติดต่อกับอุปกรณ์เครือข่ายผ่าน
#manager เป็นโมดูลหลักของ ncclient ที่ใช้สำหรับเปิดการเชื่อมต่อกับอุปกรณ์และจัดการค่าคอนฟิก
from ncclient import manager

#นำเข้าไลบรารีสำหรับการจัดการ XML
import xml.dom.minidom

# กำหนดตัวแปรที่ใช้ในการเชื่อมต่ออุปกรณ์ NETCONF
DEVICE = {
    "host": "192.168.100.3",  
    "port": 830,        
    "username": "admin",     
    "password": "cisco",  
    "hostkey_verify": False, 
}

# ฟังก์ชันสำหรับเชื่อมต่ออุปกรณ์โดยใช้ ncclient
# ใช้ **DEVICE เพื่อแตกค่าพารามิเตอร์ออกจาก dictionary
# timeout=30 กำหนดเวลาหมดอายุของการเชื่อมต่อเป็น 30 วินาที
def connect_to_device():
    return manager.connect(**DEVICE, timeout=30)

# ฟังก์ชันสำหรับดึงค่าคอนฟิกจากอุปกรณ์
# บันทึกค่าคอนฟิกที่ดึงมาในไฟล์ Lab5-config.txt
def get_config():
    with connect_to_device() as m:
        config = m.get_config(source="running").data_xml # ดึง Running Configuration

        #ใช้ xml.dom.minidom เพื่อทำให้การกำหนดค่าที่ดึงมาอ่านง่ายขึ้น
        pretty_config = xml.dom.minidom.parseString(config).toprettyxml(indent="  ")

        #บันทึกการกำหนดค่าที่อ่านง่ายลงในไฟล์ Lab5-config.txt
        with open("Lab8-config-R3.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

        print("Config Saved")

# ฟังก์ชันสำหรับดึงค่าคอนฟิกบางส่วนโดยใช้ XPath filter
def filter_config(xpath):
    with connect_to_device() as m:
        filter_criteria = f"<filter>{xpath}</filter>"
        config = m.get_config(source="running", filter=filter_criteria).data_xml
        print("### Filtered Configuration ###")
        print(config)

# ฟังก์ชันสำหรับแก้ไขค่าคอนฟิกของอุปกรณ์ผ่าน NETCONF
def edit_config(xml_config):
    with connect_to_device() as m:
        response = m.edit_config(target="running", config=xml_config)# ส่งค่า config ใหม่ไปยัง running-config
        print("### Edit Config Response ###")
        print(response)

        # บันทึกค่าคอนฟิกที่แก้ไขไปยัง startup-config
        save_response = m.copy_config(source="running", target="startup")
        print("### Save Config Response ###")
        print(save_response)

if __name__ == "__main__":

    #filter_config('<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"><interface/></native>')
   
    R3_config = """
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>R3</hostname>
                <ip>
                    <dhcp>
                        <excluded-address xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                            <low-high-address-list>
                                <low-address>192.168.3.1</low-address>
                                <high-address>192.168.3.10</high-address>
                            </low-high-address-list>
                        </excluded-address>
                        <pool xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                            <id>1</id>
                            <default-router>
                                <default-router-list>192.168.3.1</default-router-list>
                            </default-router>
                            <network>
                                <primary-network>
                                <number>192.168.3.1</number>
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
                        <name>0/0/0.10</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>10</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.10.2</address>
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
                            <address>192.168.40.1</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.80</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>80</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.80.1</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.300</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>300</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.3.1</address>
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
                            <address>3.3.3.3</address>
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
                            <ip>3.3.3.3</ip>
                            <wildcard>0.0.0.0</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.10.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.40.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.80.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.3.0</ip>
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
    #เรียกใช้ฟังก์ชัน edit_config เพื่อแก้ไขการกำหนดค่าของอินเตอร์เฟซ
    #edit_config(R3_config)

    #เรียกใช้ฟังก์ชัน get_config เพื่อดึงการกำหนดค่าจากอุปกรณ์
    get_config()
