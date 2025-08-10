# User guide
This guide describes how to deploy and run the various components of the IOS-MCN-RAN project. All build artifacts are generated under the build directory inside the main **ios-mcn-ran** directory. Refer to the [Installation Guide](./IOS-MCN%20RAN-DIS%20Installation-guide.md) for steps to build and install the RAN.
```
cd ios-mcn-ran
```
The following are the commands to run CU-CP, CU-UP and DU,
- [Run CU-CP](#run-cu-cp)
- [Run CU-UP](#run-cu-up)
- [Run DU](#run-du)
  - [Split 8](#split-8)
  - [Split 7.2](#split-72)
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
Configuration details can be customized in the above ``.conf`` file. Modify the ``plmn_list``, ``amf_ip_address``, ``GNB_IPV4_ADDRESS_FOR_NG_AMF`` and ``tracking_area_code`` according to your deployment.

If the deployment includes ios-mcn-core, you can retrieve the IP addresses of the AMF and UPF by logging into the core system and executing the following commands:
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

## Run UE with RFSIM:
To run UE with RFSIM to connect with DU, one can run UE with the following command, the center frequency and other parameters should be changed according to the setup. Refer the following for more [details](./IOS-MCN%20RAN-DIS%20RUNUEMODEM.md).
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
>⚠️**NOTE:** Use Netmonster or similar tools to configure the phone preferred network type to NR only, to be able to detect and connect to 5G network.

## Containerized deployment

The deployment is as easy as modifying the .env and the configuration files
```bash
cd ios-mcn-ran
# Modify the .env file with the Organization and Image version.
vi cicd/5g_sa_rfsim/.env

# Modify the CU-CP configuration file with PLMN and AMF IP address.
vi conf/gnb-cucp.sa.f1-e1.iisc.conf
vi conf/gnb-cuup.sa.f1-e1.iisc.conf

# The DU configuration file can be modified with the required frequency and bandwidth.
vi conf/gnb-du.sa.band78.106PRB.1x1-f1-e1-usrpb210.conf
```
and running docker-compose up -d. </br>
```bash
cd cdcd/5g_sa_rfsim
docker-compose up -d
```


# Advanced deployment
## Including RIC interfaces O1 and/or E2.
IOS-MCN-RAN supports integration with SMO and RIC:
### O1-adapter
O1-adapter is used for setting up an O1 interface for the RAN components, O1-adapter connects to the RAN components using the telent interface. Documentation for the telnet interface in the RAN. [telnet-o1](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/common/utils/telnetsrv/DOC/telneto1.md)
Documentation to setup the O1 interface to the RAN. [Documentation](https://gitlab.eurecom.fr/oai/o1-adapter)

<img alt="o1-adapter" src="./images/image.png" width="70%">

### Run with RU M plane
On the DU side to run with RU M plane use the configuration with ``-mplane.*.conf`` configuration file and ``--mplane`` parameter.
```
sudo nr-softmodem -O ./conf/gnb-du.sa.band78.273PRB.1x1-f1-e1-lekha.iisc.conf --thread-pool 12,14 --mplane
```
On the o1-adapter side too run with ``--mplane`` to use the paramters sent by the RAN with respect to M plane.
```
sudo gnb-adapter -c ./o1-config/config/conf.json --mplane
```
### E2 Agent
E2 interface for the RAN components is enabled by providing the e2 details in the configuration file. Documentation to setup E2 interface.[Documentaion](https://gitlab.eurecom.fr/oai/openairinterface5g/-/tree/develop/openair2/E2AP) <br>
![near RT RIC](<./images/nearRT ric.svg>)

For more details on development, Please refer the [Developers guide](./IOS-MCN%20RAN-DIS%20developer-guide.md). <br><br>
Troubleshooting guide shared for the issues faced. [Troubleshooting](./IOS-MCN%20RAN-DIS%20Troubleshooting-guide.md)