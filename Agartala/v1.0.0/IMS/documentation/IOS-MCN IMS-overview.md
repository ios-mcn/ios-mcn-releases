# IOS-MCN-IMS – CSCF Agartala v1.0.0

The **IOS-MCN-IMS** project provides a complete and integrated IMS framework combining **P-CSCF**, **I-CSCF**, **S-CSCF**, **N5 Interface**, and **RESTCONF Server** into a unified architecture.

This release enables a streamlined IMS deployment for **5G Core** networks supporting **Voice over New Radio (VoNR)** and **Video over New Radio (ViNR)** services while providing integrated subscriber management, policy control, authentication, and configuration management capabilities.

It delivers optimized **SIP signaling**, **IMS AKA authentication**, **policy control integration**, **UDR-based subscriber management**, and **RESTCONF-based configuration management** with a lightweight and high-performance architecture suitable for research, private 5G, enterprise, and production-grade IMS environments.

---

## Overview

The IOS-MCN-IMS platform implements:

- **P-CSCF (Proxy-Call Session Control Function)** – Handles SIP signaling between User Equipment (UE) and IMS Core.
- **I-CSCF (Interrogating-Call Session Control Function)** – Provides routing and subscriber lookup functionality.
- **S-CSCF (Serving-Call Session Control Function)** – Manages IMS registration, authentication, and session control.
- **N5 Interface** – Enables communication between the IMS Application Function (AF) and Policy Control Function (PCF).
- **RESTCONF Server** – Provides centralized configuration and operational management APIs.
- **UDR Integration** – Supports unified subscriber management across IMS and 5G Core environments.

This integrated architecture simplifies IMS deployment while maintaining standards-compliant SIP signaling and policy-controlled service delivery.

---

## Core Functionalities

### SIP Signaling and Session Control

The integrated SIP processing engine supports core SIP methods and responses required for IMS deployments.

#### Supported SIP Methods

- `REGISTER` – Handles IMS registration procedures.
- `INVITE` – Initiates voice and video sessions.
- `ACK` – Confirms successful session establishment.
- `BYE` – Terminates active sessions.
- `CANCEL` – Cancels pending session requests.
- `PRACK` – Supports reliable provisional responses.
- `UPDATE` – Modifies session parameters during active dialogs.
- `INFO` – Exchanges mid-session information.
- `SUBSCRIBE` – Requests event notifications.
- `NOTIFY` – Delivers event notifications.

#### Supported SIP Responses

##### 1xx (Provisional Responses)

- `100 Trying`
- `180 Ringing`
- `183 Session Progress`

##### 2xx (Successful Responses)

- `200 OK`

##### 4xx (Client Failure Responses)

- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `486 Busy Here`

##### 5xx (Server Failure Responses)

- Standard IMS server-side error handling.

This comprehensive SIP support enables standards-compliant IMS signaling for VoNR and ViNR deployments.

---

### IMS Registration and Authentication

The platform includes native IMS AKA authentication support using MILENAGE algorithms.

#### Supported Features

- IMS AKA Authentication
- MILENAGE Authentication
- RAND Generation
- AUTN Generation
- CK Generation
- IK Generation
- RES/XRES Validation
- SQN Management
- Security Context Management

#### Security Features

- IMS AKA Authentication
- IPsec Support
- Security Association Management
- Secure SIP Signaling

---

### UDR-Based Subscriber Management

The platform supports direct integration with the User Data Repository (UDR).

#### Benefits

- Unified subscriber management for IMS and 5G Core
- Centralized subscriber data storage
- Authentication data management
- Reduced dependency on dedicated HSS deployments
- Simplified deployment architecture

---

### N5 Policy Interface Integration

The N5 Interface natively integrates policy control capabilities through communication with the Policy Control Function (PCF).

#### NF Registration

- Registers the IMS node as an Application Function (AF).
- Supports lifecycle management and heartbeat procedures.

#### Policy Control

- Policy Authorization
- Traffic Influence
- QoS Enforcement
- Session Management
- HTTP/2 SBI Communication
- SCP-Based Routing

#### Audio and Video Session Management

- Supports VoNR policy-controlled sessions.
- Supports ViNR policy-controlled sessions.
- Enables QoS-aware service delivery.

---

### RESTCONF Configuration Management

The platform includes an integrated RESTCONF server for centralized configuration management.

#### Features

- RFC8040 RESTCONF APIs
- YANG Model Support
- Configuration Persistence
- Runtime Configuration Updates
- Token-Based Authentication

#### Available Endpoints

```text
/restconf
/restconf/data
/restconf/operations
/healthz
/.well-known/host-meta
```

---

### Lightweight Architecture

The IOS-MCN-IMS framework adopts a lightweight and modular architecture designed for high-performance IMS deployments.

Key characteristics include:

- Multi-threaded SIP Processing
- Socket-Based Communication
- UDP/TCP Transport Support
- Container-Friendly Deployment
- Modular IMS Components
- Low-Latency Operation
- Cloud-Native Deployment Support

---

### Session Management and Cleanup

- IMS Registration Management
- SIP Dialog Tracking
- Session Establishment
- Session Modification
- Session Termination
- Automatic Resource Cleanup
- Timeout Handling
- State Management

---

## Supported 5G IMS Use Cases

### Voice Services

- Voice over New Radio (VoNR)
- IMS Voice Calling

### Video Services

- Video over New Radio (ViNR)
- IMS Video Calling

### IMS Services

- IMS Registration
- Authentication
- Session Establishment
- Session Modification
- Session Termination
- Policy-Controlled Services

---

## IOS-MCN-IMS Advantages

### Integrated IMS Framework

Provides P-CSCF, I-CSCF, S-CSCF, N5 Interface, and RESTCONF Server within a single deployable framework.

### Unified Subscriber Management

Supports direct UDR integration for subscriber and authentication data management across IMS and 5G Core environments.

### Native IMS Authentication

Provides built-in IMS AKA and MILENAGE authentication capabilities.

### Centralized Configuration Management

RESTCONF-based configuration management simplifies deployment and operational management.

### Open Source

Distributed under the Apache License 2.0, supporting commercial use, customization, redistribution, and enterprise adoption.

---

## Supported 5G Deployments

- Voice over New Radio (VoNR) Deployments
- Video over New Radio (ViNR) Deployments
- Policy-Controlled QoS Sessions for Voice and Video Services
- IMS-Based Voice and Multimedia Services
- IMS with 5G Network Deployments
- Enterprise IMS Communication Platforms
- Research and Development Testbeds
- Unified IMS and 5G Core Subscriber Management Deployments

---

## Summary

The IOS-MCN-IMS platform provides a unified and open-source IMS implementation that combines SIP signaling, authentication, subscriber management, policy control, and configuration management within a single framework.

By integrating **P-CSCF**, **I-CSCF**, **S-CSCF**, **N5 Interface**, **RESTCONF Server**, and **UDR Integration**, the platform simplifies IMS deployment while delivering standards-compliant functionality required for modern 5G communication services.
