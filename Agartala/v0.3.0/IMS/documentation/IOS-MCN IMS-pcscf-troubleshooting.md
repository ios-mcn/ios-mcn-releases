# P-CSCF Troubleshooting Guide

This guide provides detailed troubleshooting steps and frequently asked questions for the P-CSCF component in the IMS architecture. Use this document to debug common deployment and runtime issues.

---

## Logs and Debugging

### View Logs

**Dockerized:**
```bash
sudo docker logs pcscf-container
```

**Bare Metal (systemd):**
```bash
journalctl -u ios-mcn-pcscf.service -f
```

---

## Common Issues and Fixes

### 1. UE fails to attach to core
**Symptoms:**
- Device fails to attach.

**Fix:**
- Ensure correct APN and IMS profile configuration on UE.
- Verify PCSCF IP/PORT is reachable and SIP traffic is not blocked by firewall.

### 2. Calls fail after a large number of iterations
**Symptoms:**
- Call processing fails after 50-60+ continuous calls.

**Fix:**
- Wait for 10 seconds before initiating another call. This issue might only arise if you make calls rapidly.

### 3. Complete stalemate and no calls initiating after wait time
**Symptoms**:
- Multiple call processing fails after waiting for 10 seconds.

**Fix:**
- This is a very very rare scenario after the v0.1.3 patch.
- If this occurs, re-attaching the UE will help.

---

## Diagnostic Commands

**Check container health:**
```bash
docker ps -a
docker logs pcscf-container
```

**Check service status (bare metal):**
```bash
sudo systemctl status ios-mcn-pcscf.service
```

**Check listening port:**
```bash
sudo netstat -tulnp | grep 5060
```

---

## FAQs

### Q1: Where can I configure the IP and PORT for P-CSCF?
**A:**  
- In Docker builds, these are hardcoded into the `Dockerfile`.
- In bare metal builds, use the file `/etc/ios-mcn/pcscf`.

### Q2: What is the expected file structure for bare metal configuration?
**A:**
```
/etc/ios-mcn/
├── pcscf
├── pcscf-logging.xml
├── subscribers.json
/lib/systemd/system/
└── ios-mcn-pcscf.service
```

### Q3: How to restart P-CSCF after modifying configs?
**Docker:**
```bash
docker restart pcscf-container
```
**Bare Metal:**
```bash
sudo systemctl restart ios-mcn-pcscf.service
```