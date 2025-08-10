# **IOS MCN v0.2.0 Agartala Release  -  Integration Guide** 

##INTRODUCTION
---

This document provides a comprehensive guide for integrating both the hardware and software components required to deploy and operate the IOS MCN v0.2.0 Agartala Release. It outlines the step-by-step process to set up and bring up a functional 5G private network.

##PURPOSE AND AUDIENCE
---


The purpose of this document is to provide a clear, structured, and step-by-step approach to integrate the IOS MCN v0.2.0 Agartala Release for a 5G private network setup. It aims to ensure that all configurations, connections, and dependencies are handled correctly for a successful deployment. This document may serve as a reference during testing, troubleshooting, and validation phases of the network rollout.

This document is intended for technical professionals involved in the deployment of 5G private networks using IOS MCN v0.2.0, including system integrators, field engineers, network engineers, validation teams, R&D, and support staff. It assumes a working knowledge of 5G architecture, Linux systems, networking, and the IOS MCN platform, and serves as a practical guide for seamless integration, setup, and troubleshooting.


##INTEGRATION OF RAN UE WITH RU AND CORE
---

#PREREQUISITES :
--

- **HARDWARE**

  - Ensure correct hardware setup and Bios configurations. For reference refer to chapter 3,4 of the RAN Installation Guide.                                            

- **SOFTWARE**

  - Ensure all the necessary software are installed. Refer to chapter 5 of the RAN Installation Guide.



**3.1 Integrating with the LPRU**
---

*LPRU Configuration:*

 Before configuring the LPRU we need to run the following commands to make our system (gNB) ready on a configuration level and to synchronize the clocks with respect to the Grandmaster switch which provides GPS signals.

 **The commands and their description in detail is noted down below:**

**1.  Run:**
   
   ```
   sudo ./test.sh
```

This script test.sh configures the 5G gNB system
to work with the LPRU by disabling NTP, setting high MTU and buffer
values, enabling CPU performance mode, and setting up static routes to
IOSMCN-CORE. It also applies essential kernel parameters like BBR and
forwarding. The script ensures synchronization with the Grandmaster
clock and prepares the system for real-time 5G processing. Unsafe
noiommu mode is enabled to support VFIO-based device access.

**2.  Run:**
 ```
 sudo./vf.sh
```
 This script prepares the enp2s0f1 NIC for DPDK-based high-speed data
 plane communication by configuring advanced features such as MTU,
 SR-IOV, VLAN tagging, spoof check disablement, and MAC assignment.

   It enables 2 Virtual Functions (VFs), configures their VLANs and
    trusted modes, and then binds them to vfio-pci drivers using
    dpdk-devbind.py to offload traffic to user space with near real-time
    performance. These settings are crucial for gNB--LPRU data paths,
    especially when handling massive traffic in 5G.



**Then, check whether the function has been created.**

**Run command in terminal:**
```
 ip link show
 ```


  **3. Run:**
``` 
   sudo ./slave-enp2s0fo.sh
```
 This command runs ptp4l to make the gNB a PTP slave to the Fibrolan Grandmaster using the *G.8275.1* telecom profile, which provides accurate phase and frequency synchronization. It binds the PTP process to CPU core 2 for better real-time performance and uses the network interface enp2s0f0 for PTP packets. This synchronization is essential for TDD-based 5G systems to ensure time alignment across gNB and LPRU.


 **4. Run:**
   
```
sudo ./master-enp2s0f1.sh
```
 This command runs ptp4l to make the gNB act as a PTP master for the
 VVDN LPRU using the G.8275.1 clock profile. It uses interface enp2s0f1
 and pins the process to core 2 for better timing precision. This
 ensures accurate time distribution from the gNB to the LPRU, enabling
 proper synchronization for 5G operations.


**5.  Run :** 

```
sudo ./phc2sys-master.sh
```
 This command runs **phc2sys** to synchronize the gNB's system clock
 with the hardware clock of interface enp2s0f1, using the G.8275.1
 profile. It ensures tight timing accuracy when the gNB is acting as a
 PTP master. The process is pinned to core 2 for consistent execution
 and uses fine-grained sync parameters to maintain real-time clock
 precision.




**To access this LPRU (LOW POWER RADIO UNIT),**
  
*We need to ssh into the machine with the below provided details:*


-   *Username*   - **root**

-   *IP Address* - **192.168.4.50**

-   *Password*   - **vvdn**



**Logging into the terminal of the LPRU:**

Once you are logged in, Follow the below provided steps to sync up the LPRU, this includes the synchronization of radio unit, the compression setting , RF antenna configuration, channel parameters and other things.

**1. To track synchronization progress in real-time by filtering sync-related log entries until the system achieves synchronization. Run command:**

 
```
tail -f/var/logs/synctiming2.log| grep sync
```
**We will wait until the Radio unit synchronizes.**

- This command continuously monitors (tail -f) the **synctiming2.log**
file and filters out lines that contain the word sync. You're
essentially waiting and watching until a synchronization message
appears in the log.

- You can also physically check the bottom most LED on the LPRU.

- It blinks red when the RU is not synchronized, and turns green when
 it is synchronized


 **2. To parse and load the e_2x2.xml configuration file for applying
    system or test setup parameters.Run command:**

  ```
  xml_parser e_2x2.xml
  ```

- Depending on whether we are running SISO (1x1) or MIMO (2x2) and e/f
Fronthaul Interface

- For 1x1 use e_1x1.xml, for 2x2 use e_2x2.xml (both for phy-e/phy-f),

- This command runs an XML parser tool to read and process the e_2x2.xml configuration file, which likely contains parameters or settings (e.g., antenna config, MIMO setup) used in the 5G lab environment.

  
 **3. To write the value 1919 to memory address a0010024 for configuring a
 specific hardware register or system setting that helps in compressing the data (e.g., I/Q samples) transmitted between the DU (Distributed Unit) and the RU (Radio Unit) over fronthaul interfaces (typically using the eCPRI or ORAN protocols). Run command:**
