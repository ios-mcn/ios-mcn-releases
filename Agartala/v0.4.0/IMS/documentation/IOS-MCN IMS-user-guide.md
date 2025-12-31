# IOS-MCN-IMS User Guide

## Overview

The **IOS-MCN-IMS** project combines the functionalities of the **Proxy–Call Session Control Function (P-CSCF)** and the **N5 interface**.

This integrated module enables a complete and streamlined IMS component for **5G Core** deployments, supporting **Voice over New Radio (VoNR)** and **Video over New Radio (ViNR)** services.

It provides optimized **SIP signaling**, **policy control integration**, and **session management** with a lightweight and high-performance architecture suitable for both experimental and production-grade 5G IMS environments.

---

### Building, Configuration and Installation

Refer this for [deployment and configuration](./iosmcn-ims-developer-guide.md)

Refer this for [installation](./iosmcn-ims-installation-guide.md)

---

## PCSCF- SIP Call Flow Verification

Once deployed, you may test the SIP call flows using IMS-capable UEs or simulated SIP clients.
Currently, Samsung A55, M14 and A14 UEs have been tested successfully.

Ensure:

- Proper registration of the UE.
- You are calling at the correct MSISDN as configured in the subscribers.json file.
- SIP INVITE and 200 OK messages are exchanged.
- BYE messages are received and properly processed to release call sessions.
- Call from various parties is successful, both voice and video calls.

---

## N5 Interface- 

The N5 Interface Application acts as the Application Function (AF) component that communicates with the Policy Control Function (PCF) over the N5 interface in a 5G Core network. This service is deployed as a containerized microservice and supports standard SBI (Service-Based Interface) messaging over HTTP/2.

## API Flow

Once the N5 application is running:

- It binds to the AF IP and port defined in the `Dockerfile`.
- Sends HTTP/2 SBI requests to the PCF over the N5 interface.
- Uses the SCP as intermediary routing if applicable.

Use tools like `curl` or Postman to send test HTTP2 requests (if TLS is configured) to:

```
https://<AF-BIND-IP>:<AF-BIND-PORT>/n5/<resource>
```

The API guide, along with API responses can be found [here](./iosmcn-ims-api-guide.md)