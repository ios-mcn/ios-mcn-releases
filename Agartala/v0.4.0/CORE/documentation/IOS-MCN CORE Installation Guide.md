# IOS MCN v0.4.0 Agartala Release: CORE Installation Guide

# Introduction

The core software for the India Open Source for Mobile Communication Network (IOS-MCN) is based on open-source SD-Core. In this document, includes the installation and configurations for making the platform up and running for the integration with RAN and UPF. This includes emulated RAN test with built in tool.

# Purpose and Audience

This document is for installing and configuring the IOS-MCN core software on the server. It can be connected to RAN, attach UEs and integrate with UPF.

# Installation methods

The installation can be proceeded with this documentation and the core can get from IOS-MCN git repository. The details of each step are given on next section.

# Installation

## Hardware Requirements

The IOSMCN-Core installation requires the following prerequisites

- 8 Cores

- 16 GB RAM

- 40 GB Disk Storage

## Software Prerequisites

- Ubuntu Server 22.04 LTS Operating system

- Git

- Curl

- Make

- Net tools

- Netplan

- Ansible

- Python3

- Docker.io

- openssh-server

- Ethtool

## Prerequisite Installation

Login to the Ubuntu Server 22.04.5 LTS and take a terminal. The internet access is required for the machine.

Update the repository by the command

```
sudo apt update
```

After the successful completion of repository update start installing the required tools.

```
sudo apt install git curl make net-tools pipx python3-venv docker.io

pipx install --include-deps ansible

pipx ensurepath

sudo apt install sshpass netplan.io iptables openssh-server ethtool
```

## Prerequisite Environment

### Firewall status

Verify the firewall is inactive on the system using the command

```
sudo ufw status
```

If the firewall is active, disable the firewall using the command

```
sudo ufw disable
```

### Networkd status

Verify the _systemd-networkd_ status for the network configuration using the command

```
systemctl status systemd-networkd.service
```

### Disable Generic receive offload (GRO)

Find the interface from the _ifconfig_ command and input the interface name to the following command

```
sudo ethtool -K \<core-interface\> gro off
```
### Set Static IP using Netplan

Verify that the Netplan configuration file includes the correct IP address, gateway, and DNS server settings.

Common Netplan config file paths:

- /etc/netplan/50-cloud-init.yaml
- /etc/netplan/01-netcfg.yaml
- /etc/netplan/00-installer-config.yaml

```
nano /etc/netplan/00-installer-config.yaml
```

eg.,

![Netplan configuration](./images/install/fig7-netplan-image.png)

where,

- Replace _ens3_ with the system's network interface.
- Under the interface section, set the addresses field to the system's IP address.
- Specify the DNS IP under nameservers.addresses.
- If no DNS is configured on the network, use 8.8.8.8 as the DNS IP.

If any change on the configuration, execute the command:

```
sudo netplan apply
```

## Installation of IOS-MCN Core

### Download core image

Download file [iosmcn.agartala.v0.4.0.core.images.tar.xz](../release-images/iosmcn.agartala.v0.4.0.core.images.tar.xz) to the directory.

```
wget https://github.com/ios-mcn/ios-mcn-releases/raw/main/Agartala/v0.4.0/CORE/release-images/iosmcn.agartala.v0.4.0.core.images.tar.xz
tar -xvJf iosmcn.agartala.v0.4.0.core.images.tar.xz
cd iosmcn.agartala.v0.4.0.core.images/IOSMCN-CoreDpm
```

This brings up a Kubernetes cluster, deploy a 5G version of IOSMCN-Core on that cluster, and then connect that IOSMCN-Core to either an emulated 5G RAN or physical RAN.
### ios-mcn-core single slice deployment
### Target Parameter Settings
```cd iosmcn.agartala.v0.4.0.core.images/IOSMCN-CoreDpm```
#### Update Configuration Files

##### Update the hosts.ini

Set the node IP to the core machine IP, and update the username and password based on your system

![alt text](images/install/image-3.png)

#### Update main.yml in vars

- Configure data_iface and values_file

Set data_iface appropriately.

> For multiple-dnn-ims support, use values_file as deps/5gc/roles/core/templates/iosmcn-5g-multiple-dnn-ims-values.yaml

![alt text](images/install/image-4.png)

- Set Helm Chart as Local

Use the cloned ios-mcn-core-helm-chart directory as the local chart

![alt text](images/install/helm-chart-path.png)

- Update AMF IP
  Ensure the AMF IP is correctly updated. (AMF IP is core machine IP)

![alt text](images/install/image-6.png)

#### Update iosmcn-5g-multiple-dnn-ims-values.yml in deps/5gc/roles/core/templates

- Modify Subscriber Details
  Add/update subscriber information as needed

![alt text](images/install/image-7.png)

- Configure Device Group and DNS

Ensure device group and DNS settings are correct. Update DNN and QCI based on the requirement.


![alt text](images/install/devgroup-msisdn.png)

