
# N5 Interface Application – User Guide

## Overview

The N5 Interface Application acts as the Application Function (AF) component that communicates with the Policy Control Function (PCF) over the N5 interface in a 5G Core network. This service is deployed as a containerized microservice and supports standard SBI (Service-Based Interface) messaging over HTTP/2.

---

## 1. Prerequisites

- Docker installed on the host system.
- Access to configured PCF and SCP services running in the 5G Core network.
- Properly configured `Dockerfile` with updated IP and port bindings for:
  - SCP (Service Communication Proxy)
  - PCF (Policy Control Function)
  - N5 Binding Interface (AF binding)

---

## 2. Configuration Parameters

All the parameters listed below must be **hardcoded into the `Dockerfile`** before building the container:

| Parameter             | Description                            | Example             |
|----------------------|----------------------------------------|---------------------|
| `SCP-IP`             | SCP Interface IP Address               | `127.0.0.200`       |
| `SCP-PORT`           | SCP Interface Port                     | `7777`              |
| `PCF-IP`             | PCF Interface IP Address               | `127.0.0.13`        |
| `PCF-PORT`           | PCF Interface Port                     | `7777`              |
| `AF-BIND-IP`         | N5 Interface IP Address (AF Binding)   | `127.0.0.201`       |
| `AF-BIND-PORT`       | N5 Interface Port (AF Binding)         | `7777`              |

---

## 3. Build Instructions

[Refer this document](./IOS-MCN%20IMS-n5-developer-guide.md)


## 4. Running the N5 Service

[Refer this document](./IOS-MCN%20IMS-n5-installation-guide.md)


## 5. Health Check and Logs

To verify the service is running:

```bash
docker ps
```

To check logs:

```bash
docker logs n5-container
```

---

## 6. API Flow

Once the N5 application is running:

- It binds to the AF IP and port defined in the `Dockerfile`.
- Sends HTTP/2 SBI requests to the PCF over the N5 interface.
- Uses the SCP as intermediary routing if applicable.

Use tools like `curl` or Postman to send test HTTP2 requests (if TLS is configured) to:

```
https://<AF-BIND-IP>:<AF-BIND-PORT>/n5/<resource>
```

The API guide, along with API responses can be found [here](./IOS-MCN%20IMS-n5-api-guide.md)
