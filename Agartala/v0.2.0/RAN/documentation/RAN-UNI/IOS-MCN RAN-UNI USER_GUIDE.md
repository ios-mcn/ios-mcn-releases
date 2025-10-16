# IOS MCN v0.2.0 Agartala Release - User Guide 
-----
The **IOS-MCN RAN Sub-Project** aim to deliver a functional, high-performance, and easily deployable Radio Access Network (RAN) based on open-source components such as *OpenAirInterface5G (OAI)*. This user guide outlines the complete process required to deploy a working 5G gNB (gNodeB) capable of interacting with either a LPRU or software-defined radio hardware like USRP B210.



# Purpose and Audience
-----
The purpose of this document is to  present the user guide of a private 5G RAN using open-source software, highlighting key components and deployment strategies.

The audience of this document is the end user who is trying to run the UNI RAN in different deployment environments.
1. Baremetal 
2. Containerized Docker Version

# IOS MCN RAN UNI Test Information
----
The setup is optimized for **low-latency, high-throughput performance**	on Ubuntu 22.04 LTS with **real-time kernel** support, DPDK-based user-space networking, and **BIOS-level optimizations**. It also covers advanced configurations such as CPU core isolation, clock synchronization using PTP, and Dockerized deployment for reproducibility and isolation.

Please refer installation guide.(Section 5.1)

# Supported Features
----

-This release consists of the following features:

>- Deployment Mode : Baremetal and Docker version
>- Band N78
>- Antenna Config - SISO and 2x2 MIMO,
>- SCS - 30 KHz
>- Bandwidth : 20 MHz, 40 MHz, 100 MHz
>- Modulation : upto 256 QAM
>- Ciphering : NEA0, NEA1, NEA2
>- Integrity : NIA1, NIA2
>- TDD Slot Configuration : DDDSU, DDDDDDDSUU
>- VoNR and ViNR
>- Peak Throughput (Downlink + Uplink) - 720+ Mbps (TDD Config - DDDSU)
>- End-2-End Data Latency <= 12 ms
>- Split option - option8 and option7.2
>- Connected UE capacity - 32 (Verified 4 UEs upto 2 Hours Stability)


# Supported Hardware
----

> **Hardware Environment Used for Testing:**
>
>-   *CPU:* 11th Gen Intel(R) Core(TM) i7-11700K @ 3.60GHz
>
>-   *Memory:* 64 GB DDR4
>
>-   *NIC:* Intel E810-XXV-4T (25GbE)
>
>-   *Storage:* NVMe SSD
>
>-   *Radio Hardware:*
>
>	-   USRP B210 (for split 8)
>
>	-   VVDN LPRU (for split 7.2)
> 
>-   *UE/MOBILE PHONE:* 5G IMS Enabled user equipments/mobile phones(preferably using **Android OS**)

Please refer to the UNI_Ran Installation Guide document for further details.

# How to Run and Boot up the CORE(Common For both Environments:Baremetal & Dockerized version)
----

- Please ensure that you have successfully installed an open-source Core server installed that you are trying to link to the RAN.
- In this section, the test environment uses IOSMCN-Core-server i.e., a part of the *Agartala v0.2.0 IOS-MCN CORE Sub-Project Release*. The relevant guides can be referred in the same repository.

**Booting up the IOSMCN-Core**
--

*Open IOSMCN-core in new terminal:*

We will access the IOSMCN-core server machine via **SSH** and view the status of **the 5G core elements/nodes** that are present on the Kubernetes cluster.

```
ssh administrator@192.168.x.X

Enter the Password: xxx@123(or whatever is configured)
```



**To watch pods status use the command mentioned below**
```
watch -n 1 kubectl get pods -A
```


![](../../documentation/RAN-UNI/images/ran_installation/image29.png) 

Figure#:Kubernetes pod watch output for core network validation



**1.1.** The command **kubectl get svc -n iosmcn -o wide** is used in Kubernetes to retrieve detailed information about services in a specific namespace.
```
kubectl get svc -n iosmcn -o wide
```


> The command is used for the following reasons:
>
>-   **Monitoring**: Check the status and details of services running in a specific namespace.
>
>-   **Debugging**: Identify issues with service configurations or connectivity.
>
>-   **Management**: Ensure services are correctly set up and running as expected

