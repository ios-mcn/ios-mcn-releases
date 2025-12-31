## IOS MCN IMS v0.4.0 Release
Welcome to the v0.4.0 Release of IOS MCN IMS P-CSCF

# Version Summary
Version Number : v0.4.0 <br>
Version Name:  v0.4.0 <br>
Date: 30-12-2025

Projects / Repos Included in this release:
| Project | version| Release image Link |
|--|--|--|
 |[P-CSCF](https://github.com/ios-mcn-ims/cscf)|v0.4.0| [Link](https://github.com/ios-mcn-ims/ios-mcn-ims/releases/tag/v0.4.0.iosmcn.ims)|


## Release Summary :
**P-CSCF agartala v0.4.0** is released with features supporting SIP message handling, custom SIP stack implementation, session management and cleanup.

## Highlights (CSCF):
- SIP Message Handling-
   - `REGISTER` – Handles UE registration requests within IMS.
   - `INVITE` – Initiates session establishment for calls or media sessions.
   - `ACK` – Confirms successful call setup.
   - `BYE` – Terminates ongoing sessions cleanly.
   - `CANCEL` – Cancels a pending INVITE request before the call is established.
   - `PRACK` – Acknowledges reliable provisional responses.
   - `INFO` – Exchanges mid-session signaling information, such as DTMF tones.
   - `SUBSCRIBE` – Requests event notifications (e.g., presence or message waiting).

   Supported SIP provisional and informational responses include:

   - **1xx (Provisional Responses)**
   - `100 Trying` – Indicates that the request has been received and processing has started.
   - `180 Ringing` – Alerts that the destination user agent is being alerted.
   - `183 Session Progress` – Provides information about early media.

   - **2xx (Successful Responses)**
   - `200 OK` – Confirms successful request processing.
   - `202 Accepted` – Indicates that the request has been accepted for processing, but completion is pending.

   - **4xx (Client Failure Responses)**
   - `400 Bad Request` – Invalid syntax or malformed request.
   - `401 Unauthorized` – Authentication is required.
   - `404 Not Found` – The user or service does not exist.
   - `486 Busy Here` – The user is busy.

- Lightweight Design
   - Custom SIP stack implementation (does not depend on third party SIP
libraries).
   - Uses direct socket-based SIP message processing on port 5060.
- Session Management and Cleanup
   - Handles call flow management (session initiation, update, termination).
   - VoNR
   - ViNR
   - Maintains session state information during active calls.
   - Performs proper session cleanup after call completion or timeout to avoid
resource leaks.
- UDM Interfacing
   - Directly interfaces with UDM (Configured at build-time) to fetch subscriber info.
   - Eliminates the use of `subscribers.json` file which used explicit declaration of subscriber info.
- HTTP/1.1 fallback support for smoother NFRegister and Heartbeat timer implementation.
- Support for prometheus actuator for service uptime.
- Support for multiple UE models apart from Samsung UEs
- Support for RESTCONF server for API-based configuration management.
- Added **UDP Handler**: This enables support for multiple UE models apart from Samsung. **Currently tested OnePlus Nord CE 5G UEs for VoNR calls.**
- Added **IPSec support** with **ESP Implementation**.


## Highlights (N5):
- NF Register:
   - Heartbeat timer to maintain register status
- Audio PDU Session Creation
- Video PDU Session Creation
- PDU Session Deletion
- SBI Interfacing for P-CSCF interoperability
- Support for RESTCONF server for API-based configuration management.

## Changelog v0.4.0
- Introduced support for PATCH-based video updates during Re-INVITE handling, enabling dynamic media modifications without full session renegotiation.
- Enhanced Re-INVITE processing to correctly apply and enforce updated QoS parameters, ensuring consistent bearer behavior during mid-call changes.
- Improved AUTS re-synchronization handling and aligned IPsec policy updates to ensure secure recovery from authentication desynchronization.
- Implemented cleanup of stale IPsec policies and Security Associations to prevent policy conflicts during reconnects and deregistration scenarios.
- Resolved an issue where prolonged UE idle state caused call setup failures due to expired or inconsistent session state.
- Refined transactional socket management to improve request/response consistency, reliability, and error isolation under concurrent signaling.
- Corrected session timer expiry handling to ensure accurate refresh and termination behavior in compliance with IMS session lifecycle rules.

#### Test Reports:
[Find the test report here](https://github.com/ios-mcn-ims/qa/tree/main/01.releases/v0.4.0/test%20report)

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
Enter container IP Will be Used For CSCF Functions and N5 Interface (example: 192.168.1.2)
Enter P-CSCF Bind Port (example: 5060)
Enter N5 Bind Port (example: 7777)
Enter N5 SBI BIND Port (example: 7782)
Enter container name (example: ims-cscf)
Enter SCP/NRF IP address (example: 127.0.0.200)
Enter SCP/NRF port (example: 7777)
Enter PCF IP address (example: 127.0.0.13)
Enter PCF port (example: 7777)
Enter UDM Server IP address (example: 127.0.0.1)
Enter UDM Server port (example: 7777)
Enter UDR Server IP address (example: 127.0.0.1)
Enter UDR Server port (example: 7777)
Please Enter TRUE is IOS-MCN-CORE is used, else FALSE
```

### OR

Run the following (sample) command to build and deploy using command line arguments-

```
./build.sh --iface eth0   --subnet 192.168.8.0/24   --gateway 192.168.8.254   --netname mcn-net   --container-ip 192.168.8.112   --pcscf-port 5060   --n5-port 7777   --n5-sbi-port 7782   --container-name ims-cscf   --scp-ip 127.0.0.200   --scp-port 7777   --pcf-ip 127.0.0.13   --pcf-port 7777   --udm-ip 127.0.0.1   --udm-port 7777   --udr-ip 127.0.0.1   --udr-port 7777   --ios-mcn-core TRUE
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