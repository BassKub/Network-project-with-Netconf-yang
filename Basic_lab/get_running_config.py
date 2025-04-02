#ncclient เป็นไลบรารี Python ที่ใช้สำหรับติดต่อกับอุปกรณ์เครือข่ายผ่าน
#manager เป็นโมดูลหลักของ ncclient ที่ใช้สำหรับเปิดการเชื่อมต่อกับอุปกรณ์และจัดการค่าคอนฟิก
from ncclient import manager

#นำเข้าไลบรารีสำหรับการจัดการ XML
from xml.dom.minidom import parseString

#กำหนดตัวแปรที่ใช้ในการเชื่อมต่ออุปกรณ์
host='192.168.100.1'
user='admin'
password='cisco'

#ฟังก์ชันสำหรับดึงการกำหนดค่าจากอุปกรณ์
def get_config():
    #เชื่อมต่อกับอุปกรณ์และดึงการกำหนดค่าจากนั้นบันทึกการกำหนดค่าในรูปแบบที่อ่านง่าย
    #port 830 เป็นพอร์ตที่ใช้สำหรับการเชื่อมต่อ NETCONF
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:

        #ดึงการกำหนดค่าจากอุปกรณ์โดยเป้าหมายเป็น running config
        running_config = m.get_config(source='running').data_xml

        #ใช้ xml.dom.minidom เพื่อทำให้การกำหนดค่าที่ดึงมาอ่านง่ายขึ้น
        pretty_config = parseString(running_config).toprettyxml(indent="  ")
        print("Retrieved Configuration (Formatted):")

        #บันทึกการกำหนดค่าที่อ่านง่ายลงในไฟล์ Lab3-config.txt
        with open("Lab3-running_config.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

if __name__ == "__main__":
    #เรียกใช้ฟังก์ชัน get_config เพื่อดึงการกำหนดค่าจากอุปกรณ์
    get_config()
    
    