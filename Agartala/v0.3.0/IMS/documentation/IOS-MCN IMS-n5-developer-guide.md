
# Developer Guide – N5 Interface v0.3.0

This guide provides developers with everything needed to build the **IOS-MCN-N5 v0.3.0** project. The N5 interface enables interaction between the Application Function (AF) and the 5G Core Policy Control Function (PCF), and is fully Dockerized for streamlined deployment.

---

## Architecture Overview

The N5 Interface exposes a **HTTP/2 SBI-based endpoint** that allows an Application Function (AF) such as IMS P-CSCF to:

- Register itself with the **NRF**
- Initiate and manage **PDU sessions** via the **PCF**

---

## Docker Installation on Ubuntu
Docker on Ubuntu can be installed by following the steps in this [link](https://docs.docker.com/engine/install/ubuntu/)


## Configuration – IP and PORT Setup

All IP address and port configurations for the N5 Interface and its 5G Core peers (PCF, SCP) **must be defined in the `Dockerfile`** prior to build time.

Update the variables inside the `Dockerfile`:

```Dockerfile
# IP Address of SCP HTTP2 SBI Interface in 5G Core
SCP-IP=127.0.0.200                     

# Port of SCP HTTP2 SBI Interface in 5G Core
SCP-PORT=7777                           

# IP Address of PCF HTTP2 SBI Interface in 5G Core
PCF-IP=127.0.0.13                    

# Port of PCF HTTP2 SBI Interface in 5G Core
PCF-PORT=7777                           

# IP Address where N5 Interface should bind (AF Interface)
AF-BIND-IP=127.0.0.201                

# Port where N5 Interface listens
AF-BIND-PORT=7777                     

#IP Address of N5-Interface SBI HTTP Interface where IMS will Request For QoS
AF-BIND-SBI-IP=127.0.0.201

#Port of N5-Interface SBI HTTP Interface where IMS will Request For QoS
AF-BIND-SBI-PORT=7782
```

> ⚠️ **NOTE**: These variables are injected during the image build process. Make sure to edit them before running `docker build`.

---

## Docker – Build

### Build Docker Image

Navigate to the source code directory and run:

```bash
sudo docker build -t n5-service .
```

This command creates a Docker image named `n5-service` using the `Dockerfile` in your project root.
