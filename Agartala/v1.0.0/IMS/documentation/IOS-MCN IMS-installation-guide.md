# Installation Guide – IOS-MCN-IMS v1.0.0

This guide explains how to install and deploy the IOS-MCN-IMS platform.

The platform includes:

- P-CSCF
- I-CSCF
- S-CSCF
- N5 Interface
- RESTCONF Server

---

# Container-Based Deployment

## Prerequisites

Ensure the following software is installed:

- Docker
- Docker Compose (Optional)
- Git

---

## Clone Source Code

```bash
git clone <repository-url>
cd cscf
```

---

## Build Images

Build all IMS components using the provided build script:

```bash
./build.sh
```

The script will prompt for the following deployment parameters:

```text
Enter parent interface name (example: enp0s3)
Enter network subnet (example: 192.168.1.0/24)
Enter gateway (example: 192.168.1.1)
Enter macvlan network name (example: mcn-net)
Enter container IP for CSCF & N5 (example: 192.168.1.2)

Enter P-CSCF Bind Port (example: 5060)
Enter I-CSCF Port (example: 4060)
Enter S-CSCF Port (example: 6060)

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
Media Server Host (if enabled)
Media Server Port (if enabled)
Media Server Control Protocol (if enabled)

Is IPsec enabled (TRUE/FALSE)
```

---

## Non-Interactive Deployment

Alternatively, deployment can be performed using command-line arguments:

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

## What the Build Script Deploys

The build script automatically:

- Creates the required Docker network (macvlan).
- Builds all IOS-MCN-IMS components.
- Generates runtime configuration files.
- Deploys:
  - P-CSCF
  - I-CSCF
  - S-CSCF
  - N5 Interface
  - RESTCONF Server
- Configures connectivity towards:
  - SCP / NRF
  - PCF
  - UDR
- Configures optional:
  - Media Server Integration
  - IPsec Support

---

## What the Build Script Does

The `build.sh` script automates the complete deployment process and performs the following actions:

- Creates the required macvlan Docker network.
- Generates runtime configuration files.
- Builds the IOS-MCN-IMS container image.
- Deploys the IMS container.
- Configures:
  - P-CSCF
  - I-CSCF
  - S-CSCF
  - N5 Interface
  - RESTCONF Server
- Configures connectivity towards:
  - SCP / NRF
  - PCF
  - UDM
  - UDR
- Configures optional:
  - Media Server Integration
  - IPsec Support

---

## Verify Deployment

Verify the container is running:

```bash
docker ps
```

Expected output should contain the configured container name.

Example:

```bash
docker ps | grep ims
```

---

## View Container Logs

```bash
docker logs -f <container-name>
```

Example:

```bash
docker logs -f ims
```

---

## Access Container Shell

```bash
docker exec -it <container-name> /bin/bash
```

Example:

```bash
docker exec -it ims /bin/bash
```

---

## Stop Container

```bash
docker stop <container-name>
```

Example:

```bash
docker stop ims
```

---

## Start Container

```bash
docker start <container-name>
```

Example:

```bash
docker start ims
```

---

## Remove Deployment

```bash
docker stop <container-name>
docker rm <container-name>
```

Example:

```bash
docker stop ims
docker rm ims
```

---

## Rebuild Deployment

If configuration or source code changes are made, rebuild the deployment using:

```bash
./build.sh
```

or

```bash
./build.sh <deployment-parameters>
```

The script will rebuild the image and redeploy the IMS container with the updated configuration.

---

# Bare Metal Deployment

## Prerequisites

Install required packages:

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
### Configure Local Trust Authentication

Determine the PostgreSQL version:

```bash
pg_lsclusters
```

Edit the `pg_hba.conf` file:

```bash
sudo vi /etc/postgresql/<version>/main/pg_hba.conf
```

Update the file to allow local connections from `127.0.0.1` without password authentication:

```text
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
```

Apply the configuration:

```bash
sudo systemctl restart postgresql
```

Enable PostgreSQL:

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Create required databases:

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

## Build Components

### Build N5

```bash
cd n5
mvn clean package -DskipTests
```

### Build P-CSCF

```bash
cd pcscf
mvn clean package -DskipTests
```

### Build I-CSCF

```bash
cd icscf
mvn clean package -DskipTests
```

### Build S-CSCF

```bash
cd scscf
mvn clean package -DskipTests
```

### Build RESTCONF Server

```bash
cd rest-conf-server

go mod download

go build -o /usr/local/bin/restconf-server ./cmd/server
```

---

## Create Deployment Directory

```bash
sudo mkdir -p /etc/ios-mcn
```

---

## Deploy Application Files

```bash
sudo cp pcscf/target/*.jar /etc/ios-mcn/pcscf.jar
sudo cp icscf/target/*.jar /etc/ios-mcn/icscf.jar
sudo cp scscf/target/*.jar /etc/ios-mcn/scscf.jar
sudo cp n5/target/*.jar /etc/ios-mcn/n5.jar
```

---

## Deploy Configuration Files

Create and deploy the following configuration files:

