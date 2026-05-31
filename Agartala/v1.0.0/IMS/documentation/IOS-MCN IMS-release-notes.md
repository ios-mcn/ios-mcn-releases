## IOS MCN IMS v1.0.0 Release
Welcome to the v1.0.0 Release of IOS MCN IMS CSCF

# Version Summary
Version Number : v1.0.0 <br>
Version Name: CSCF Agartala v1.0.0 <br>
Date: 27-05-2026

Projects / Repos Included in this release:

| Project | version | Release image Link |
|--|--|--|
| CSCF | v1.0.0 | Link |

## Release Summary :

**CSCF Agartala v1.0.0** introduces the initial integrated IMS core release including P-CSCF, I-CSCF, S-CSCF, N5 Interface, and RESTCONF Server. This release focuses on SIP signaling, IMS registration and AKA authentication, secure IPsec handling, HTTP/2-based SBI communication, and centralized configuration management across CSCF components. The release establishes foundational IMS capabilities with improved session handling, inter-module communication, and policy control integration required for IMS deployments.

## Highlights (P-CSCF)

- Added SIP signaling support over UDP and TCP.
- Added IPSec UDP/TCP listener support for secure IMS communication.
- Added SIP request forwarding toward I-CSCF and S-CSCF.
- Added session handling and IMS registration processing.
- Introduced security context management and authentication handling.
- Added configurable media server and IPsec support.
- Improved multi-threaded SIP processing performance.

## Highlights (I-CSCF)

- Added SIP routing and forwarding support.
- Added configurable routing between P-CSCF and S-CSCF.
- Added support for IMS registration flow handling.
- Added UDR integration capability.

## Highlights (S-CSCF)

- Added IMS AKA authentication support.
- Added MILENAGE authentication vector generation.
- Added RAND, AUTN, CK, IK and RES generation procedures.
- Added authentication challenge handling for IMS registration.
- Improved registration processing reliability.

## Highlights (N5 Interface)

- Added N5 to PCF communication support.
- Added HTTP/2 and SBI interface support.
- Added SCP/NRF integration capability.
- Added dynamic instance handling and configuration loading.

## Highlights (RESTCONF Server)

- Added RESTCONF API support for configuration management.
- Added token-based authentication.
- Added YANG model loading support.
- Added datastore synchronization and configuration persistence.

## Changelog v1.0.0

- Added integrated P-CSCF, I-CSCF and S-CSCF modules.
- Added IMS AKA authentication using MILENAGE.
- Added SIP signaling support over UDP/TCP.
- Added IPSec handling support.
- Added N5 Interface for policy control communication.
- Added HTTP/2 SBI communication support.
- Added RESTCONF server for centralized configuration management.
- Added multi-threaded processing for improved SIP handling.
- Added security context and registration handling mechanisms.
- Added configurable IMS routing between CSCF entities.

## Supported Functionalities

✓ IMS Registration  
✓ SIP Signaling  
✓ AKA Authentication  
✓ HTTP/2 Communication  
✓ N5 Policy Interface  
✓ RESTCONF Management  
✓ IPSec Support  
✓ Session Handling  

#### Test Reports:
[Find the test report here](https://github.com/ios-mcn-ims/qa/tree/main/01.releases/v1.0.0/test%20report)

## How to use the Release:
### Environment Requirements and Pre-requisites:

- Docker engine is an environmental pre-requisite for a successful dockerized deployment.

### Build

#### From the root folder run-

`./build.sh`

Enter the following details as prompted:

```
Enter parent interface name (example: enp0s3)
Enter network subnet (example: 192.168.1.0/24)
Enter gateway (example: 192.168.1.1)
Enter macvlan network name (example: mcn-net)
Enter container IP for CSCF & N5 (example: 192.168.1.2)
Enter P-CSCF Bind Port (example: 5060)
I-CSCF Port (example: 4060)
S-CSCF Port (example: 6060)
Enter N5 Bind Port (example: 7777)
Enter N5 SBI Bind Port (example: 7782)
Enter container name (example: ims-cscf)
Enter SCP/NRF IP address (example: 127.0.0.200)
Enter SCP/NRF port (example: 7777)
Enter PCF IP address (example: 127.0.0.13)
Enter PCF port (example: 7777)
Enter UDM Server IP address (example: 127.0.0.1)
Enter UDM Server port (example: 7777)
Enter UDR Server IP address (example: 127.0.0.1)
Enter UDR Server port (example: 7777)
Is IOS-MCN-CORE used (TRUE/FALSE)
Is Media Server enabled (TRUE/FALSE)
Media Server Host (if enabled) (example: 127.0.0.1)
Media Server Port (if enabled) (example: 2223)
Media Server Control Protocol (if enabled, example: ng)
Is IPsec enabled (TRUE/FALSE)
```

### OR

Run the following (sample) command to build and deploy using command line arguments-

```
./build.sh --iface eth0 --subnet 192.168.8.0/24 --gateway 192.168.8.254 --netname mcn-net --container-ip 192.168.8.112 --pcscf-port 5060 --icscf-port 4060 --scscf-port 6060 --n5-port 7777 --n5-sbi-port 7782 --container-name ims --scp-ip 192.168.8.66 --scp-port 7777 --pcf-ip 192.168.8.69 --pcf-port 7777 --udm-ip 192.168.8.68 --udm-port 7777 --udr-ip 192.168.8.67 --udr-port 7777 --ios-mcn-core FALSE --media-server-enabled FALSE --media-server-host 127.0.0.1 --media-server-port 2223 --media-server-control-protocol ng --ipsec-enabled FALSE
```

### Gain shell access
`sudo docker exec -it cscf-app /bin/bash`

## License
| Library | License |
| ------ | ------- |
| Spring Framework | Apache License 2.0 |
| Spring Boot | Apache License 2.0 |
| Spring Boot Devtools | Apache License 2.0 |
| Apache Log4j | Apache License 2.0 |
| Lombok | MIT License |

## Issues and Suggestions
For all issues/suggestions related to specific projects, please raise here - [Link](https://github.com/ios-mcn-ims/ios-mcn-ims/issues)
