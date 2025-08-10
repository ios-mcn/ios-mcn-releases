# 5G NR

## SA setup with OAI NR-UE

The standalone mode is the default mode.

The default (SA) mode does the following:
- At the gNB:
* The RRC encodes SIB1 according to the configuration file and transmits it through NR-BCCH-DL-SCH.

- At the UE:
* Decode SIB1 and starts the 5G NR Initial Access Procedure for SA:
  1) 5G-NR RRC Connection Setup
  2) NAS Authentication and Security
  3) 5G-NR AS Security Procedure
  4) 5G-NR RRC Reconfiguration
  5) Start Downlink and Uplink Data Transfer

Command line parameters for UE in standalone mode:
- `-C` : downlink carrier frequency in Hz (default value 0)
- `--CO` : uplink frequency offset for FDD in Hz (default value 0)
- `--numerology` : numerology index (default value 1)
- `-r` : bandwidth in terms of RBs (default value 106)
- `--band` : NR band number (default value 78)
- `--ssb` : SSB start subcarrier (default value 516)

To simplify the configuration for the user testing OAI UE with OAI gNB, the latter prints the following LOG that guides the user to correctly set some of the UE command line parameters:

```shell
[PHY]   Command line parameters for OAI UE: -C 3319680000 -r 106 --numerology 1 --ssb 516
```

You can run this, using USRPs, on two separate machines:

```shell
sudo nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --ssb 516
```

With the **RFsimulator** (on the same machine), just add the option `--rfsim` to both gNB and NR UE command lines.

## Optional NR-UE command line options

Here are some useful command line options for the NR UE:

| Parameter                | Description                                                                                                   |
|--------------------------|---------------------------------------------------------------------------------------------------------------|
| `--ue-scan-carrier`      | Scan for cells in current bandwidth. This option can be used if the SSB position of the gNB is unknown. If multiple cells are detected, the UE will try to connect to the first cell. By default, this option is disabled and the UE attempts to only decode SSB given by `--ssb`. |
| `--ue-fo-compensation`   | Enables the frequency offset compensation at the UE. Useful when running over the air and/or without an external clock/time source. |
| `--usrp-args`            | Equivalent to the `sdr_addrs` field in the gNB config file. Used to identify the USRP and set some basic parameters (like the clock source).  |
| `--clock-source`         | Sets the clock source (internal or external).                                                                 |
| `--time-source`          | Sets the time source (internal or external).                                                                  |

You can view all available options by typing:

```shell
./nr-uesoftmodem --help
```
## Common gNB and NR UE command line options

### Three-quarter sampling

The command line option `-E` can be used to enable three-quarter sampling for split 8 sample rate. Required for certain radios (e.g., 40MHz with B210). If used on the gNB, it is a good idea to use for the UE as well (and vice versa).