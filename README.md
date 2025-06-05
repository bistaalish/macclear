# Telnet OLT MAC Address Unbinder

A Python script to automate Telnet access to an Optical Line Terminal (OLT), extract EPON interface ports, and unbind inactive ONU MAC addresses.

## 📋 Features

- Telnet connection to OLT devices
- Extraction of `epon` interface ports
- Identification and unbinding of inactive ONU MAC addresses
- Regex-based MAC address parsing (xxxx.xxxx.xxxx format)
- Basic logging to console for removed MACs

## ⚙️ Requirements

- Python 3.12
- Telnet access enabled on the OLT
- Telnetlib (standard Python library)
- Valid login credentials

## 🛠️ Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/olt-mac-unbinder.git
cd olt-mac-unbinder
```

2. Modify the client details:

Open the script and set your OLT connection parameters at the top of the file:

```bash
hostname = "YOUR_OLT_IP"
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
```

3. Run the script:

```bash
python3 epon.py
```

## Output
```markdown
--------------------------------------------------
Unbinding the macs from interface:  epon0/1
--------------------------------------------------
Removed:  aaaa.bbbb.cccc
Removed:  dddd.eeee.ffff
```
