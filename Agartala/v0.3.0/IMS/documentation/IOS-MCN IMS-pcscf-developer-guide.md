
# Developer Guide – IOS-MCN-IMS v0.3.0

This guide explains how to configure, build, and run the P-CSCF (Proxy–Call Session Control Function) module. It supports both **Dockerized** and **Bare Metal** deployments.

---
## Docker Installation on Ubuntu
Docker on Ubuntu can be installed by following the steps in this [link](https://docs.docker.com/engine/install/ubuntu/)

## Dockerized Build

### Parameters

- Default runtime parameters: `defaults/pcscf`

### Interface Configuration

- Listen IP: `PCSCF-LISTEN-IP=192.168.0.1`
- Listen Port: `PCSCF-LISTEN-PORT=5060`
- N5 SBI Listen IP: `N5-SBI-LISTEN-IP=127.0.0.1`
- N5 SBI Listen Port: `N5-SBI-LISTEN-PORT=8080`
- UDM Server IP: `UDM-SERVER-IP=127.0.0.1`
- UDM Server Port: UDM-SERVER-PORT=7777
- `TIMEOUT-MS=10000`
- `PLMN-ID=00101`
- `IOSMCNCORE=TRUE`

### Subscriber Information

Subscriber details are configured in: `cscf/pcscf/subscribers.json`. Users need to edit this as per their requirement.

This file contains key-value pairs mapping `IMSI` to `MSISDN`.

Example format:

```json
{
  "001010000000001": "9100000001",
  "001010000000002": "9100000002",
  "001010000000003": "9100000003"
}
```

---


### Step 1: Configuration

- Ensure the following IP/Port variables are defined inside the `Dockerfile`:

```Dockerfile
PCSCF-LISTEN-IP=192.168.0.1
PCSCF-LISTEN-PORT=5060
N5-SBI-LISTEN-IP=127.0.0.1
N5-SBI-LISTEN-PORT=8080
UDM-SERVER-IP=127.0.0.1
UDM-SERVER-PORT=7777
TIMEOUT-MS=10000
PLMN-ID=00101
IOSMCNCORE=TRUE
```

- The Dockerfile will automatically pick up the `subscribers.json` file without any extra steps.

### Step 2: Build

Navigate to the `pcscf` folder and run:

```bash
sudo docker build -t pcscf .
```


## Bare Metal Build

### Required Files

The following configuration files must be created and placed manually:

- `/etc/ios-mcn/pcscf-logging.xml`
- `/etc/ios-mcn/pcscf`
- `/etc/ios-mcn/subscribers.json`
- `/lib/systemd/system/ios-mcn-pcscf.service`

> Reference contents for these files can be found [here](https://docs.google.com/document/d/1Ek-rYGfBonGcgr0kIi2XRSh-aNQc_R847LkSfficHEs/edit?tab=t.0)

### Step 1: Prepare Configuration Directory

```bash
sudo mkdir -p /etc/ios-mcn
```

Create the following files under `/etc/ios-mcn` with appropriate content:

- `pcscf-logging.xml` – Logging configuration
- `pcscf` – Runtime configuration (including IP and Port)
- `subscribers.json` – Subscriber IMSI:MSISDN mappings

### Step 2: Build the Application

1. In the source directory, rename:

```bash
mv cscf/pcscf/defaults cscf/pcscf/config
```

> This is necessary because the `defaults` folder is exclusively used for Docker builds.

2. Navigate to the `pcscf` source directory:

```bash
cd cscf/pcscf
mvn clean package
```

3. After a successful build, the output `.jar` file will be located at:

```
cscf/pcscf/target/pcscf-0.0.1.jar
```

This JAR can be used to run the service or linked with a systemd unit file for persistent service management.