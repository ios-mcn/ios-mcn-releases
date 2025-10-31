## IOS MCN IMS P-CSCF v0.3.0 Release
Welcome to the v0.3.0 Release of IOS MCN IMS P-CSCF

# Version Summary
Version Number : v0.3.0 <br>
Version Name:  v0.3.0 <br>
Date: 26-06-2025

Projects / Repos Included in this release:
| Project | version| Release image Link |
|--|--|--|
 |[P-CSCF](https://github.com/ios-mcn-ims/cscf)|v0.3.0| [Link](https://github.com/ios-mcn-ims/cscf/releases/tag/v0.3.0.iosmcn.ims.cscf)|


## Release Summary :
**P-CSCF agartala v0.3.0** is released with features supporting SIP message handling, custom SIP stack implementation, session management and cleanup.

## Highlights:
- SIP Message Handling-
   - Supports core SIP methods:
      - REGISTER
      - INVITE
      - ACK
      - BYE
   - Handles essential SIP provisional and informational responses:
      - 100 Trying
      - 180 Ringing
      - 183 Session Progress
   - Supports PRACK method for reliable provisional responses.
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

## Changelog v0.3.0
- Support for an extensive catalog of SIP Messages
- UDM Interfacing for implicit subscriber info
- HTTP/1.1 fallback support

#### Test Reports:
[Find the test report here](https://github.com/ios-mcn-ims/qa/tree/main/01.releases/v0.1.2/test%20report)

## How to use the Release (Dockerized):
### Environment Requirements and Pre-requisites:

- Docker engine is an environmental pre-requisite for a successful dockerized deployment.

### Build (Dockerized Deployment)

- The configurations need to be done **directly in the Dockerfile** present in the source folder. The application picks up the IP and PORT mapping from the Dockerfile.

### From the pcscf folder run-

`sudo docker build -t pcscf .`

### Run

`sudo docker run -d --name pcscf-container -p 5060:5060 pcscf`

### Gain shell access
`sudo docker exec -it pcscf-container /bin/bash`

## How to use the Release (Bare Metal):

### Contents of the files- 
- `/etc/ios-mcn/pcscf-logging.xml`
- `/lib/systemd/system/ios-mcn-pcscf.service`
- `/etc/ios-mcn/pcscf`
- `/etc/ios-mcn/subscribers.json`
### can be located [here](https://docs.google.com/document/d/1Ek-rYGfBonGcgr0kIi2XRSh-aNQc_R847LkSfficHEs/edit?tab=t.0)

### Necessary Configurations Before Building:
- In directory `/etc/ios-mcn` make a file named `pcscf-logging.xml`
- In directory `/etc/ios-mcn` make a file named `pcscf`, and input the `IP` and `PORT` according to your own system
- In directory `/etc/ios-mcn` make a file named `subscribers.json`, and make key value pairs of subscriber info (IMSI:MSISDN) as per your requirement.

### Build Process:
- In the source code directory, rename the `cscf/pcscf/defaults` directory to `cscf/pcscf/config`. This step is crucial since `defaults` directory is exclusively used for dockerized build.
- Navigate to the source code directory, under directory `cscsf/pcscf`, run command- `mvn clean package`
- This command will generate a new directory named `target`, under which the `pcscf-0.0.1.jar` file can be located

### Deployment Process:
- From the directory `cscf/pcscf/target`, rename the file named `pcscf-0.0.1.jar` to `pcscf.jar` and place the `pcscf.jar` file in directory `/etc/ios-mcn`
- In directory `/lib/systemd/system` make a file named `ios-mcn-pcscf.service`
- Run `sudo systemctl daemon-reload`
- Run `sudo systemctl enable ios-mcn-pcscf.service`
- Run `sudo systemctl start ios-mcn-pcscf.service`
- Run `sudo systemctl status ios-mcn-pcscf.service` to check the status of the service
- After all the configurations, service setup, and running build commands, if the systemctl status command shows **"Active: active (running)"**, deployment was successful.

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