![](../../documentation/RAN-UNI/images/ran_installation/image30.png)

*The above image is the output of the above given command.*

**1.2. Checking the configuration file parameters & Running the gNb:**

> **1.2.1** Change the AMF IP in the gNB conf file **(test-xx.conf)** to the IP that is mentioned in the above step.
>
> **1.2.2** Check the **GNB_IPV_ADDRESS_FOR_NG_AMF** and **GNB_IPV_ADDRESS_FOR_NGU** and set it to the IP of the gNB Machine (Here it is **[192.x.X.149]**)

![](../../documentation/RAN-UNI/images/ran_installation/image31.png)

 Figure#:Checking gNB configuration file parameters before launch

> **1.2.3** Run the **nr-softmodem** using the following command to RUN THE RAN.
> Refer to the Installation Guide(Section 7)

# How to connect the supported hardware
	
	
**1. USRP**
----
**1.1. Configuration/Setup:**
----
 
Refer to the UNI_RAN Installation Documentation (link mentioned in the below table)

**1.2. Testing the Setup:**
----

This section describes the procedure to execute the **nr-softmodem binary** build for **USRP b210 board**. For execution we need to connect b210 on the machine on USB port 3.0.

![](../../documentation/RAN-UNI/images/ran_installation/image10.png)

Figure#: USRP B210 to gNB hardware connection diagram


After that start the nr-softmodem:

```
 untar release image file as tar -xzvf v.0.0.X.baremetal.tar.gz
 cd v.0.0.X.baremetal
 cd final_artifact
 mv bin/* .
 mv lib/* .
 mv utils/* .
 Set patchelf path if required
 Execute gNB binary as follows:
 sudo taskset -c 10 ./nr-softmodem -O ./<configuration file> --sa -E --usrp-tx-thread-config 1 --thread-pool 3,4,5
```

**Note**: *The argument to run nr-softmodem binaries are different for USRP you can see argument are different and for LPRU Argument passed in the command are different.*

**2. LPRU :**
--

**Before configuring the LPRU we need to run the following commands to make our system(gNB) ready on a configuration level and to synchronize the clocks with respect to the Grandmaster switch which provides GPS signals.**

 **The commands and their description in detail can be found on the link noted down below:**

 **2.1. Configuration/Setup:**
 ----

**To access this LPRU (LOW POWER RADIO UNIT)**
  
*We need to ssh into the machine with the below provided details:*


- Username - **root**

- IP Address - **192.168.4.50**

- Password: **vvdn**

![](../../documentation/RAN-UNI/images/ran_installation/image22.png) 

Figure#:Logging into LPRU terminal

**Logging into the terminal of the LPRU:**
----

Once you are logged in, Follow the below provided steps to sync up the LPRU, this includes the synchronization of radio unit, the compression setting , RF antenna configuration, channel parameters and other things.

**1. To track synchronization progress in real-time by filtering sync-related log entries until the system achieves synchronization.Run command:**


```
tail -f/var/logs/synctiming2.log| grep sync
```
**The user will wait until the unit synchronizes.**

- This command continuously monitors (tail -f) the **synctiming2.log** file and filters out lines that contain the word sync. You're essentially waiting and watching until a synchronization message appears in the log.

 ![](../../documentation/RAN-UNI/images/ran_installation/image23.png)
 
 Figure#:LPRU synchronization confirmation in terminal

- **You can also physically check the bottom most LED on the LPRU.**

- **It blinks red when the RU is not synchronized, and turns green when it is synchronized**


**2. To parse and load the e_2x2.xml configuration file for applying
    system or test setup parameters.Run command:**

  ```
  xml_parser e_2x2.xml
  ```

>-**Depending on whether we are running SISO (1x1) or MIMO (2x2) and e/f
Fronthaul Interface**
>
>- **For 1x1 use e_1x1.xml, for 2x2 use e_2x2.xml (both for phy-e/phy-f),**
>
>- **This command runs an XML parser tool to read and process the e_2x2.xml configuration file, which likely contains parameters or settings (e.g., antenna config, MIMO setup) used in the 5G lab environment.**




![](../../documentation/RAN-UNI/images/ran_installation/image24.png) 

Figure #:XML parser configuration script for LPRU (e_2x2.xml)



![](../../documentation/RAN-UNI/images/ran_installation/image25.png)

Figure#: Output of the xml_parser file

