#ncclient เป็นไลบรารี Python ที่ใช้สำหรับติดต่อกับอุปกรณ์เครือข่ายผ่าน
#manager เป็นโมดูลหลักของ ncclient ที่ใช้สำหรับเปิดการเชื่อมต่อกับอุปกรณ์และจัดการค่าคอนฟิก
from ncclient import manager 

#นำเข้าไลบรารีสำหรับการจัดการ XML
import xml.dom.minidom

#กำหนดตัวแปรที่ใช้ในการเชื่อมต่ออุปกรณ์
host='192.168.100.1'
user='admin'
password='cisco'

#ฟังก์ชันสำหรับแก้ไขการกำหนดค่า
def edit_config(nc):
    #เชื่อมต่อกับอุปกรณ์และแก้ไขการกำหนดค่าตามที่ระบุใน xml
    #port 830 เป็นพอร์ตที่ใช้สำหรับการเชื่อมต่อ NETCONF
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:

        #แก้ไขการกำหนดค่าที่อุปกรณ์โดยเป้าหมายเป็น running config
        m.edit_config(target="running", config=nc)

    print("Configuration Updated")

#ฟังก์ชันสำหรับดึงการกำหนดค่าจากอุปกรณ์
def get_config():
    #เชื่อมต่อกับอุปกรณ์และดึงการกำหนดค่าจากนั้นบันทึกการกำหนดค่าในรูปแบบที่อ่านง่าย
    #port 830 เป็นพอร์ตที่ใช้สำหรับการเชื่อมต่อ NETCONF
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:

        #ดึงการกำหนดค่าจากอุปกรณ์โดยเป้าหมายเป็น running config
        config = m.get_config(source="running").data_xml

        #ใช้ xml.dom.minidom เพื่อทำให้การกำหนดค่าที่ดึงมาอ่านง่ายขึ้น
        pretty_config = xml.dom.minidom.parseString(config).toprettyxml(indent="  ")

        #บันทึกการกำหนดค่าที่อ่านง่ายลงในไฟล์ Lab3-config.txt
        with open("Lab3-config.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

        print("Config Saved")

if __name__ == "__main__":
    #กำหนดค่าการกำหนดค่าอินเตอร์เฟซในรูปแบบ XML
    hostname_config = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>Test1234</hostname>
        </native>
    </config>
    """

    edit_config(hostname_config)
    
    get_config()