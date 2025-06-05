# Client Details
hostname = "100.126.255.140"
username = "flinksupport"
password = "f@linksupport#"
import telnetlib
import time
import re

def TelnetSession(host,username,password):
    """Telnet into the OLT and execute basic commands, extracting MAC addresses."""
    try:
        tn = telnetlib.Telnet(host)

        # Read and provide Username
        tn.read_until(b"Username: ")
        tn.write(username.encode("ascii") + b"\n")

        # Read and provide Password
        tn.read_until(b"Password: ")
        tn.write(password.encode("ascii") + b"\n")
        output = tn.read_until(b">", timeout=5).decode("ascii")
        if "Authentication failed!" in output:
            print("Authentication failed!")
            exit(0)
        # Wait for prompt
        time.sleep(1)
        tn.read_until(b">", timeout=5).decode("ascii")
        # Enter enable mode
        tn.write(b"enable\n")
        tn.write(b"\n")
        tn.read_until(b"#", timeout=5)

        # Enter config mode
        tn.write(b"config\n")
        tn.read_until(b"_config#", timeout=5)
        return tn

    except Exception as e:
        print(f"Error during Telnet session: {e}")

def extractEPONPorts(tn):
    tn.write(b"show interface brief\n")
    tn.write(b"q\n")
    output = tn.read_until(b">>", timeout=5).decode('ascii')
    output = output.splitlines()
    epon_interfaces = []
    for line in output:
        match = re.match(r'^(epon0/\d+)\s', line)
        if match:
            epon_interfaces.append(match.group(1))
    return epon_interfaces

def clearMAC(tn,interface):
    cmd = "show epon inactive-onu interface " + interface + "\n"
    print("-" * 50)
    print("Unbinding the macs from interface: ", interface)
    print("-" * 50)
    tn.write(cmd.encode("ascii"))
    tn.write(b"\n")
    output = tn.read_until(b">>", timeout=5).decode('ascii')
    # Regex to find MAC addresses in xxxx.xxxx.xxxx format
    mac_pattern = r'\b[\da-fA-F]{4}\.[\da-fA-F]{4}\.[\da-fA-F]{4}\b'
    mac_addresses = re.findall(mac_pattern, output)
    interfaceCMD = "interface " + interface +"\n"
    tn.write(interfaceCMD.encode("ascii"))
    for mac_address in mac_addresses:
        unbindCMD = "no epon bind-onu mac " + mac_address + "\n"
        tn.write(unbindCMD.encode("ascii"))
        output = tn.read_until(b">>", timeout=5).decode('ascii')
        if output:
            print("Removed: ", mac_address)
    # print(mac_addresses)
    # time.sleep(4)

if __name__ == "__main__":
    tn = TelnetSession(hostname,username,password)
    epon_interfaces = extractEPONPorts(tn)
    for interface in epon_interfaces:
        clearMAC(tn,interface)