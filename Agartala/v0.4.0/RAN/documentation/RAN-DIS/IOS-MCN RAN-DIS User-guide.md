# User guide
This guide describes how to deploy and run the various components of the IOS-MCN-RAN project. All build artifacts are generated under the build directory inside the main **ios-mcn-ran** directory. Refer to the [Installation Guide](./IOS-MCN%20RAN-DIS%20Installation-guide.md) for steps to build and install the RAN.

⚠️To run the Distributed Unit in split 7.2 configuration, with Lekha or a VVDN radios, 
the following pre-requirsites are needed to be completed. [Prerequisites](./IOS-MCN%20RAN-DIS%20ORAN-FHI7.2-Tutorial.md)
```
cd ios-mcn-ran
```
The following are the commands to run CU-CP, CU-UP and DU,
- [Run CU-CP](#run-cu-cp)
- [Run CU-UP](#run-cu-up)
- [Run DU](#run-du)
  - [Split 8](#split-8)
  - [Split 7.2](#split-72)
- [XN Handover](#xn-handover)
- [Run UE with RFSIM](#run-ue-with-rfsim)
- [COTS UE usage](#cots-ue-usage)
- [Including RIC interfaces O1 and/or E2](#including-ric-interfaces-o1-andor-e2)
- [Run with RU M plane](#run-with-ru-m-plane)

![ran architecture with IP](<./images/ran architecture - ip.svg>)
## Run CU-CP:
To start the Central Unit - Control Plane(CU-CP):
```
sudo nr-softmodem -O ./conf/gnb-cucp.sa.f1-e1.iisc.conf 
```
Configurations are to be modified in the above ``.conf`` file. Modify the ``plmn_list``, ``amf_ip_address``, ``GNB_IPV4_ADDRESS_FOR_NG_AMF`` and ``tracking_area_code`` according to your deployment.

When deploying using ios-mcn-core, retrieve the IP addresses of the AMF and UPF by logging into the core system and executing the following commands:
```bash
# List the services in the core network and note the Cluster IP of the AMF
kubectl get svc -n iosmcn

# Display the IP address of the UPF interface(access) connected to the access network
ip a show access
```

## Run CU-UP:
To start the Central Unit - User Plane (CU-UP):
```
sudo nr-cuup -O ./conf/gnb-cuup.sa.f1-e1.iisc.conf
```
This guide assumes that the CU-CP, CU-UP, and DU components are deployed on a single server. If they are deployed on separate servers, make sure to update the IP addresses for ``ipv4_cucp``, ``ipv4_cuup``, ``local_s_address``, and ``remote_s_address`` in their respective configuration files to reflect the correct network setup.
## Run DU:
The Distributed Unit (DU) can be launched in two main configurations:

1. Split 8 setups are typically used with SDRs like USRP, where the PHY resides on the DU machine.
2. In Split 7.2, the L1 PHY is split up, and Fronthaul communication is handled over e-CPRI (Ethernet using a dedicated PHY interface library).

![Split 8](<./images/ran architecture - split 8.svg>) ![Split 7.2](<./images/ran architecture - split 7.2.svg>)
<br>
### Split 8
In split 8 depending on the requirements, simulate the RF channel by running the DU in RFSIM mode (If no radio is available) or with a USRP radio to radiate over the air. 
Depending on the radio either a B210 or an X310 configuration file can be used
```bash
# For B210
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.106PRB.1x1-f1-e1-usrpb210.conf

# For X310
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.106PRB.1x1-f1-e1-usrpx310.conf
```
To run with RF simulator one can use the argument ``--rfsim``

```
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.106PRB.rfsim.conf --rfsim --gNBs.[0].min_rxtxtime 6
```
### Split 7.2
⚠️To run in split 7.2 configuration, with Lekha or a VVDN radios, 
the following pre-requirsites are needed to be completed. [Prerequisites](./IOS-MCN%20RAN-DIS%20ORAN-FHI7.2-Tutorial.md)
```
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.273PRB.1x1-f1-e1-lekha.iisc.conf --thread-pool 12,14
```

## Run UE over RFSIM:
To run UE over RFSIM to connect with DU, one can run UE with the following command, the center frequency and other parameters should be changed according to the setup. Refer the following for more [details](./IOS-MCN%20RAN-DIS%20RUNUEMODEM.md).
```
sudo nr-uesoftmodem -O ./conf/ue.sa.conf -C 3619200000 -r 106 --ssb 512 --numerology 1 --rfsimulator.serveraddr 127.0.0.1
```

## COTS UE usage
The following are the list of UEs that are tested in our lab.
|UE         | model and chipset                                                                    |
|-----------|--------------------------------------------------------------------------------------|	 
|1	        |OnePlus Nord CE 3 Lite 5G(CPH2467)	Qualcomm Snapdragon 695 5G Octa Core               |
|2	        |Samsung Galaxy A15 5G(SM-A156E/DS)	MediaTek Dimensity 6100+                           |
|3	        |Lava Blaze 5G(LAVA LXX503)	MediaTek Dimensity 700                                     |
|4	        |OnePlus Nord CE 4 Lite 5G(CPH2619)	Qualcomm Snapdragon 695 5G Octa Core               |
|5	        |Oppo F23 5G(CPH2527)	Qualcomm Snapdragon 888 Octa Core                              |
|6	        |OnePlus Nord CE4(CPH2613)	Qualcomm Snapdragon 7 Gen 3                                |
|7	        |Oneplus 9 5G	Qualcomm Snapdragon 888 Octa Core                                      |
|8	        |Oppo F23 5G(CPH2527)	Qualcomm Snapdragon 888 Octa Core                              |
|9	        |Optimus Rhino 5G	MediaTek Dimensity 900 octa-core                                   |
|10	        |Oneplus Nord CE3 5G	Qualcomm Snapdragon 782G  Octa Core                            |
|11	        |Samsung Galaxy A14 5G	Exynos 1330 Octa Core                                          |
|12	        |Samsung Galaxy M15 5G	MediaTek Dimensity 6100+                                       |
|13	        |Oppo A3 Pro 5G 	MediaTek Dimensity 6300                                            |
|14	        |Vivo T3x 5G	Qualcomm Snapdragon 6 Gen 1                                            |
|15	        |Realme p2 Pro 5G 	Qualcomm Snapdragon 7 Gen 2                                        |
|16	        |Moto G85 5G	Qualcomm Snapdragon 6s Gen3                                            |
|17	        |Moto G35 5G	Unisoc T760 Octa Core                                                  |
|18	        |Oppo F27 5G 	MediaTek Dimensity 6300                                                |
|19	        |Lava Agni 2(LAVA LXX504) 	MediaTek Dimensity 7050                                    |

COTS UEs (with programmable SIMs from OpenCells) are used for integration testing.
### SIM Card
Program UICC/SIM Card with [Open Cells Project](https://open-cells.com/) programming tool [uicc-v3.3](https://open-cells.com/d5138782a8739209ec5760865b1e53b0/uicc-v3.3.tgz).

```bash
# Download the SIM programmer tool
wget https://open-cells.com/d5138782a8739209ec5760865b1e53b0/uicc-v3.3.tgz

# Unzip the zip file
tar -xvf uicc-v3.3.tgz

# Navigate to the unzipped directory
cd uicc-v3.3

# Build the programmer
make 

# Connect the USB with the programmable SIM and program the SIM with the following command
sudo ./program_uicc --adm 12345678 --imsi 001010000000001 --isdn 00000001 --acc 0001 --key fec86ba6eb707ed08905757b1bb44b8f --opc C42449363BBAD02B66D16BC975D77CC1 -spn "IOSMCN" --authenticate

# To check if the SIM is programmed run
sudo ./program_uicc
# ..and check if the IMSI matches with the one in the earlier command.
```
>⚠️**NOTE:** Use NetMonster or similar tools to set the phone preferred network type to NR only, to be able to detect and connect to 5G stand-alone (SA) network. 

## Containerized deployment

The deployment is as easy as modifying the .env file, and configuration files according to the deployment, in the .env file configure the ```REPOSITORY=ios-mcn``` and ```VERSION=v0.4.0```
```bash
cd ios-mcn-ran/cicd/5g_sa_b200_40MHz/
# Modify the .env file with the Organization and Image version.
vi .env

# Go back to ios-mcn-ran/conf
cd ios-mcn-ran/conf/
# Modify the CU-CP configuration file with PLMN and AMF IP address.
vi gnb-cucp.sa.f1-e1.iisc.conf
vi gnb-cuup.sa.f1-e1.iisc.conf

# The DU configuration file can be modified with the required frequency and bandwidth.
vi gnb-du.sa.band78.106PRB.1x1-f1-e1-usrpb210.conf
```

To bring up the container run ```docker-compose up -d```. </br>
```bash
cd ios-mcn-ran/cicd/5g_sa_b200_40MHz/
docker-compose up -d
```

To bring down the container run ```docker-compose down```.</br>
```bash
cd ios-mcn-ran/cicd/5g_sa_b200_40MHz/
docker-compose down
```

To check the status of the containers run ```docker ps -a```.
```bash
docker ps -a
```

The container logs can be checked using the command ```docker logs -f <contaienr_name>```.</br>
```bash
# Example
docker logs -f ios-mcn-cucp
```

# Advanced deployment
## Including RIC interfaces O1 and/or E2.
IOS-MCN-RAN supports integration with SMO and RIC:
### O1-adapter
o1-adapter is used for setting up an O1 interface for the RAN components, o1-adapter connects to the RAN components using the telent interface. Documentation for the telnet interface in the RAN. [telnet-o1](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/common/utils/telnetsrv/DOC/telneto1.md)
Documentation to setup the O1 interface to the RAN. [Documentation](https://gitlab.eurecom.fr/oai/o1-adapter)

<img alt="o1-adapter" src="./images/image.png" width="70%">

### Run o1-adapter with DU
On the **DU** side, enable the Telnet server to allow O1-adapter communication.  
Use the following parameters:
- `--telnetsrv` — enables the Telnet server  
- `--telnetsrv.shrmod o1` — loads the O1 shared module  
- `--telnetsrv.listenport <port-number>` — sets the Telnet port (default: `9090`)
```
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.273PRB.1x1-f1-e1-lekha.iisc.conf --thread-pool 12,14 --telnetsrv --telnetsrv.shrmod o1 --telnetsrv.listenport 9090
```
IOS-MCN version fo the o1-adapter supports running o1-adapter for disaggregated RAN components(CU-CP, CU-UP and DU). On the o1-adapter side.
```bash
cd cicd/5g_fh72_tdd_100MHz/

# Modify the additional paramters to --du (command: ["--du", "-c", "/docker/config/du_config.json"]) for DU
# or ["--cu-cp", "-c", "/docker/config/cu_cp_config.json"]) for CU-CP
# for CU-UP ["--cu-up", "-c", "/docker/config/cu_up_config.json"])
# Modify the Netconf port and sftp port as per the requirement and volume mount the configuration file appropriately in docker-compose-o1.yaml
vi docker-compose-o1.yaml
```
The configuration files are present ``conf/o1-config/config`` of the ios-mcn-ran project, and are needed to be volume mounted to the docker container appropriately in the ``docker-compose-o1.yaml``.
```bash
cd ios-mcn-ran
ls -ltr conf/o1-config/config
# drwxrwxr-x 2 root root 4096 Dec 24 15:40 ./
# drwxrwxr-x 3 root root 4096 Nov 24 16:10 ../
# -rw-rw-r-- 1 root root 1568 Nov 24 16:10 cu_cp_config.json
# -rw-rw-r-- 1 root root 1545 Nov 24 16:10 cu_up_config.json
# -rw-rw-r-- 1 root root 1573 Nov 24 16:10 du_config.json
# -rw-rw-r-- 1 root root 3331 Dec 24 15:40 pmData-measData.xml
# -rw-rw-r-- 1 root root 1699 Aug 12 14:33 ves-clear-alarm.json
# -rw-rw-r-- 1 root root 1924 Aug 12 14:33 ves-file-ready.json
# -rw-rw-r-- 1 root root 1050 Aug 12 14:33 ves-heartbeat.json
# -rw-rw-r-- 1 root root 1981 Aug 12 14:33 ves-new-alarm.json
# -rw-rw-r-- 1 root root 1913 Aug 12 14:33 ves-pnf-registration.json
# -rw-rw-r-- 1 root root  776 Aug 12 14:33 vsftpd.conf
# -rw-rw-r-- 1 root root    8 Aug 12 14:33 vsftpd.userlist
```
In the component configuration files(``cu_cp_config.json``, ``cu_up_config.json`` or ``du_config.json``), under the ``network.host`` add the IP address of the machine running the adapter-gnb, ``network.username`` and ``network.password`` for the container are ``netconf`` and ``netconf!``. In the ``ves.url`` add the url of the ves listening port(``http://IP-address:Port/eventListener/v7``). Under ``telnet.host`` and ``telnet.port`` add the IP address and port of the telnet interface open in the respective RAN component. </br>
Once the above configurations are done run adapter-gnb,
```bash
# Navigate to the folder with docker-compose-o1.yaml
cd ios-mcn-ran/cicd/5g_fh72_tdd_100MHz/
docker compose -f docker-compose-o1.yaml up -d
```
### Run with RU M plane

M plane allows to setup, configure and get performance metrics from the RUs, this has been tested with the following RUs
- Lekha MaRUt Low power radio unit
- VVDN LPRU

The IOS-MCN deployment of the RAN with M plane is hierarchical model, where the DU connects with the SMO to get the configurations and the DU connects with the RU, to push the configurations and get the performance metrics from the RU. 

In order for the DU to connect with the RU over ``NETCONF``(underly protocol is SSH) without password, copy the DU public key to the RU. 
```bash
# Generate a id_rsa and id_rsa.pub key using ssh-keygen
ssh-keygen -t rsa -b 4096 -f /path/to/your/keyname
# preferably in the .ssh folder of your user-directory /home/user/.ssh/id_rsa
# generates id_rsa.pub and id_rsa, public and private keys

# Copy the public key to the authorized_keys of the radio unit allowing passwordless SSH to the RU
ssh-copy-id <ru_username>@<ru_ip_address>
```

#### M plane section in the DU configuration file 
```bash
    fhi_72 = {
      dpdk_devices = ("0000:b1:01.0", "0000:b1:01.1");
      system_core = 2;
      io_core = 6;
      worker_cores = (4);
      du_addr = ("00:11:22:33:44:66", "00:11:22:33:44:66");
      ru_addr = ("98:ae:71:04:83:a3", "98:ae:71:04:83:a3");
      ru_ip_addr = ("192.168.4.42");
      du_key_pair = ("/home/nr5glab-server/.ssh/id_rsa.pub", "/home/nr5glab-server/.ssh/id_rsa");
      vlan_tag = (100, 100);
      mtu = 8870; # check if xran uses this properly
      fh_config = ({
        ...  
        ...
        ru_config = {
          ...
        };
        prach_config = {
          eAxC_offset = 1;
        };
      });
    };
```
Configure the fhi_72 section with `du_key_pair`, `ru_ip_address`, and `ru_username` inorder for the DU to connect with RU over M plane over SSH.

On the DU side to run with RU M plane use the configuration with ``-mplane.*.conf`` configuration file and ``--mplane`` parameter.
```
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.273PRB.1x1-f1-e1-lekha.iisc.conf --thread-pool 12,14 --mplane
```

On the o1-adapter side too run with ``--mplane`` to use the paramters sent by the RAN with respect to M plane.
```bash
# Modify the additional paramters to run with Mplane (command: ["--du", "-c", "/docker/config/du_config.json", "--mplane"])
cd cicd/5g_fh72_tdd_100MHz/
vi docker-compose-o1.yaml

docker compose -f docker-compose-o1.yaml up -d
```

#### RU reset
Resetting the RU over M plane is only supported by the VVDN RU. To reset the RU the above hierarchical configuration of the M plane needs to completed, connect to the DU over NETCONF and push the reset-rpc to the DU. 
```bash
# We use netopeer2-cli to send the reset-rpc to the DU.
$ netopeer2-cli
> connect --ssh --login netconf --host <adapter-gnb-ip-address>
# once connected send the reset-rpc using the user-rpc command(opens a editor and paste the following rpc)
> user-rpc
# <reset xmlns="urn:o-ran:operations:1.0"></reset>
# once the rpc is pushed successfully you'll see OK as the response from the netopeer2-server
# If the rpc is pushed successfully the RU will be reset after this.
```
### E2 Agent
E2 interface for the RAN components is enabled by providing the e2 details in the configuration file. Documentation to setup E2 interface.[Documentaion](https://gitlab.eurecom.fr/oai/openairinterface5g/-/tree/develop/openair2/E2AP) <br>
![near RT RIC](<./images/nearRT ric.svg>)

For more details on development, Please refer the [Developers guide](./IOS-MCN%20RAN-DIS%20developer-guide.md). <br><br>
Troubleshooting guide shared for the issues faced. [Troubleshooting](./IOS-MCN%20RAN-DIS%20Troubleshooting-guide.md)