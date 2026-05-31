# Developer Guide – IOS-MCN-IMS v1.0.0

This guide explains how to configure, build, and deploy the IOS-MCN-IMS platform.

IOS-MCN-IMS provides an integrated IMS framework consisting of:

- P-CSCF (Proxy Call Session Control Function)
- I-CSCF (Interrogating Call Session Control Function)
- S-CSCF (Serving Call Session Control Function)
- N5 Interface
- RESTCONF Server

The platform supports both **Container-Based Deployment** and **Bare Metal Deployment**.

---

# Development Environment

## Supported Operating Systems

- Ubuntu 22.04 LTS
- Debian 12

## Required Software

### Container Deployment

- Docker
- Git

### Bare Metal Deployment

- OpenJDK 17+
- Maven 3.8+
- Go 1.23+
- PostgreSQL
- Git

---

# Source Code Structure

```text
cscf/
├── build.sh
├── Dockerfile
├── pcscf/
├── icscf/
├── scscf/
├── n5/
└── rest-conf-server/
```

---

# Containerized Build

## Runtime Configuration

The deployment script automatically generates configuration files for all IMS components.

Generated configuration files include:

```text
generated-configs/
├── pcscf
├── icscf
├── scscf
├── iosmcn-ims-n5
├── pcscf-logging.xml
├── icscf-logging.xml
├── scscf-logging.xml
└── n5-logging.xml
```

---

## Core Runtime Parameters

### PCSCF Configuration

| Parameter | Description |
|------------|-------------|
| PCSCF-LISTEN-IP | P-CSCF Bind IP |
| PCSCF-LISTEN-PORT | P-CSCF SIP Port |
| ICSCF-LISTEN-IP | I-CSCF Bind IP |
| ICSCF-LISTEN-PORT | I-CSCF SIP Port |
| SCSCF-LISTEN-IP | S-CSCF Bind IP |
| SCSCF-LISTEN-PORT | S-CSCF SIP Port |
| N5-LISTEN-SBI-IP | N5 SBI Bind IP |
| N5-LISTEN-SBI-PORT | N5 SBI Bind Port |
| TIMEOUT-MS | SIP Transaction Timeout |
| PLMN-ID | PLMN Identifier |
| IOSMCNCORE | Enable IOS-MCN Core Integration |
| MEDIA-SERVER-ENABLED | Enable Media Server Integration |
| MEDIA-SERVER-HOST | Media Server Address |
| MEDIA-SERVER-PORT | Media Server Control Port |
| MEDIA-SERVER-CONTROL-PROTOCOL | Media Server Control Protocol |
| IPSEC-ENABLED | Enable IMS IPsec Security |


## I-CSCF Configuration

| Parameter | Description |
|------------|-------------|
| ICSCF-LISTEN-IP | I-CSCF Bind IP Address |
| ICSCF-LISTEN-PORT | I-CSCF SIP Listening Port |
| SCSCF-LISTEN-IP | S-CSCF IP Address |
| SCSCF-LISTEN-PORT | S-CSCF SIP Port |
| PCSCF-LISTEN-IP | P-CSCF IP Address |
| PCSCF-LISTEN-PORT | P-CSCF SIP Port |
| UDR-SERVER-IP | UDR Server IP Address |
| UDR-SERVER-PORT | UDR Server Port |
| PLMN-ID | PLMN Identifier |
| TIMEOUT-MS | SIP Transaction Timeout |
| IOSMCNCORE | Enable IOS-MCN Core Integration |

---

## S-CSCF Configuration

| Parameter | Description |
|------------|-------------|
| SCSCF-LISTEN-IP | S-CSCF Bind IP Address |
| SCSCF-LISTEN-PORT | S-CSCF SIP Listening Port |
| PCSCF-LISTEN-IP | P-CSCF IP Address |
| PCSCF-LISTEN-PORT | P-CSCF SIP Port |
| ICSCF-LISTEN-IP | I-CSCF IP Address |
| ICSCF-LISTEN-PORT | I-CSCF SIP Port |
| UDR-SERVER-IP | UDR Server IP Address |
| UDR-SERVER-PORT | UDR Server Port |
| TIMEOUT-MS | SIP Transaction Timeout |
| PLMN-ID | PLMN Identifier |
| IOSMCNCORE | Enable IOS-MCN Core Integration |

---

### N5 Configuration

| Parameter | Description |
|------------|-------------|
| SCP-IP | SCP / NRF SBI Address |
| SCP-PORT | SCP / NRF SBI Port |
| PCF-IP | PCF SBI Address |
| PCF-PORT | PCF SBI Port |
| AF-BIND-IP | N5 Interface Address |
| AF-BIND-PORT | N5 Service Port |
| AF-BIND-SBI-IP | N5 SBI Address |
| AF-BIND-SBI-PORT | N5 SBI Port |

