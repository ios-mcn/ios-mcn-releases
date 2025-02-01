## This document explains how to build and deploy the images from source-code.

Step 1 : untar the iosmcn.agartala.v0.1.0.core.ran.tar.gz

```sh
tar -xvzf iosmcn.agartala.v0.1.0.core.ran.tar.gz

```
# System Initialization 
### System configuration for the setup:
**CPU:** Intel® Xeon® Gold 6544Y Processor </br>
**Memory:** 8x16 DDR5 5200 memory </br>
**Operating system:** Ubuntu 22.04 LTS </br>
**Kernel:** 5.15.0-1032-realtime </br>
**NIC:** Intel E810 XXV DA4T </br>
**NIC firmware version:** 4.01 0x800135e7 1.3256.0 </br>
**Driver for NIC:** ice 1.12.7 </br>
**Linux PTP version:** 3.1.1 </br>

**Step 1:** Installing real time kernel and setting up the grub configuration
```sh
$ sudo apt install linux-realtime
```
> **Note:** you must select the realtime kernel version 5.15.0-1032-realtime.
 
Open the grub configurations in ```etc/default/grub```
```sh
$ sudo vi /etc/default/grub
```
change the GRUB_CMDLINE_LINUX_DEFAULT to the following mentioned,
```sh
GRUB_CMDLINE_LINUX_DEFAULT="isolcpus=0-17 nohz_full=0-17 rcu_nocbs=0-17 kthread_cpus=18-31 rcu_nocb_poll nosoftlockup default_hugepagesz=1GB hugepagesz=1G hugepages=20 intel_iommu=on iommu=pt mitigations=off skew_tick=1 selinux=0 enforcing=0 tsc=reliable nmi_watchdog=0 softlockup_panic=0 audit=0 vt.handoff=7"
```
and also change the GRUB_ DEFAULT to the following mentioned.
```sh
GRUB _DEFAULT="Advanced options for Ubuntu>Ubuntu, with Linux 5.15.0-1032-realtime"
```
 
> **Note:** The isolation of the CPU must be done according to the CPU that is used, depending on which cores of the CPU operate at higher frequency or performance-oriented cores, isolate those CPUs and assign them to the gNB. 
After saving the grub changes update grub using the command 
```sh
$ sudo update-grub
```
Restart the system and check if the DPDK huge pages are allocated.
```sh
$ cat /proc/meminfo | grep Huge
```
 
Refer the PTP document for synchronization setup and make sure systems are in sync before Running the DU.

**Step 2:** Installing and configuring tuneD. 
TuneD is a service used to tune your system and optimise the performance under certain workloads. At the core of TuneD are profiles, which tune your system for different use cases.

2.0 Installing tuneD.
```sh
 $ sudo apt install tuned
```
**Step 2.1** After installing tuned package, you must set tuned-adm to realtime by following command.
> **Note:** If you have isolated the CPU core in the grub configuration, then you must update the isolated core number in /etc/tuned/realtime-variables.conf, then you must execute the previous command or else it will throw an error. 

 ```sh
$ tuned-adm profile realtime
```
After this You can check current tuned profile by running
```sh
$ tuned-adm profile
```

**Step 3:** Installing the dependencies </br>
The following commands installs all the dependencies required to install the RAN setup. 
```sh
$ sudo apt install make gcc cmake git meson -y
```

**Step 4:** Installing and configuring DPDK (version.20.11.9) </br>
DPDK (Data Plane Development Kit) is an open-source software project that provides a set of libraries and network interface controller polling-mode drivers for accelerating packet processing workloads on various CPU architectures. It allows offloading TCP packet processing from the operating system kernel to processes running in user space.

4.1 Download the DPDK source code and extract it.
```sh
 $ cd ~/ 
 $ wget http://static.dpdk.org/rel/dpdk-20.11.9.tar.gz 
 $ tar -xf dpdk-20.11.9.tar.gz
```

