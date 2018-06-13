# Ryu Monitor
SDN controller for monitoring load on OpenVSwitch. Python scripts for a Ryu controller running on controller node in a cloud 
infrastructure.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites

Make sure you have pip installed on the controller node:

```
sudo apt-get install python-pip
```

### Installing

On the controller node install Ryu components, pip command is the easiest option:

```
pip install ryu
```
To run a program in a OpenStack environemnt use the following command:

```
ryu-manager --ofp-tcp-listen-port 5555 --verbose ryu.app.simple_monitor_13
```
In this case you are running a sample implementation of Traffic Monitor.
It is important to specify a new port to listen, instead of the default 6633, in a OpenStack enviroment, due to other processes
listening on the default one.

### Deployment

The program is based on external libraries, if not present please install them via pip:
```
sudo pip install --upgrade cython
sudo pip install numexpr
sudo pip install arch
sudo pip install pyramid
sudo pip install pyramid-arima
```
Now you are able to run the controller:
```
ryu-manager --ofp-tcp-listen-port 5555 --verbose ryuMonitor/monitor_tuple.py
```

### Helpful commands

Run these commands on the compute nodes.

```
#show ovs current config summary
sudo ovs-vsctl show

#set the new controller for **br-flat-lan-1** bridge
sudo ovs-vsctl set-controller br-flat-lan-1 tcp:<Controller_IP>:5555

#view forwarding table (mac address table)
sudo ovs-appctl fdb/show

#see mapping of OpenFlow ports to system ports
sudo ovs-ofctl show mybridge

#see flow entries (OpenFlow) on mybridge
sudo ovs-ofctl dump-flows mybridge

#see records in ovsdb-server tables
sudo ovs-vsctl list Bridge
sudo ovs-vsctl list Port
sudo ovs-vsctl list Interface
```
The commands assume tou have already set *ctl* as the IP of the Controller node, while *br-flat-lan-1* is the OVS bridge name.