---

## Build and Deploy

Build and deploy the complete IMS platform:

```bash
chmod +x build.sh
./build.sh
```

The deployment script will:

- Create the required Docker macvlan network.
- Generate runtime configuration files.
- Build the IMS image.
- Configure IMS components.
- Configure N5 connectivity.
- Configure UDR connectivity.
- Configure optional Media Server integration.
- Configure optional IPsec support.
- Deploy the IMS container.

---

## Build Using Command Line Arguments

Example:

```bash
./build.sh \
--iface eth0 \
--subnet 192.168.8.0/24 \
--gateway 192.168.8.254 \
--netname mcn-net \
--container-ip 192.168.8.112 \
--pcscf-port 5060 \
--icscf-port 4060 \
--scscf-port 6060 \
--n5-port 7777 \
--n5-sbi-port 7782 \
--container-name ims \
--scp-ip 192.168.8.66 \
--scp-port 7777 \
--pcf-ip 192.168.8.69 \
--pcf-port 7777 \
--udm-ip 192.168.8.68 \
--udm-port 7777 \
--udr-ip 192.168.8.67 \
--udr-port 7777 \
--ios-mcn-core TRUE \
--media-server-enabled FALSE \
--media-server-host 127.0.0.1 \
--media-server-port 2223 \
--media-server-control-protocol ng \
--ipsec-enabled TRUE
```

---

# Bare Metal Build

## Install Dependencies

```bash
sudo apt update

sudo apt install -y \
    openjdk-17-jdk \
    maven \
    golang \
    postgresql \
    net-tools \
    iproute2 \
    curl \
    vim \
    sngrep
```

Verify installation:

```bash
java -version
mvn -version
go version
psql --version
```

---

## PostgreSQL Configuration

Enable PostgreSQL:

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### Configure Local Trust Authentication

Determine the PostgreSQL version:

```bash
pg_lsclusters
```

Edit the PostgreSQL authentication file:

```bash
sudo vi /etc/postgresql/<version>/main/pg_hba.conf
```

Add or update the following entries:

```text
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

### Create Databases

```bash
sudo -u postgres psql -c "CREATE DATABASE pcscf;"
sudo -u postgres psql -c "CREATE DATABASE icscf;"
sudo -u postgres psql -c "CREATE DATABASE scscf;"
```

Verify databases:

```bash
sudo -u postgres psql -l
```

Expected databases:

- pcscf
- icscf
- scscf

---

## Build N5

```bash
cd n5
mvn clean package -DskipTests
```

---

## Build P-CSCF

```bash
cd pcscf
mvn clean package -DskipTests
```

---

## Build I-CSCF

```bash
cd icscf
mvn clean package -DskipTests
```

---

## Build S-CSCF

```bash
cd scscf
mvn clean package -DskipTests
```

---

## Build RESTCONF Server

```bash
cd rest-conf-server

go mod download

go build -o restconf-server ./cmd/server
```

---

# Runtime Architecture

The IOS-MCN-IMS platform consists of:

| Component | Function |
|------------|-----------|
| P-CSCF | IMS Access Proxy |
| I-CSCF | IMS Routing and Subscriber Discovery |
| S-CSCF | Registration and Session Control |
| N5 | Policy Control Interface |
| RESTCONF | Configuration Management |
| PostgreSQL | Subscriber Sessions and Runtime Data Storage |

---

# Logging

Each component uses an independent logging configuration.

| Component | Logging Configuration |
|------------|----------------------|
| P-CSCF | pcscf-logging.xml |
| I-CSCF | icscf-logging.xml |
| S-CSCF | scscf-logging.xml |
| N5 | n5-logging.xml |

---

# RESTCONF Server

The RESTCONF Server is implemented in Go and provides:

- RFC8040 RESTCONF APIs
- YANG-Based Configuration Management
- Runtime Configuration Operations
- REST API Access to IMS Configuration

Build:

```bash
cd rest-conf-server

go build -o restconf-server ./cmd/server
```

Run:

```bash
./restconf-server
```

For detailed RESTCONF deployment and API usage, refer to the `README.md` file available in the RESTCONF source code directory.

---

# Troubleshooting

### Verify PostgreSQL

```bash
sudo systemctl status postgresql
```

### Verify Listening Ports

```bash
sudo ss -tulpn
```

### View Docker Logs

```bash
docker logs -f <container-name>
```

### Verify RESTCONF Health

```bash
curl http://<server-ip>:8088/healthz
```

Expected output:

```text
OK
```