```
  mw.l a0010024 1919
```
- This command writes the value 1919 to the memory address a0010024
using the mw.l (memory write long) command. It's typically used to
configure hardware registers, initialize components, or change
settings in embedded/5G systems.

 

  
**4. To edit the live running configuration in Sysrepo using the vi
    editor and To configure and activate transmit carrier parameters ---
    including center frequency, bandwidth, duplex scheme, and RF gain
    --- by editing the system configuration and setting the carrier
    status to ACTIVE, thereby completing the RU's channel setup for 5G
    NR transmission. Run command:**
```
sysrepocfg --edit=vi -d running
```

- Change 'INACTIVE' to 'ACTIVE' at two places and save the file.

- This command opens the running datastore of Sysrepo (a YANG-based
 configuration datastore) for editing using the vi editor. It's used
to view or modify the current live configuration of a network
component or service.


**Now, the RU configuration is done.**



 After completing these steps the user **start the nr-softmodem** binary by Running the below mentioned commands after the user have successfully configured the LPRU.
 
```
 cd ios-mcn-ran-uni-baremetal-v0.2.0.tar.gz
```
```
 sudo taskset -c 10 ./nr-softmodem -O ./<configuration file> --sa -reorder-thread-disable 1 --thread-pool 3,4,5,7
```

-   Check logs to validate that gNB is up and running , you can store logs and see them on the console by using the following command at end of the previos commandline
```
2>&1 | tee <name-of-the-test-case>.log
```
## **3.2 INTEGRATING SDR - USRP**

### PREREQUISITES

- Refer to chapter 3 of RAN-UNI developer guide to build and install the necessary packages to run the USRP.


- Note: The USRP Device must be connected to the build server on **USB port 3.0.**
  

 This section describes the procedure to execute the nr-soft modem
binary build for USRP b210 board. 



 **Package Information:**

- Download the tar file from the Official channel
> *https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.2.0/RAN/source-code/iosmcn.agartala.v0.2.0.ran.source.tar.gz*

 Copy the tar file to the target gNB machine (/home/user/) . Untar the
file using cmd.
```
 tar -xvzf ios-mcn-ran-uni-baremetal-v0.2.0.tar.gz
 cd ios-mcn-ran-uni-baremetal-v0.2.0
```

In case of USRP we don't need any fronthaul binary. We just need to
set the dynamic linking of the shared libraries as shared in the
package.

Set the shared library linking using utility patchelf. You can install this utility using cmd.
```
 sudo apt install patchelf
 sudo patchelf --set-rpath <complete path to package><artifact(nr-softmodem)>
```

**Environment Setup or general system initial commands**

**Run these commands from the home folder: cd ~  :**

```
 sudo timedatectl set-ntp false
 sudo cpupower idle-set -D 0
 sudo sysctl -w net.core.rmem_max=62500000
 sudo sysctl -w net.core.wmem_max=62500000
 sudo sysctl -w net.core.rmem_default=62500000
 sudo sysctl -w net.core.wmem_default=62500000
 sudo sysctl -w net.core.default_qdisc=fq
 sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
 sudo ip route add 192.168.x.0/24 via 192.168.x.56 ##(add route according to the core system installed )This is an sample command.
 sudo iptables -P FORWARD ACCEPT
 sudo sysctl net.ipv4.conf.all.forwarding=1
 sudo cpupower frequency-set -g performance -u 4.70GHz -d 4.70GHz
 sudo ethtool -G enp2s0f1 tx 4096 rx 4096
 sudo sh -c 'echo "1" > /sys/module/vfio/parameters/enable_unsafe_noiommu_mode'
```

After that start the nr-softmodem:
```
 cd ios-mcn-ran-uni-baremetal-v0.2.0
 sudo taskset -c 10 ./nr-softmodem -O ./<configuration file> --sa -E --usrp-tx-thread-config 1 --thread-pool 3,4,5
```


## **3.3 Integrating with the core**
Open SD-core in new terminal:

We will access the SD-core server machine via **SSH** and view the
status of **the 5G core elements/nodes** that are present on the Kubernetes cluster
```
ssh administrator@192.168.x.41   #Enter Password
```

**Command: to watch pods status is mentioned below**
```
watch -n 1 kubectl get pods -A
```



The command **kubectl get svc -n iosmcn -o wide** is used in
Kubernetes to retrieve detailed information about services in a
specific namespace.
```
kubectl get svc -n iosmcn -o wide
```

The command is used for the following reasons:

-   **Monitoring**: Check the status and details of services running in
     a specific namespace.

-   **Debugging**: Identify issues with service configurations or
     connectivity.

-   **Management**: Ensure services are correctly set up and running as
     expected

**Checking the configuration file parameters & Running the
gNb:**

- Change the AMF IP in the gNB conf file **(test-xx.conf)** to  the IP that is mentioned in the above step.

- Check the **GNB_IPV_ADDRESS_FOR_NG_AMF** and **GNB_IPV_ADDRESS_FOR_NGU** and set it to the IP of the gNB Machine, here it is **192.168.108.149**

Run the **nr-softmodem** using the following command to start the gNB

```
sudo taskset -c 10 ./nr-softmodem -O ./(name-of-the-file).conf --sa --reorder-thread-disable 1 --thread-pool 3,4,5,7
```

> The command runs the nr-softmodem process on CPU core 10 with specific configuration and optimization options. It disables thread reordering and assigns threads to a pool of CPU cores (3, 4, 5, 7). This setup is used to optimize the performance and latency of the softmodem in a 5G network environment.