```text
/etc/ios-mcn/
├── pcscf
├── icscf
├── scscf
├── iosmcn-ims-n5
├── subscribers.json
├── pcscf-logging.xml
├── icscf-logging.xml
├── scscf-logging.xml
├── n5-logging.xml
```

---

## Create Systemd Service Files

Create service files under:

```text
/lib/systemd/system/
```

### P-CSCF Service

`/lib/systemd/system/ios-mcn-pcscf.service`

```ini
[Unit]
Description=IOS MCN P-CSCF Module

[Service]
ExecStart=/bin/bash -c "java -Dapp.config=/etc/ios-mcn/pcscf -Dlogging.config=/etc/ios-mcn/pcscf-logging.xml -jar /etc/ios-mcn/pcscf.jar"
Type=simple
Restart=always
RestartSec=30
TimeoutSec=600

[Install]
WantedBy=multi-user.target
```

### I-CSCF Service

`/lib/systemd/system/ios-mcn-icscf.service`

```ini
[Unit]
Description=IOS MCN I-CSCF Module

[Service]
ExecStart=/bin/bash -c "java -Dapp.config=/etc/ios-mcn/icscf -Dlogging.config=/etc/ios-mcn/icscf-logging.xml -jar /etc/ios-mcn/icscf.jar"
Type=simple
Restart=always
RestartSec=30
TimeoutSec=600

[Install]
WantedBy=multi-user.target
```

### S-CSCF Service

`/lib/systemd/system/ios-mcn-scscf.service`

```ini
[Unit]
Description=IOS MCN S-CSCF Module

[Service]
ExecStart=/bin/bash -c "java -Dapp.config=/etc/ios-mcn/scscf -Dlogging.config=/etc/ios-mcn/scscf-logging.xml -jar /etc/ios-mcn/scscf.jar"
Type=simple
Restart=always
RestartSec=30
TimeoutSec=600

[Install]
WantedBy=multi-user.target
```

### N5 Service

`/lib/systemd/system/ios-mcn-n5.service`

```ini
[Unit]
Description=IOS MCN N5 Interface

[Service]
ExecStart=/bin/bash -c "java -Dapp.config=/etc/ios-mcn/iosmcn-ims-n5 -Dlogging.config=/etc/ios-mcn/n5-logging.xml -jar /etc/ios-mcn/n5.jar"
Type=simple
Restart=always
RestartSec=30
TimeoutSec=600

[Install]
WantedBy=multi-user.target
```

### RESTCONF Service

`/lib/systemd/system/ios-mcn-restconf.service`

```ini
[Unit]
Description=IOS MCN RESTCONF Server

[Service]
ExecStart=/usr/local/bin/restconf-server --yang-dir /opt/ios-mcn/restconf-server/yang
Type=simple
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

---

## Enable Services

```bash
sudo systemctl daemon-reload

sudo systemctl enable postgresql

sudo systemctl enable ios-mcn-pcscf.service
sudo systemctl enable ios-mcn-icscf.service
sudo systemctl enable ios-mcn-scscf.service
sudo systemctl enable ios-mcn-n5.service
sudo systemctl enable ios-mcn-restconf.service
```

---

## Start Services

```bash
sudo systemctl start postgresql

sudo systemctl start ios-mcn-pcscf.service
sudo systemctl start ios-mcn-icscf.service
sudo systemctl start ios-mcn-scscf.service
sudo systemctl start ios-mcn-n5.service
sudo systemctl start ios-mcn-restconf.service
```

---

## Verify Services

```bash
sudo systemctl status ios-mcn-pcscf.service
sudo systemctl status ios-mcn-icscf.service
sudo systemctl status ios-mcn-scscf.service
sudo systemctl status ios-mcn-n5.service
sudo systemctl status ios-mcn-restconf.service
```

Expected output:

```text
Active: active (running)
```

---

## Verify Ports

```bash
sudo ss -tulpn
```

| Component | Default Port |
|------------|--------------|
| P-CSCF | 5060 |
| I-CSCF | 4060 |
| S-CSCF | 6060 |
| N5 | 7777 |
| N5 SBI | 7782 |

---

## View Logs

### P-CSCF

```bash
sudo journalctl -u ios-mcn-pcscf.service -f
```

### I-CSCF

```bash
sudo journalctl -u ios-mcn-icscf.service -f
```

### S-CSCF

```bash
sudo journalctl -u ios-mcn-scscf.service -f
```

### N5

```bash
sudo journalctl -u ios-mcn-n5.service -f
```

### RESTCONF

```bash
sudo journalctl -u ios-mcn-restconf.service -f
```

---

## RESTCONF Verification

```bash
curl http://<server-ip>:8088/healthz
```

Expected output:

```text
OK
```

---

## Post Installation Verification

Verify:

- IMS Registration succeeds.
- IMS AKA Authentication succeeds.
- UDR connectivity is successful.
- N5 connectivity to PCF is successful.
- RESTCONF APIs are reachable.
- Voice calls can be established successfully.
- Video calls can be established successfully.