![alt text](images/install/qos.png)

- Update Network Slice MCC and MNC

Set the appropriate sst, sd, MCC and MNC

![alt text](images/install/image-10.png)

### Install Kubernetes

Start installation with the command

```
cd iosmcn.agartala.v0.4.0.core.images/IOSMCN-CoreDpm
make iosmcn-k8s-install
```

Verify the installation status by the command

```
kubectl get pods --all-namespaces
```

The successful output looks like

![Output of Kubernetes installation](./images/install/fig2-output-kubernetes.png)

Figure 2: Output of Kubernetes installation

### Install IOSMCN-Core

Initiate the installation by the command

```
make iosmcn-5gc-install
```

The successful outcome shall be verified using the following command

```
kubectl get pods -n iosmcn
```

![](./images/install/fig6-install-sd-core.png)

_Figure 3: Success state of IOSMCN-Core installation_

### ios-mcn-core multiple slice deployment
### Target Parameter Settings
```cd iosmcn.agartala.v0.4.0.core.images/IOSMCN-CoreDpm```
#### Update Configuration Files

##### Update the hosts.ini

Set the node IP to the core machine IP, and update the username and password based on your system

![alt text](images/install/image-3.png)

#### Update main.yml in vars
Replace the existing vars/main.yml file with the updated vars/main-upf.yml file to enable multiple UPF configurations.

```cp vars/main-upf.yml vars/main.yml```

Update data_iface and chart_ref based on your iosmcn-core-helm-chart path.
- Set data_iface appropriately.
- Set Helm Chart as Local

Use the cloned ios-mcn-core-helm-chart directory as the local chart

![alt text](images/install/helm-chart-path.png)
![alt text](images/install/helm-chart-path-2.png)

- Update AMF IP
  Ensure the AMF IP is correctly updated. (AMF IP is core machine IP)

![alt text](images/install/image-6.png)

#### Update iosmcn-multiple-slice.yaml in deps/5gc/roles/core/templates

- Modify Subscriber Details
  Add/update subscriber information as needed

![alt text](images/install/subscribers.png)

- Configure Device Group and DNS

Create Device groups for each slices. Ensure DNS settings are correct. Update DNN and QCI based on the requirement.


![alt text](images/install/devgroup1.png)

![alt text](images/install/devgrp1-qci.png)

![alt text](images/install/devgrp2.png)

![alt text](images/install/devgrp2-qci.png)


- Configure Network multiple network slice 

Update the required sst and sd values, plmn and configure the device group name according to the UE’s slice requirement.

![alt text](images/install/networkslice-1.png)

![alt text](images/install/networkslice-2.png)

### Install Kubernetes

Start installation with the command

```
cd iosmcn.agartala.v0.4.0.core.images/IOSMCN-CoreDpm
make iosmcn-k8s-install
```

Verify the installation status by the command

```
kubectl get pods --all-namespaces
```

The successful output looks like

![Output of Kubernetes installation](./images/install/fig2-output-kubernetes.png)

Figure 2: Output of Kubernetes installation

### Install IOSMCN-Core

Initiate the installation by the command

```
make iosmcn-5gc-install
```

The successful outcome shall be verified using the following command

```
kubectl get pods -n iosmcn
```

![](./images/install/fig6-install-sd-core.png)

_Figure 3: Success state of IOSMCN-Core installation_

### Install IOSMCN-UPF 

Initiate the installation by the command

```
make 5gc-upf-install
```

The successful outcome shall be verified using the following command

```
kubectl get pods -A
```
![](./images/install/pod-status-multiple-upf.png)

## Add Route in gNB

In core machine, run following command to get the AMF service IP:

```
kubectl get svc -n iosmcn
```

![](./images/install/fig17.png)

Add route in gNB machine to AMF service IP:

```
sudo ip route add \<amf-service-ip\> via <core_ip>
```

Add route in gNB machine to UPF:

```
sudo ip route add 192.168.252.0/24 via <core_ip>
```

## Add Route in IMS Server if you are using IMS

In core machine, run following command to get the NFs service IP:

```
kubectl get svc -n iosmcn
```

![](./images/install/NFs-svc.png)

Add route in IMS server machine to NFs service IP:

```
sudo ip route add 10.43.0.0/16 via <core_ip>
```

Add route in gNB machine to UPF:

```
sudo ip route add 172.252.0.0/16 via <core_ip>
```

## Verify Network

### Check core and access are properly configured outside the container

There are two bridges that connect the physical interface with the UPF container. The access bridge connects the UPF downstream to the RAN (this corresponds to 3GPP’s N3 interface) and is assigned IP subnet 192.168.252.0/24 . The core bridge connects the UPF upstream to the Internet (this corresponds to 3GPP’s N6 interface) and is assigned IP subnet 192.168.250.0/24 .

![](./images/install/fig8-verify-network.png)

The above output from ip shows the two interfaces visible to the server, but running outside the container.

