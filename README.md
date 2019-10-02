# SNAP
A Simple Network Automation Program to load a Cisco router from nothing to something somewhat quickly.
![SNAP](https://github.com/JTHern/SNAP---Dist/blob/master/images/Snap1.PNG)

# How does it work:
Open SNAP.

# Router Info:
Select your method for connection.
(Console)(Telnet)(SSH)
Enter the username (usernames will not be saved)
enter the password (password will not be saved)
Then select the COM port (if using Console) or IP if using telnet or ssh.

Click Verify.

This will then use the credentials on the device.
It will automatically make sure the Cisco Router is above IOS 15.4 (this was for my use but it wont affect anything.)

# Load Page:

* Make sure the config does not have conf t, enable, building.., or end in it.

Click open to select the config you want to load. Then Click Load, watch as the config loads line by line.

Or pull the current config on the device. (This will automatically save the config in the same directory as SNAP)

If you want to completely erase the Cisco Router there is also a Zeroize feature. (This was useful for me because reasons.)

# Troubleshoot

ping [Enter the ip into the empty field] - Pings from the Cisco Router, not your machine.  
Traceroute [Enter the ip into the empty field] - Traceroutes from the Cisco router, not your machine.

Routes - prints the output of [show ip route] to the Snap Screen.
Interaces - prints the output of [show ip interface brief] to the Snap Screen.
DMPVN - prints the output of [show crypto ikev2 sa] to the Snap Screen.
OSPF - prints the output of [show ip ospf neigh] to the Snap Screen.
EIGRP - prints the output of [show ip eigrp neigh] to the Snap Screen.

# About

Dependencies:
Netmiko (and all of its dependencies), PyQT5.
