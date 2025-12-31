# IOS-MCN-IMS Troubleshooting Guide

## P-CSCF Troubleshooting Guide

This guide provides detailed troubleshooting steps and frequently asked questions for the P-CSCF component in the IMS architecture. Use this document to debug common deployment and runtime issues.

---

### Logs and Debugging

#### View Logs

**Dockerized:**
```bash
sudo docker logs iosmcn-ims-container
```

**Bare Metal (systemd):**
```bash
journalctl -u ios-mcn-pcscf.service -f
```

---

### Common Issues and Fixes

#### 1. UE fails to attach to core
**Symptoms:**
- Device fails to attach.

**Fix:**
- Ensure correct APN and IMS profile configuration on UE.
- Verify PCSCF IP/PORT is reachable and SIP traffic is not blocked by firewall.

#### 2. Calls fail after a large number of iterations
**Symptoms:**
- Call processing fails after 50-60+ continuous calls.

**Fix:**
- Wait for 10 seconds before initiating another call. This issue might only arise if you make calls rapidly.

#### 3. Complete stalemate and no calls initiating after wait time
**Symptoms**:
- Multiple call processing fails after waiting for 10 seconds.

**Fix:**
- This is a very very rare scenario after the v0.1.3 patch.
- If this occurs, re-attaching the UE will help.

---

### Diagnostic Commands

**Check container health:**
```bash
sudo docker ps -a
sudo docker logs iosmcn-ims-container
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

### FAQs

#### Q1: Where can I configure the IP and PORT for P-CSCF?
**A:**  
- In Docker builds, these are hardcoded into the `Dockerfile`.
- In bare metal builds, use the file `/etc/ios-mcn/pcscf`.

#### Q2: What is the expected file structure for bare metal configuration?
**A:**
```
/etc/ios-mcn/
├── pcscf
├── pcscf-logging.xml
├── subscribers.json
/lib/systemd/system/
└── ios-mcn-pcscf.service
```

#### Q3: How to restart P-CSCF after modifying configs?
**Docker:**
```bash
sudo docker restart iosmcn-ims-container
```
**Bare Metal:**
```bash
sudo systemctl restart ios-mcn-pcscf.service
```


## N5 Interface Troubleshooting Guide

This guide provides help for diagnosing and resolving common issues with the N5 Interface implementation.

---

### Common Issues & Solutions

#### 1. **N5 Service Not Starting**
- **Symptom**: The container fails to start or crashes immediately.
- **Resolution**:
  - Check Docker logs using: `docker logs iosmcn-ims-container`
  - Verify that all required IP and PORT configurations are correctly set inside the Dockerfile.
  - Ensure that port `8080` is available and not blocked by a firewall.

---

#### 2. **SCP/PCF Connection Fails**
- **Symptom**: N5 logs show errors related to connection failures with SCP or PCF.
- **Resolution**:
  - Make sure the `SCP-IP`, `SCP-PORT`, `PCF-IP`, and `PCF-PORT` values are correct in the Dockerfile.
  - Confirm that the SCP and PCF services are running and listening on the correct interfaces.
  - Ensure network reachability from the IOSMCN-IMS container to these interfaces.

---

#### 3. **No Response from N5 Endpoint**
- **Symptom**: HTTP clients or services do not receive any response from the N5 API.
- **Resolution**:
  - Check that port `8080` is exposed and mapped correctly using `docker ps`.
  - Verify application logs to ensure the API service has started without exceptions.
  - Confirm that the application is bound to `AF-BIND-IP` as set in the Dockerfile.

---

#### 4. **Unexpected Response Codes**
- **Symptom**: Client receives `500 Internal Server Error` or `400 Bad Request` unexpectedly.
- **Resolution**:
  - Review logs to identify exception traces or validation errors.
  - Validate the incoming request JSON against the expected schema.
  - Make sure SCP/PCF endpoints are returning valid responses to N5.

---

### FAQs

#### **Q1: How do I change the binding IP or port for N5?**
Edit the `AF-BIND-IP` and `AF-BIND-PORT` values directly in the Dockerfile and rebuild the image using:
```bash
sudo sudo docker build -t iosmcn-ims .
```

#### **Q2: How do I verify N5 is listening on the correct port?**
Run the following command after starting the container:
```bash
sudo docker exec -it iosmcn-ims-container netstat -tulnp
```

#### **Q3: How to restart the N5 container cleanly?**
```bash
sudo docker stop iosmcn-ims-container
sudo docker rm iosmcn-ims-container
sudo docker run -d --name iosmcn-ims-container -p 8080:8080 -p 5060:5060 iosmcn-ims

```

#### **Q4: Where can I find logs for debugging?**
Inside the container, logs are printed to the console. You can use:
```bash
sudo docker logs iosmcn-ims-container
```

#### **Q5: My SCP/PCF is returning timeout errors, what should I check?**
- Ensure SCP/PCF is running and reachable.
- Test network connectivity using ping or curl from inside the container.
- Check for any firewall rules blocking the request.
