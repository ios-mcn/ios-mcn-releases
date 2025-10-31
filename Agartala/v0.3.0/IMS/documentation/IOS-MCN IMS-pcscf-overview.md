# P-CSCF – Agartala v0.3.0

This project implements a **Proxy–Call Session Control Function (P-CSCF)** node as part of the **IP Multimedia Subsystem (IMS)**, customized for modern 5G IMS deployment scenarios such as **VoNR** (Voice over New Radio) and **ViNR** (Video over New Radio).

The `P-CSCF agartala v0.3.0` release focuses on **SIP signaling**, **session management**, and **lightweight design**, featuring a **custom SIP stack** for core IMS call flows without reliance on third-party SIP libraries.

This implementation is optimized for direct socket-based message processing and maintains fine-grained control over session states and resource cleanup.

---

## Highlights

### SIP Message Handling

Supports core SIP signaling methods used in IMS sessions:
- `REGISTER` – For user agent registration with IMS
- `INVITE` – Call initiation
- `ACK` – Call establishment confirmation
- `BYE` – Session termination

Handles essential SIP provisional and informational responses:
- `100 Trying`
- `180 Ringing`
- `183 Session Progress`

Additional Support:
- `PRACK` – For reliable provisional response handling

---

### Lightweight Design

- **Custom SIP Stack**: Fully developed in-house, not dependent on external SIP libraries
- **Direct Socket Communication**: Processes SIP messages directly over UDP/TCP sockets on port `5060`
- **Low Latency**: Minimal overhead design ideal for embedded telecom testbeds and experimental IMS cores

---

### Session Management and Cleanup

- **Call Flow Management**:
  - Establishes, maintains, and terminates IMS sessions
  - Supports real-time services like VoNR and ViNR
- **Session State Maintenance**:
  - Retains active session data in memory for ongoing call tracking
- **Cleanup Mechanism**:
  - Detects session timeout or termination events
  - Ensures proper memory/resource release to prevent leaks