from ncclient import manager
import xml.dom.minidom

# กำหนดข้อมูลอุปกรณ์ NETCONF
DEVICE = {
    "host": "192.168.100.30",  # เปลี่ยนเป็น IP ของอุปกรณ์จริง
    "port": 830,            # พอร์ตเริ่มต้นของ NETCONF
    "username": "admin",     # เปลี่ยนเป็น username จริง
    "password": "cisco",  # เปลี่ยนเป็น password จริง
    "hostkey_verify": False, # ปิดการตรวจสอบ hostkey (สำหรับ lab)
}

def connect_to_device():
    """สร้างการเชื่อมต่อกับอุปกรณ์ NETCONF"""
    return manager.connect(**DEVICE, timeout=30)

def get_config():
    """ดึงค่าคอนฟิกทั้งหมดและบันทึกเป็นไฟล์ txt"""
    with connect_to_device() as m:
        config = m.get_config(source="running").data_xml
        
        # จัดรูปแบบ XML ให้สวยงาม
        pretty_config = xml.dom.minidom.parseString(config).toprettyxml(indent="  ")

        # บันทึกลงไฟล์
        with open("netconf_config.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

        print("✅ คอนฟิกถูกบันทึกลงไฟล์: netconf_config.txt")

def filter_config(xpath):
    """ดึงค่าคอนฟิกเฉพาะส่วนที่ต้องการ (ใช้ XPath)"""
    with connect_to_device() as m:
        filter_criteria = f"<filter>{xpath}</filter>"
        config = m.get_config(source="running", filter=filter_criteria).data_xml
        print("### Filtered Configuration ###")
        print(config)

def edit_config(xml_config):
    """แก้ไขค่าคอนฟิกโดยส่ง XML"""
    with connect_to_device() as m:
        response = m.edit_config(target="running", config=xml_config)
        print("### Edit Config Response ###")
        print(response)

        save_response = m.copy_config(source="running", target="startup")
        print("### Save Config Response ###")
        print(save_response)

def delete_config(target="running"):
    """ลบค่าคอนฟิก (เฉพาะ startup หรือ candidate)"""
    if target not in ["startup", "candidate"]:
        print("Error: สามารถลบได้เฉพาะ startup หรือ candidate เท่านั้น")
        return
    with connect_to_device() as m:
        response = m.delete_config(target=target)
        print("### Delete Config Response ###")
        print(response)

# ----------------------- ทดสอบฟังก์ชัน -----------------------
if __name__ == "__main__":
    # ดึงค่าคอนฟิกทั้งหมด
    #get_config()

    # ดึงค่าคอนฟิกเฉพาะ interface
    #filter_config('<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"><interface/></native>')


    R5_config = """
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>R5</hostname>
                <ip>
                    <dhcp>
                        <excluded-address xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                            <low-high-address-list>
                                <low-address>192.168.5.1</low-address>
                                <high-address>192.168.5.10</high-address>
                            </low-high-address-list>
                        </excluded-address>
                        <pool xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp">
                            <id>1</id>
                            <default-router>
                                <default-router-list>192.168.5.1</default-router-list>
                            </default-router>
                            <network>
                                <primary-network>
                                <number>192.168.5.1</number>
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
                        <name>0/0/0.50</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>50</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.50.2</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.60</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>60</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.60.2</address>
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
                            <address>192.168.70.2</address>
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
                            <address>192.168.80.2</address>
                            <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                        </ip>
                    </GigabitEthernet>
                    <GigabitEthernet>
                        <name>0/0/0.500</name>
                        <encapsulation>
                        <dot1Q>
                            <vlan-id>500</vlan-id>
                        </dot1Q>
                        </encapsulation>
                        <ip>
                        <address>
                            <primary>
                            <address>192.168.5.1</address>
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
                            <address>5.5.5.5</address>
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
                            <ip>5.5.5.5</ip>
                            <wildcard>0.0.0.0</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.50.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.60.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.70.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.80.0</ip>
                            <wildcard>0.0.0.255</wildcard>
                            <area>0</area>
                        </network>
                        <network>
                            <ip>192.168.5.0</ip>
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

    edit_config(R5_config)
    
    # ลบค่าคอนฟิก startup (ใช้เมื่ออุปกรณ์รองรับ)
    #delete_config(target="startup")
