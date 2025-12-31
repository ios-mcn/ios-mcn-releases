## **Xn Handover Tutorial**
This guide explains how to perform an **Xn-based handover** in IOS-MCN.  
It covers both **COTS UE** and **NR UE (in RFsim mode)** test scenarios.

## Table of Contents

- [Xn Handover Overview](#xn-handover-overview)
- [Build with telnet support](#build-with-telnet-support)
- [XNAP Configuration in CUCP](#xnap-configuration-in-cucp)
- [Neighbour configuration](#neighbour-configuration)
- [Xn Handover configuration files](#xn-handover-configuration-files)
- [Bringing up the setup](#bringing-up-the-setup)
  - [Steps to run Xn Handover with COTS UE](#steps-to-run-xn-handover-with-cots-ue)
  - [Steps to run Xn Handover with NR UE in RFsim mode](#steps-to-run-xn-handover-with-nr-ue-in-rfsim-mode)
  - [Performing Xn-Handover with Lekha RU](#performing-xn-handover-with-lekha-ru)

## Xn Handover Overview
An Xn handover involves the transfer of a UE from one gNB to another gNB, where both the gNBs are connected to the same 5G core network. In F1 handover, the CU handles the process internally between its DUs and in N2 handover requires signaling through the AMF. In Xn Handover, signaling happens between CUCPs via Xn-C.

We assume:
* Two independent gNBs connected to the same 5GC.
* A UE is initially connected to a gNB (source gNB), which will be handed over to neighbour gNB (target gNB).
* Handover is triggered by either a decision based on measurement event (e.g. A3) or telnet command.

## Build with telnet support

If running [RF Simulator mode with NR UE](./README.md#run-ue-in-rfsim-mode), since the UE does not support any measurement reporting, it cannot trigger a handover on its own; it has to be triggered manually through telnet. Thus, build both gNB and NR UE as well as activate the build of telnet to that purpose:

`./build_oai --ninja --nrUE --gNB --build-lib telnetsrv`


## XNAP Configuration in CUCP
In your CUCP configuration file, add the XNAP section under the gNBs section (below `E1_INTERFACE`):

```bash
    XNAP :
    {
         ENABLE_XN = 1;
         GNB_PORT_FOR_XNC            = 38423;
         GNB_IP_ADDRESS_FOR_XNC      = "10.32.14.191"; // <local_system_ip> 
         Target_gNB_XN_address       = ({ ip = "10.32.14.192";});
    }
```
> To disable Xn, set `ENABLE_XN = 0`.

## Neighbour Configuration
In order to enable handovers (triggered by the UE event-based measurement reports e.g., A3 event), you have to configure the neighbour relation of the DUs at the CU. To do so, proceed as follows:


1. To simplify filling the right values in the neighbour configuration, you can rely on the information the CUCP has about the DU. Bring up the gNBs. Navigate to the directory from which you started the CUCP, and print RRC statistics:
   ```
   cat nrRRC_stats.log
   ```
1. Fill in the [`neighbour-config.conf`](../conf/xn_conf_files/neighbour-config.conf) configuration file as shown below, and
   `@include` it in the CUCP file.
1. Start both gNBs.
1. Bring the phone close to one cell, and leave flight mode. It should connect to the gNB to which it is closer.
1. Move the UE towards the other gNB; it should trigger an "A3 event" (Neighbour Becomes Better than Serving by an offset), and the CUCP will trigger the handover towards the other gNB.

```
neighbour_list = (
  {
    nr_cellid = 12345678;
    neighbour_cell_configuration = (
      {
        gNB_ID = 0xe01;
        nr_cellid = 11111111;
        physical_cellId = 1;
        absoluteFrequencySSB = 643296;
        subcarrierSpacing = 1; #30 KHz
        band = 78;
        plmn = { mcc = 001; mnc = 01; mnc_length = 2};
        tracking_area_code = 1;
      }
    )
  },
  {
    nr_cellid = 11111111;
    neighbour_cell_configuration = (
      {
        gNB_ID = 0xe00;
        nr_cellid = 12345678;
        physical_cellId = 0;
        absoluteFrequencySSB = 643296;
        subcarrierSpacing = 1; #30 KHz
        band = 78;
        plmn = { mcc = 001; mnc = 01; mnc_length = 2};
        tracking_area_code = 1;
      }
    )
  }
 );
nr_measurement_configuration = {
  Periodical = {
    enable = 1;
    includeBeamMeasurements = 1;
    maxNrofRS_IndexesToReport = 4;
  };
  A2 = {
    enable = 1;
    threshold = 60;
    timeToTrigger = 1;
  };
  A3 = ({
    cell_id = -1; #Default
    offset = 10;
    hysteresis = 0;
    timeToTrigger = 1
  })
};
```
The above configuration further enables periodic measurements, A2 event ("Serving becomes worse than threshold"), and A3 events ("Neighbour Becomes Better than Serving by an offset"). The A2 event can be disabled by setting `enable = 0`. A3 events cannot be disabled as of now. Further, the A3 events can be made specific to cells; `cell_id = -1` means "any cell".

`@include` this configuration file inside the gNB section of CUCP file as shown below.
```
    plmn_list = ({ mcc = 001; mnc = 01; mnc_length = 2; snssaiList = ({ sst = 1, sd = 0x000000 })});
    @include "neighbour-config.conf"
```
## Xn Handover Configuration Files
Please find Xn handover configuration files here [../conf/xn\_conf\_files](../conf/xn_conf_files)

## Bringing up the setup

### Steps to run Xn Handover with COTS UE.
1. Bring up the 5G core network.
2. Run the gNBs having XNAP enabled and neighbour section included in the CUCP configuration.
3. You can refer [here](./README.md#user-guide).
4. Connect UE to any of the gNBs.
5. As you move UE towards the neighbouring gNB, A3 Events get triggered, and then the source gNB  will handover the UE to the target gNB.

### Steps to run Xn Handover with [NR UE in RFsim mode](./README.md#run-ue-in-rfsim-mode).
1. Bring up the 5G core network.
2. Make sure you build the gNB with telnet [as shown here](#build-with-telnet-support).
   And gNBs having XNAP enabled and neighbour section included in the CUCP configuration.
3. Bring up gNBs using commands from [section](./README.md#user-guide). Just append `--telnetsrv --telnetsrv.shrmod ci` to CUCP command.
```bash
sudo ./nr-softmodem -O <cucp_conf_having_XNAP_and_neighbour_configuration_included> --sa --telnetsrv --telnetsrv.shrmod ci
```
4. To trigger HO from source gNB to target gNB, use the following commands.
```bash
cd ios-mcn-ran/openairinterface5g/
echo ci trigger_xn_ho [cu-ue-id] | nc 127.0.0.1 9090 && echo
```

> **Note**
> You can use the telnet command with COTS UE as well. For that, follow the below steps.
> Make sure you build the gNB with telnet [as shown here](#build-with-telnet-support). 
> Append `--telnetsrv --telnetsrv.shrmod ci` to CUCP command while bringing up the gNBs.
> Use telnet command as shown above to trigger handover.

### Performing Xn-Handover with Lekha RU
This example demonstrates how to perform Xn-Handover using Lekha RU with two independent gNBs.

1. Run the 5G Core Network if not already running.
2. Start the source gNB.
```bash
cd ios-mcn-ran
```
1. Start the CUCP including telnet support.
```bash
sudo ./nr-softmodem --sa -O ./conf/xn_conf_files/gnb-cucp.sa.f1-e1-xn-source.conf --telnetsrv --telnetsrv.shrmod ci
```
2. Start the CUUP.
```bash
sudo ./nr-cuup --sa -O ./conf/xn_conf_files/gnb-cuup.sa.f1-e1-xn-source.conf
```
3. Start the DU.
```bash
sudo ./nr-softmodem --sa -O ./conf/xn_conf_files/gnb-du.sa.band78.106PRB.1x1.lekha.f1-e1-xn-source.conf --thread-pool 11,12,13,14
```
3. Start the target gNB.
```bash
cd ios-mcn-ran
```
1. Start the CUCP including telnet support.
```bash
sudo ./nr-softmodem --sa -O ./conf/xn_conf_files/gnb-cucp.sa.f1-e1-xn-target.conf --telnetsrv --telnetsrv.shrmod ci
```
2. Start the CUUP.
```bash
sudo ./nr-cuup --sa -O ./conf/xn_conf_files/gnb-cuup.sa.f1-e1-xn-target.conf
```
3. Start the DU.
```bash
sudo ./nr-softmodem --sa -O ./conf/xn_conf_files/gnb-du.sa.band78.106PRB.1x1.lekha.f1-e1-xn-target.conf --thread-pool 11,12,13,14
```
4. Connect the UE to any of the gNBs.
5. Trigger Handover.
  - Option (i): Automatic Handover <br>
  	Move the UE towards the neighbouring gNB. The A3 event will be automatically triggered, and the source gNB  will hand over the UE to the target gNB.  
  - Option (ii): Manual Handover via Telnet <br>
  	If you want to manually trigger the Xn handover, use the following command:
```bash
cd ios-mcn-ran/openairinterface5g
echo ci trigger_xn_ho [cu-ue-id] | nc 127.0.0.1 9090 && echo
```
>Replace [cu-ue-id] with the actual CU UE ID of the connected UE.
