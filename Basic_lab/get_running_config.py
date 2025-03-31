from ncclient import manager
from xml.dom.minidom import parseString

host='192.168.100.1'
user='admin'
password='cisco'

def get_config():
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        running_config = m.get_config(source='running').data_xml
        pretty_config = parseString(running_config).toprettyxml(indent="  ")
        print("Retrieved Configuration (Formatted):")

        with open("Lab3-running_config.txt", "w", encoding="utf-8") as file:
            file.write(pretty_config)

if __name__ == "__main__":
    get_config()
    
    