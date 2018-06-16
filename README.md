# callwall_netlist_proxy

CallWall is a phone blocker program by NullRiver for the Mac.
One feature of CallWall is to enable the use of a netlist, http://www.whocalled.net, for its information.

This python 2.5.1 program is a HTTP Web Proxy which redirects the netlist URL to an alternate source.

To enable:
1) On the Mac, go to System Preferences/Network
2) Select your network adapter (i.e. Ethernet, Wifi) and click "Advanced..."
3) Click "Proxies"
4) Select and check "Web Proxy (HTTP)"
5) In the "Web Proxy Server", specify "localhost:8080"
6) Select "OK"

In a terminal window run...
     python callwall_proxy.py

# DISCLAIMER

Please note: all tools/scripts in this repo are released for use "AS IS" without any warranties of any kind.

Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.

You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.

