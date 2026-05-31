# IOS-MCN-IMS Troubleshooting Guide

## Overview

This guide provides troubleshooting procedures and diagnostic steps for the IOS-MCN-IMS platform.

The guide covers:

- P-CSCF
- I-CSCF
- S-CSCF
- N5 Interface
- RESTCONF Server
- UDR Integration
- IMS AKA Authentication
- IPsec Connectivity

---

## General Diagnostics

### View Container Logs

```bash
docker logs <container-name>
```

### View Service Logs

```bash
journalctl -u <service-name> -f
```

### Verify Running Containers

```bash
docker ps -a
```

### Verify Listening Ports

```bash
ss -tulpn
```

---

# P-CSCF Troubleshooting

## UE Registration Failure

### Symptoms

- UE unable to register
- Repeated REGISTER attempts
- No 401 Unauthorized challenge received

### Resolution

- Verify P-CSCF service is running.
- Verify SIP port accessibility.
- Verify IMS APN configuration.
- Verify firewall settings.
- Verify UE can reach the P-CSCF IP address.

### Diagnostics

```bash
ss -tulpn | grep 5060
```

```bash
tcpdump -i any port 5060
```

---

## IPsec Establishment Failure

### Symptoms

- Registration stops after 401 challenge
- Security association not established

### Resolution

- Verify IPsec is enabled.
- Verify Security-Server headers.
- Verify CK and IK generation.
- Verify UE supports IMS IPsec procedures.

### Diagnostics

```bash
ip xfrm state
```

```bash
ip xfrm policy
```

---

## Call Setup Failure

### Symptoms

- Registration successful
- INVITE processing fails

### Resolution

- Verify I-CSCF connectivity.
- Verify S-CSCF connectivity.
- Verify subscriber provisioning.
- Verify Route and Record-Route headers.

---

# I-CSCF Troubleshooting

## REGISTER Not Forwarded

### Symptoms

- REGISTER reaches I-CSCF
- No response from S-CSCF

### Resolution

- Verify S-CSCF IP and port.
- Verify routing configuration.
- Verify connectivity between I-CSCF and S-CSCF.
- Verify UDR lookup functionality.

### Diagnostics

```bash
tcpdump -i any port <icscf-port>
```

```bash
tcpdump -i any port <scscf-port>
```

---

## Subscriber Lookup Failure

### Symptoms

- SIP 403 Forbidden
- Registration rejected

### Resolution

- Verify subscriber exists in UDR.
- Verify IMSI format.
- Verify UDR connectivity.

---

# S-CSCF Troubleshooting

## Authentication Failure

### Symptoms

- Repeated 401 responses
- Registration never completes

### Resolution

- Verify subscriber credentials.
- Verify K and OP/OPc values.
- Verify SQN synchronization.
- Verify authentication vector generation.

### Authentication Parameters

- RAND
- AUTN
- CK
- IK
- RES
- XRES

---

## INVITE Rejected

### Symptoms

- Registration successful
- Call setup fails

### Resolution

- Verify subscriber registration state.
- Verify routing configuration.
- Verify subscriber provisioning.

---

# UDR Troubleshooting

## Subscriber Lookup Failure

### Symptoms

- Registration rejected
- SIP 403 Forbidden

### Resolution

- Verify UDR service availability.
- Verify subscriber records.
- Verify IMSI mappings.

### Diagnostics

```bash
curl http://<udr-ip>:<udr-port>
```

---

# N5 Interface Troubleshooting

## N5 Service Not Starting

### Symptoms

- Container exits immediately
- Service startup failure

### Resolution

- Verify N5 configuration.
- Verify AF bind IP and port.
- Verify SCP/NRF configuration.
- Verify PCF configuration.

### Diagnostics

```bash
docker logs <iosmcn-ims-container-name>
```

---

## SCP/NRF or PCF Connectivity Failure

### Symptoms

- Policy requests timeout
- HTTP/2 connection failures

### Resolution

- Verify SCP/NRF connectivity.
- Verify PCF connectivity.
- Verify network routing.
- Verify firewall configuration.

### Diagnostics

```bash
curl http://<scp-ip>:<scp-port>
or
curl http://<nrf-ip>:<nrf-port>
```

```bash
curl http://<pcf-ip>:<pcf-port>
```

---

## HTTP/2 SBI Errors

### Symptoms

- Unexpected response codes
- SBI request failures

### Resolution

- Verify HTTP/2 support.
- Verify request payloads.
- Verify PCF responses.

---

# RESTCONF Server Troubleshooting

## RESTCONF Server Not Reachable

### Symptoms

- Connection refused
- API requests fail

### Resolution

- Verify RESTCONF service status.
- Verify RESTCONF port configuration.
- Verify firewall settings.

### Diagnostics

```bash
curl http://<restconf-ip>:8088/healthz
```

Expected Response:

```text
OK
```

---

## Authentication Failure

### Symptoms

- HTTP 401 Unauthorized
- HTTP 403 Forbidden

### Resolution

- Verify Bearer token.
- Verify Authorization header.
- Verify RESTCONF token configuration.

### Example

```bash
curl \
-H "Authorization: Bearer <token>" \
http://<restconf-ip>:8088/restconf
```

---

# Frequently Asked Questions

## How do I verify IMS registration?

Verify the following SIP sequence:

```text
REGISTER
401 Unauthorized
REGISTER (with Authorization)
200 OK
```

---

## How do I verify subscriber provisioning?

Verify the subscriber exists in UDR and is accessible by I-CSCF and S-CSCF.

---

## How do I restart IMS services?

### Docker

```bash
docker restart <container-name>
```

### Systemd for Bare Metal

```bash
systemctl restart <service-name>
```

---

## How do I verify RESTCONF operation?

```bash
curl http://<restconf-ip>:8088/healthz
```

Expected output:

```text
OK
```

---

## Recommended Troubleshooting Flow

1. Verify service status.
2. Verify network connectivity.
3. Verify UDR connectivity.
4. Verify IMS registration.
5. Verify SIP call flow.
6. Verify N5 connectivity.
7. Verify RESTCONF accessibility.

This sequence typically helps isolate and resolve most deployment and operational issues efficiently.