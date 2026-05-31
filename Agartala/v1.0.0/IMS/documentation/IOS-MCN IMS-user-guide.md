# IOS-MCN-IMS User Guide

Version: CSCF Agartala v1.0.0

---

## Overview

IOS-MCN-IMS is an integrated IP Multimedia Subsystem (IMS) framework that combines multiple IMS core components into a unified deployment architecture.

The platform includes:

- P-CSCF (Proxy-Call Session Control Function)
- I-CSCF (Interrogating-Call Session Control Function)
- S-CSCF (Serving-Call Session Control Function)
- N5 Interface (Application Function)
- RESTCONF Server

IOS-MCN-IMS is designed to support modern 5G IMS deployments including:

- Voice over New Radio (VoNR)
- Video over New Radio (ViNR)
- IMS Registration and Authentication
- SIP Session Management
- Policy Control Integration
- Centralized Configuration Management

The platform provides a lightweight, modular, and cloud-native IMS implementation suitable for research, private 5G, enterprise, and production environments.

---

## Key Features

##### Integrated IMS Core

- Integrated P-CSCF, I-CSCF and S-CSCF architecture
- End-to-end IMS registration support
- SIP signaling over UDP and TCP
- SIP session establishment and termination
- SIP dialog management
- Multi-threaded SIP processing

##### Authentication and Security

- IMS AKA Authentication
- MILENAGE-based authentication
- RAND, AUTN, CK, IK and RES generation
- IPsec support for secure IMS signaling
- Security context management

##### Unified Subscriber Management

- Direct UDR integration
- Unified subscriber management for IMS and 5G Core
- Reduced dependency on dedicated HSS deployments

##### Policy Control Integration

- N5 Interface support
- AF to PCF communication
- HTTP/2 SBI support
- SCP/NRF integration support

##### Centralized Configuration Management

- RESTCONF Server
- RFC8040 compliant APIs
- YANG model support
- Configuration persistence
- Runtime configuration updates

##### Open Source

- Apache License 2.0
- Commercial use permitted
- Enterprise customization support
- Open and extensible architecture

---

## Building, Configuration and Installation

##### Developer Guide

Refer to the Developer Guide for deployment and configuration procedures.

##### Installation Guide

Refer to the Installation Guide for environment preparation, build instructions, and deployment procedures.

---

## IMS Registration Verification

After deployment, verify IMS registration using IMS-capable User Equipment (UE).

##### Validation Checklist

- UE registration successful
- IMS AKA authentication successful
- UDR subscriber lookup successful
- 401 Authentication challenge successful
- Registration completion successful
- P-CSCF processing verified
- I-CSCF processing verified
- S-CSCF processing verified
- IPsec establishment verified (if enabled)

---

## SIP Call Flow Verification

##### Supported Call Scenarios

- Voice Call (VoNR)
- Video Call (ViNR)
- Mobile Originated Calls
- Mobile Terminated Calls
- SIP Registration
- Call Release Procedures

##### SIP Procedures Validated

- REGISTER
- INVITE
- 100 Trying
- 180 Ringing
- 183 Session Progress
- PRACK
- UPDATE
- 200 OK
- ACK
- BYE

##### Validation Checklist

- Successful IMS Registration
- Successful Call Establishment
- Successful Media Negotiation
- Successful Call Release
- Successful Session Refresh Handling
- Successful Dialog Continuity Handling

---

## N5 Interface

The N5 Interface acts as the Application Function (AF) component and communicates with the Policy Control Function (PCF) in a 5G Core network.

##### Capabilities

- HTTP/2 Communication
- SBI Messaging
- Policy Authorization
- Traffic Influence
- AF Session Management
- SCP Routing Support

---

## RESTCONF Server

The RESTCONF Server provides centralized configuration and operational management capabilities for all IMS components.

##### Features

- RFC8040 RESTCONF APIs
- Bearer Token Authentication
- YANG Model Support
- Configuration Persistence
- Runtime Configuration Updates

##### Available Endpoints

```text
/restconf
/restconf/data
/restconf/operations
/healthz
/.well-known/host-meta