**3. To write the value 1919 to memory address a0010024 for configuring a specific hardware register or system setting that helps in compressing the data (e.g., I/Q samples) transmitted between the DU (Distributed Unit) and the RU (Radio Unit) over fronthaul interfaces (typically using the eCPRI or ORAN protocols). Run command:**

```
  mw.l a0010024 1919
```
- **This command writes the value 1919 to the memory address a0010024
using the mw.l (memory write long) command. It's typically used to
configure hardware registers, initialize components, or change
settings in embedded/5G systems.**

 
![](../../documentation/RAN-UNI/images/ran_installation/image26.png) 

Figure#: Memory register write command run in LPRU terminal

**4. To edit the live running configuration in Sysrepo using the vi
    editor and To configure and activate transmit carrier parameters ---
    including center frequency, bandwidth, duplex scheme, and RF gain
    --- by editing the system configuration and setting the carrier
    status to ACTIVE, thereby completing the RU's channel setup for 5G
    NR transmission. Run command:**
```
sysrepocfg --edit=vi -d running
```

- **Change 'INACTIVE' to 'ACTIVE' at two places and save the file.**

- **This command opens the running datastore of Sysrepo (a YANG-based
configuration datastore) for editing using the vi editor. It's used
to view or modify the current live configuration of a network
component or service.**

 ![](../../documentation/RAN-UNI/images/ran_installation/image27.png)

Figure#:Screenshot of sysrepocfg editor showing ACTIVE status

**Now, the RU configuration is done.**

**2.2. Testing the Setup:**
----

> After that **start the nr-softmodem**:
>Run the below mentioned commands after the user have successfully configured the LPRU.

```
cd <v.0.0.2.baremetal.tar.gz> #go the directory where the RAN-source package was unzipped and built.
```
```
 sudo taskset -c 10 ./nr-softmodem -O ./<configuration file> --sa -reorder-thread-disable 1 --thread-pool 3,4,5,7
```

- Check logs to validate that ran is up and running:

![](../../documentation/RAN-UNI/images/ran_installation/image28.png)

Figure#:gNB registration



**3. UE (User Equipment/Mobile Phones)**
---
**3.1. Configuration/Setup:**

**3.2. Testing the Setup:**

-   We will pow­­­­­­er on our UE (User Equipment).

-   Remove the flight mode as shown in the screenshot below which will
    in turn start the attach procedure.

![](../../documentation/RAN-UNI/images/ran_installation/image32.png) 

Figure#:Selecting the private 5G carrier on UE

![](../../documentation/RAN-UNI/images/ran_installation/image33.png)

Figure#:Removing airplane mode on UE to initiate attach procedure

![](../../documentation/RAN-UNI/images/ran_installation/image34.png)

Figure#:Console log on gNB indicating UE attach success

-   The image below shows that the UE has successfully attached and you
    can see the logs on the core side.

![](../../documentation/RAN-UNI/images/ran_installation/image35.png)

Figure#:AMF terminal log showing UE attachment and core interaction

# To Run the Dockerized Version 

The user needs to check the Docker image from the repository and follw the below given steps

## Load the images into Docker:

```
 sudo docker load -i /path/to/uni-ran-gnb.tar
```
## Launch the Container:

> With the below mentioned command the user can launch the 5G RAN node inside a prepared container, wires up its configuration and hardware,and also logs the boot process that will enable the user to a fully containerized and reproducible deployment

```
 docker-compose up | tee output.txt
```
For any related information please refer to the Installation and Developers Guide.(Sections 8 and 4 respectively.)

# Features:

The following section shows the usage of the feature that is supported with UNI RAN;

- **VoNR/ViNR**
  

## VoNR/ViNR:

  **1.1. Configuration/Setup**

> To use VoNR please go through the sections provided below:

### Prerequisites:
- Private 5G SA (Standalone) network with IMS support
- Two Android UEs with 5G NR and VoNR capability
- SIM cards provisioned for IMS services
- Core network configured for VoNR (AMF, SMF, UPF, IMS)
- gNodeB configured and operational



**1.1.1. Core Network Status Check**
- Verify AMF (Access and Mobility Management Function) is running
- Confirm SMF (Session Management Function) is operational
- Check UPF (User Plane Function) connectivity
- Validate IMS core components (P-CSCF, I-CSCF, S-CSCF, HSS/UDM)
- Ensure DNS resolution for IMS domains is configured

