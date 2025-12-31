# IOS-MCN-IMS – Agartala v0.4.0

The **IOS-MCN-IMS** project combines the functionalities of the **Proxy–Call Session Control Function (P-CSCF)** and the **N5 interface**.

This integrated module enables a complete and streamlined IMS component for **5G Core** deployments, supporting **Voice over New Radio (VoNR)** and **Video over New Radio (ViNR)** services.

It provides optimized **SIP signaling**, **policy control integration**, and **session management** with a lightweight and high-performance architecture suitable for both experimental and production-grade 5G IMS environments.

---

## Overview

The IOS-MCN-IMS module implements:
- **P-CSCF Node** – for managing SIP signaling between User Equipment (UE) and IMS Core components.
- **N5 Interface** – for enabling communication between the IMS Application Function (AF) and the Policy Control Function (PCF) in the 5G Core.

This unified system ensures seamless policy-controlled session handling and real-time service management for next-generation communication services.

---

## Core Functionalities

### SIP Signaling and Session Control

The integrated SIP processing engine supports all of the core SIP Methods and responses, notably-

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

This comprehensive method and response support ensures full compatibility with IMS-compliant SIP signaling and 5G VoNR/ViNR service flows.

---

### N5 Policy Interface Integration

The module natively integrates the **N5 interface** for dynamic policy control and Quality of Service (QoS) management via the **Policy Control Function (PCF)**.

#### NF Registration
- Registers the IMS node as an **Application Function (AF)** with the **Network Repository Function (NRF)**.
- Maintains active registration using a configurable **heartbeat timer**.

#### Audio and Video PDU Session Management
- Establishes **Audio (VoNR)** and **Video (ViNR)** PDU sessions with PCF for policy-based QoS enforcement.
- Dynamically negotiates QoS profiles for differentiated traffic treatment.

#### PDU Session Deletion
- Gracefully terminates policy-controlled sessions.
- Notifies PCF to remove policy associations and release resources.

---

### Lightweight Architecture

The IOS-MCN-IMS adopts a **minimalist, socket-based** design for superior performance and low latency.

Key aspects include:
- **Custom SIP Stack**: Fully developed in-house, independent of third-party SIP libraries.
- **Direct Socket Communication**: Handles SIP messages directly over UDP/TCP on port `5060`.
- **Low Latency Operation**: Designed for high throughput and minimal overhead, ideal for 5G testbeds and lightweight deployments.

---

### Session Management and Cleanup

- **Call Flow Management**: Establishes, maintains, and terminates SIP-based multimedia sessions in real time.
- **In-Memory State Tracking**: Maintains active session data structures for tracking live calls.
- **Automatic Resource Cleanup**: Detects timeouts and disconnections, ensuring proper resource and memory release.

---

## Supported 5G IMS Use Cases

- **Voice over New Radio (VoNR)**
- **Video over New Radio (ViNR)**
- **Policy-Controlled QoS Sessions** for real-time services

---

## Summary

The IOS-MCN-IMS project provides a cohesive, open-source implementation that bridges the signaling and policy control layers of 5G IMS.

By integrating **P-CSCF** signaling logic with the **N5 policy interface**, this module enables efficient, standards-aligned IMS behavior while maintaining the flexibility, transparency, and performance expected in modern 5G core environments.