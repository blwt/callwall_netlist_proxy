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
