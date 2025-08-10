
# N5 Interface Troubleshooting Guide

This guide provides help for diagnosing and resolving common issues with the N5 Interface implementation.

---

## Common Issues & Solutions

### 1. **N5 Service Not Starting**
- **Symptom**: The container fails to start or crashes immediately.
- **Resolution**:
  - Check Docker logs using: `docker logs n5-container`
  - Verify that all required IP and PORT configurations are correctly set inside the Dockerfile.
  - Ensure that port `8080` is available and not blocked by a firewall.

---

### 2. **SCP/PCF Connection Fails**
- **Symptom**: N5 logs show errors related to connection failures with SCP or PCF.
- **Resolution**:
  - Make sure the `SCP-IP`, `SCP-PORT`, `PCF-IP`, and `PCF-PORT` values are correct in the Dockerfile.
  - Confirm that the SCP and PCF services are running and listening on the correct interfaces.
  - Ensure network reachability from the N5 container to these interfaces.

---

### 3. **No Response from N5 Endpoint**
- **Symptom**: HTTP clients or services do not receive any response from the N5 API.
- **Resolution**:
  - Check that port `8080` is exposed and mapped correctly using `docker ps`.
  - Verify application logs to ensure the API service has started without exceptions.
  - Confirm that the application is bound to `AF-BIND-IP` as set in the Dockerfile.

---

### 4. **Unexpected Response Codes**
- **Symptom**: Client receives `500 Internal Server Error` or `400 Bad Request` unexpectedly.
- **Resolution**:
  - Review logs to identify exception traces or validation errors.
  - Validate the incoming request JSON against the expected schema.
  - Make sure SCP/PCF endpoints are returning valid responses to N5.

---

## FAQs

### **Q1: How do I change the binding IP or port for N5?**
Edit the `AF-BIND-IP` and `AF-BIND-PORT` values directly in the Dockerfile and rebuild the image using:
```bash
docker build -t n5-service .
```

### **Q2: How do I verify N5 is listening on the correct port?**
Run the following command after starting the container:
```bash
docker exec -it n5-container netstat -tulnp
```

### **Q3: How to restart the N5 container cleanly?**
```bash
docker stop n5-container
docker rm n5-container
docker run -d --name n5-container -p 8080:8080 n5-service
```

### **Q4: Where can I find logs for debugging?**
Inside the container, logs are printed to the console. You can use:
```bash
docker logs n5-container
```

### **Q5: My SCP/PCF is returning timeout errors, what should I check?**
- Ensure SCP/PCF is running and reachable.
- Test network connectivity using ping or curl from inside the container.
- Check for any firewall rules blocking the request.