### Check core and access are properly configured inside the container

kubectl can be used to see what’s running inside the UPF, where bessd is the name of the container image that implements the UPF, and access and core are the last two interfaces shown below:

```
kubectl -n iosmcn exec -ti upf-0 bessd -- ip addr
```

![](./images/install/fig9.png)

When packets flowing upstream from the gNB arrive on the server’s physical interface, they need to be forwarded over the access interface. This is done by having the following kernel route installed, which should be the case if your ios-mcn-core installation was successful.

```
route -n | grep "Iface\|access"
```

![](./images/install/fig10.png)

Within the UPF, the correct behavior is to forward packets between the access and core

interfaces. Upstream packets arriving on the access interface have their GTP headers

removed and the raw IP packets are forwarded to the core interface. The routes inside the UPF’s bessd container will look something like this:

```
kubectl -n iosmcn exec -ti upf-0 bessd -- ip route
```

![](./images/install/fig11.png)

```
route -n | grep "Iface\|core"
```

![](./images/install/fig12.png)

The first rule above matches packets to the UEs on the 172.250.0.0/16 subnet. The next hop for these packets is the core IP address inside the UPF. The second rule says that next hop address is reachable on the core interface outside the UPF. As a result, the downstream packets arrive in the UPF where they are GTP-encapsulated with the IP address of the gNB.

Note that if you are not finding access and core interfaces outside the UPF, the following commands can be used to create these two interfaces manually (again using our running example for the physical ethernet interface):

```
ip link add core link ens3 type macvlan mode bridge 192.168.250.3

ip link add access link ens3 type macvlan mode bridge 192.168.252.3
```

Note that if you are find access and core interfaces outside the UPF, but route not generated the following commands can be used to create these two routes manually (again using our running example for the physical ethernet interface):

```
sudo ip route add 192.168.252.0/24 dev access

sudo ip route add 192.168.250.0/24 dev core
```

### Packet Traces

Packet traces are the best way to diagnose your deployment, and the most helpful traces you can capture are shown in the following commands. You can run these on the core server, where we use our example ens3 interface for illustrative purposes:

```
sudo tcpdump -i any sctp -w sctp-test.pcap

sudo tcpdump -i ens3 port 2152 -w gtp-outside.pcap

sudo tcpdump -i access port 2152 -w gtp-inside.pcap

sudo tcpdump -i core net 172.250.0.0/16 -w n6-inside.pcap

sudo tcpdump -i ens3 net 172.250.0.0/16 -w n6-outside.pcap
```

If the gtp-outside.pcap has packets and the gtp-inside.pcap is empty (no packets captured), you may run the following commands to make sure packets are forwarded from the ens3 interface to the access interface and vice versa:

```
sudo iptables -A FORWARD -i ens3 -o access -j ACCEPT

sudo iptables -A FORWARD -i access -o ens3 -j ACCEPT
```

## Routing Configuration inside UPF pod

### Enter the UPF Pod

To enter the UPF pod, execute the following commands:

```
kubectl exec -it upf-0 -n iosmcn -- /bin/bash
```

Once inside the pod, verify the network interfaces:

```
ip addr
```

Ensure the following four interfaces are created: lo, eth0, access, and core.

![](./images/install/fig13.png)

#### Verify Routing Table

Check the routing table to ensure it matches the expected configuration

```
ip r
```

![](./images/install/fig14.png)

#### Ping test

![](./images/install/fig15.png)

#### Check and Update ARP Entries

![](./images/install/fig16.png)

Ensure that the ARP entries for access and core interfaces have the correct MAC addresses. If the MAC addresses do not match, update them as follows:

```
sudo arp -s 192.168.252.3 \<mac-address-access\>

sudo arp -s 192.168.250.3 \<mac-address-core\>
```

Replace \<mac-address-access\> and \<mac-address-core\> with the actual MAC addresses of the access and core interfaces respectively [Inside UPF-POD].

## Related Artifacts & links

| **Document Name**     | **Purpose**                           | **Link**                                   |
| --------------------- | ------------------------------------- | ------------------------------------------ |
| Developer Guide       | Guide for IOSMCN-Core developers      | [Click Here](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.4.0/CORE/documentation/IOS-MCN%20CORE%20Developer%20Guide.md)       |
| User Guide            | Quick user guide                      | [Click Here](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.4.0/CORE/documentation/IOS-MCN%20CORE%20User%20Guide.md)            |
| API Guide             | API guide                             | [Click here](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.4.0/CORE/documentation/IOS-MCN%20CORE%20API%20Guide.md)             |
| Troubleshooting Guide | Troubleshooting guide for IOSMCN-Core | [Click here](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.4.0/CORE/documentation/IOS-MCN%20CORE%20Troubleshooting%20Guide.md) |
| Installation Guide    | Installation of IOSMCN-Core           | [Click here](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.4.0/CORE/documentation/IOS-MCN%20CORE%20Installation%20Guide.md)    |