4.2 Export the necessary environment variables?
```sh
$ export RTE_TARGET=x86_64-native-linuxapp-gcc
$ export RTE_SDK=~/dpdk-stable-20.11.9
$ export RTE_INCLUDE=${RTE_SDK}/${RTE_TARGET}/include
$ cd ${RTE_SDK}
```

4.3 Build DPDK (Data Plane Development Kit) libraries
```sh
$ meson build 
$ cd build
$ sudo ninja install
```

**Step 5:** Download and install dpdk-kmod for igb_uio driver. </br>
DPDK-kmods is a repository of kernel modules or add-ons for DPDK. Follow the following steps to install and use igb_uio module. 
5.1 Get the igb_uio source.
```sh
$ cd ~
$ git clone http://dpdk.org/git/dpdk-kmods
```

5.2 Compile the igb_uio driver.
```sh
$ cd ~/dpdk-kmods/linux/igb_uio
$ make
```

5.3 Load the igb_uio driver.
```sh
$ modprobe uio
$ insmod igb_uio.ko
```

**Step 6:** Installing and setting up linuxptp. </br>
Clone the single setup script from safwan’s public repository.
```sh
$ git clone https://github.com/safwan2m/single-setup-script.git
$ cd ~/single-setup-script/ptp_install
```
Change the FH interface in .env file according to the system FH interface. 
```sh
$ vi .env
```

```sh
$ sudo ./install_linuxptp.sh
```

**Step 7:** setup virtual functions:
```sh
$ cd ~/single-setup-script/du_startup
```
Change the FH interface, FH_NIC_BUS_ID and VLAN in .env file according to the system FH interface. 
 
To get the FH_NIC BUS_ID run, and get the bus id according to the number of interface
```sh
$ lspci | grep Eth
```
 
If VLAN is not required set the FH_CU_VLAN to 0 in .env.
```sh
$ sudo ./service-running.sh
```

The virtual functions created can be verified by running.
```sh
$ ip link show <interface_name>
Example: 
```

**Step 8:** Setting up the DHCP server.
```sh
$ cd ~/single-setup-script/dhcp_server_setup
$ sudo ./install_dhcp_server.sh
```

**Step 9:** Build and install the RAN. </br>
You can use the make commands provided in the build to install the RAN dependencies and the RAN.
```sh
$ cd ~/ios-mcn-ran-distributed/
$ sudo make dependency
$ sudo make all
$ sudo make install
```

**Step 9:** Configuring the RU using GUI/Netconf. </br>
9.1 IP assigned to the RU can be obtained by running dhcp-lease-list command. 
```sh
$ dhcp-lease-list
```
 
9.2	login to the GUI of the RU using the RUs IP. The username and password of the RU is 
username: oranuser
password: oranuser
 
 

9.3	Once logged into the RU go to configuration and RF calibration to set the center frequency of the RU. 
 
9.4	Activate the carrier of the RU before transmission. 
The carrier of the RU should be activated before transmission only after the RU is synchronized, this can be verified using the sync light turning green on the VVDN Gen 3 RU. 
```sh
$ cd ~/single-setup-script/ru_startup
$ ./setup-ru.sh
```
When prompted for root password enter: vvdn
if prompted for system password enter: \<enter the system password>

# Execution

Run the CU-CP
```sh
$ sudo ./cmake_targets/ran_build/build/nr-softmodem --sa -O targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb-cucp.sa.f1-e1-oaicore.conf
```
Run the CU-UP
```sh
$ sudo ./cmake_targets/ran_build/build/nr-cuup --sa -O targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb-cuup.sa.f1-e1.conf
```
Run the DU
```sh
$ sudo ./cmake_targets/ran_build/build/nr-softmodem --sa -O targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb-du.sa.band78.273PRB.1x1-f1-e1-vvdn.conf --thread-pool 12,13,14,15 --mplane
```
# System bring up
- Every time the system is restarted the following steps must be followed before running the gNB. </br>
- Ensure the isc-dhcp-server is running. </br>
- Ensure the virtual functions are created and specified with correct MAC address and VLAN. </br>
- RU is assigned with proper IP address and configurable using Netconf. </br>
