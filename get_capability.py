from ncclient import manager
from xml.dom.minidom import parseString

host='192.168.20.3'
user='admin'
password='cisco'

def get_capability():
    with manager.connect(host=host, port=830, username=user, password= password, hostkey_verify=False) as m:
        device_capability = m.server_capabilities
        formatted_capabilities = "Supported NETCONF Capabilities:\n\n"
        formatted_capabilities += "\n".join(
            [f"- {cap}" for cap in device_capability]
        )

        # Save to a .txt file
        with open("device_capabilities.txt", "w", encoding="utf-8") as file:
            file.write(formatted_capabilities)

        print("Capabilities saved to device_capabilities.txt")
    
if __name__ == "__main__":
    get_capability()