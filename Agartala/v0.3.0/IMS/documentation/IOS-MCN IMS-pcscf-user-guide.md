
# P-CSCF Application User Guide

## Overview

The Proxy-Call Session Control Function (P-CSCF) module is a critical component in the IP Multimedia Subsystem (IMS) network architecture. It is responsible for handling SIP signaling, serving as the first contact point for IMS User Equipment (UE), and forwarding requests to the appropriate CSCF components.

---

### Building, Configuration and Installation

Refer this for [deployment and configuration](./pcscf-developer-guide.md)

Refer this for [installation](./pcscf-installation-guide.md)

---

## SIP Call Flow Verification

Once deployed, you may test the SIP call flows using IMS-capable UEs or simulated SIP clients.
Currently, Samsung A55, M14 and A14 UEs have been tested successfully.

Ensure:

- Proper registration of the UE.
- You are calling at the correct MSISDN as configured in the subscribers.json file.
- SIP INVITE and 200 OK messages are exchanged.
- BYE messages are received and properly processed to release call sessions.
- Call from various parties is successful, both voice and video calls.
