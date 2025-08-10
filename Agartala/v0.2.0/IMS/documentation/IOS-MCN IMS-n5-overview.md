# N5 Interface – Agartala v0.0.1

This project implements the **N5 interface**, a standardized 3GPP reference point between the **Policy Control Function (PCF)** and an **Application Function (AF)**, such as IMS P-CSCF, in a 5G Core network.

The N5 interface allows Application Functions to request policy control for application sessions requiring differentiated QoS, enabling seamless **VoNR**, **ViNR**, and other real-time services.

`N5 agartala v0.0.1` provides key functionalities including **Audio and Video PDU Session Creation**, **Session Deletion**, and **NF Registration** of the P-CSCF node.

---

## Highlights

### NF Registration
- Registers the P-CSCF node with the NRF as a 5G Network Function (AF)
- Includes **heartbeat timer** mechanism to maintain active registration status

### Audio PDU Session Creation
- Initiates policy-controlled sessions for voice streams (VoNR)
- Ensures correct QoS enforcement via PCF

### Video PDU Session Creation
- Enables video stream session setup for services like ViNR
- Leverages dynamic QoS profiles communicated to PCF

### PDU Session Deletion
- Handles proper teardown of AF sessions
- Notifies PCF to remove policy associations gracefully