**1.1.2. Start the RAN(Radio Access Network) Check**
- Verify gNodeB is broadcasting 5G NR signals
- Confirm cell parameters (PCI, TAC, PLMN)
- Check that VoNR is enabled in gNodeB configuration
- Validate QCI/5QI profiles for voice services are configured



**1.1.3 SIM Card Configuration**
- Insert SIM cards with IMS provisioning in both UEs
- Verify SIM cards have correct IMSI, Ki, OPc values
- Confirm IMS APN settings are provisioned on SIM
- Check that VoLTE/VoNR flags are enabled in SIM profile

**1.1.4. Android UE Settings - UE1**
1. Power on the first Android UE
2. Navigate to **Settings > Mobile Network**
3. Select your carrier/SIM card
4. Enable **5G** network mode


**1.1.5. Android UE Settings - UE2**
Repeat the same configuration steps as UE1:
1. Power on the second Android UE
2. Configure identical network and call settings
3. Ensure both UEs use the same network operator settings

**1.1.6. UE1 Registration Process**
1. Verify UE1 shows **5G** or **5G SA** in status bar
2. Check signal strength is adequate (-70 dBm or better)
3. Confirm UE has obtained IP address via PDU session
4. Monitor registration logs for successful AMF attachment
   - Check: Registration Accept message received
   - Verify: Security context established
   - Confirm: Default bearer established

**1.1.7. UE2 Registration Process**
1. Repeat registration verification for UE2
2. Ensure both UEs are registered to same AMF/cell
3. Verify both UEs have active PDU sessions

**1.1.8. Verify VoNR is Active on Both UEs On each UE**

1.	Check "IMS Status":Registered.
2.	Verify network type: NR or 5G.
3.	Confirm "VoNR" icon is visible in the status bar.

## 1.2. Testing Procedure

**1.2.1. Outgoing Call - UE1 to UE2**
1. On UE1, open the phone dialer
2. Dial the number assigned to UE2
3. Press call button
4. Monitor that call stays on 5G (no fallback to 4G)
5. Verify call setup time is acceptable (< 3 seconds)

**1.2.2. Call Progress Monitoring**
During call setup, verify:
- SIP INVITE sent through IMS core
- Media negotiation completed
- RTP stream established over 5G NR
- No circuit-switched fallback occurs
- Voice quality is acceptable

**1.2.3. Bidirectional Call Testing**
1. Answer call on UE2
2. Test audio quality in both directions
3. Verify call remains on 5G NR throughout
4. Test call hold/resume functionality
5. Test call transfer if supported

**1.2.4. Incoming Call - UE2 to UE1**
1. End the first call
2. Initiate call from UE2 to UE1
3. Repeat all verification steps
4. Confirm bidirectional VoNR capability



## Succcesfull implementation
- Both UEs registered on 5G SA network  
- IMS registration successful on both UEs  
- VoNR calls establish without CS fallback  
- Good voice quality in both directions  
- Call setup time < 3 seconds  
- Calls remain on 5G throughout duration  
- Basic supplementary services functional  

## Monitoring and Logs
- Core network logs (AMF, SMF, IMS)
- gNodeB performance counters
- UE field test logs
- SIP signaling traces
- RTP media quality metrics 


# Related Artifacts & links

This section contains list of related documents to the UNI RAN PROJECT. 

| Document Name       | Purpose | Link  |
|---------------------|---------|-------|
| Integration Guide   |  To integration with Radio unit and Core|https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.2.0/RAN/documentation/RAN-UNI/IOS-MCN%20RAN-UNI%20Integration%20Guide.md   |
| Developers Guide    | To build UNI RAN in Different environment       | https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.2.0/RAN/documentation/RAN-UNI/IOS-MCN%20RAN-UNI%20DEVELOPER_GUIDE.md      |
|Installation Guide  |  To install the UNI RAN environment    | https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.2.0/RAN/documentation/RAN-UNI/IOS-MCN%20RAN-UNI%20INSTALLATION_GUIDE.md     |
|Troubleshooting Guide|To help the user troubleshoot issues         | https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.2.0/RAN/documentation/RAN-UNI/IOS-MCN%20RAN-UNI%20TROUBLESHOOTING_GUIDE.md    |




	

