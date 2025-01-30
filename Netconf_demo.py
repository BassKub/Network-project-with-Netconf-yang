from ncclient import manager
from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import AuthenticationError, SSHError
from paramiko.ssh_exception import AuthenticationException, SSHException
from xml.dom.minidom import parseString



# Device connection details
DEVICE = {
    "host": "192.168.20.3",
    "port": 830,
    "username": "admin",
    "password": "cisco",
    "hostkey_verify": False
}

def get_capabilities():
    """
    Retrieve and save the NETCONF capabilities of the device in a formatted .txt file.
    """
    try:
        with manager.connect(**DEVICE) as MNG:
            capabilities = MNG.server_capabilities

            # Format the capabilities for a readable file output
            formatted_capabilities = "Supported NETCONF Capabilities:\n\n"
            formatted_capabilities += "\n".join(
                [f"- {cap}" for cap in capabilities]
            )

            # Save to a .txt file
            with open("device_capabilities.txt", "w", encoding="utf-8") as file:
                file.write(formatted_capabilities)

            print("Capabilities saved to device_capabilities.txt")

    except (AuthenticationError, SSHError) as e:
        print(f"Connection error: {e}")
    except RPCError as e:
        print(f"RPC error: {e}")

def get_filtered_config():
    """
    Retrieve specific configuration using a YANG model-based filter and display it in a pretty format.
    """
    filter_xml = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface/>
            </interfaces>
        </filter>
    """
    try:
        with manager.connect(**DEVICE) as MNG:
            # Send the filtered request to retrieve interfaces
            response = MNG.get_config(source="running", filter=filter_xml).data_xml

            # Format the response XML to make it more readable
            pretty_response = parseString(response).toprettyxml(indent="  ")

            # Print the pretty response
            print("Filtered Configuration (Interfaces):")
            print(pretty_response)
    except (AuthenticationError, SSHError) as e:
        print(f"Connection error: {e}")
    except RPCError as e:
        print(f"RPC error: {e}")


def get_running_config():
    """
    Retrieve and save the running configuration from the device, formatted for readability.
    """
    try:
        with manager.connect(**DEVICE) as MNG:
            # Get the full running configuration
            config = MNG.get_config(source='running').data_xml
            
            # Format the XML for better readability
            pretty_config = parseString(config).toprettyxml(indent="  ")

            print("Retrieved Configuration (Formatted):")
            print(pretty_config)

            # Save the formatted configuration to a .txt file
            with open("running_config.txt", "w", encoding="utf-8") as file:
                file.write(pretty_config)

            print("Formatted configuration saved to running_config.txt")
    except (AuthenticationError, SSHError) as e:
        print(f"Connection error: {e}")
    except RPCError as e:
        print(f"RPC error: {e}")

def edit_config(config_data):
    """
    Apply configuration changes to the device and commit to save.
    """
    try:
        with manager.connect(**DEVICE, timeout=60) as MNG:
            # Attempt to lock the configuration
            MNG.lock(target='running')
            print("Configuration locked successfully.")
            
            # Apply the configuration changes
            response = MNG.edit_config(config_data, target='running')
            print("Edit Config Response:", response)
            
            # Commit the changes to ensure they are saved
            commit_response = MNG.commit()
            print("Commit Response:", commit_response)
            
            # Unlock the configuration after changes
            MNG.unlock(target='running')
            print("Configuration unlocked successfully.")
    except (AuthenticationError, SSHError) as e:
        print(f"Connection error: {e}")
    except (AuthenticationException, SSHException) as e:
        print(f"SSH Authentication error: {e}")
    except RPCError as e:
        print(f"RPC error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Modify the configuration to change the hostname
    new_config = f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>NewR1</hostname>
        </native>
    </config>
    """

    # Retrieve the current running configuration
    #get_running_config()

    # Retrieve the device's capabilities
    get_capabilities()

    # Retrieve specific configuration (hostname)
    #get_filtered_config()

    # Apply new configuration (change hostname) and commit changes
    #edit_config(new_config)
