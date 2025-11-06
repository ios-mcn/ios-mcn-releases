
# Installation Guide – IOS-MCN-IMS v0.3.0

This guide explains how to install and run the **P-CSCF** module either via Docker or on a bare metal Linux system.

---

## Docker-Based Installation

### Step 1: Build Docker Image
[Refer](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.3.0/IMS/documentation/IOS-MCN%20IMS-pcscf-developer-guide.md)

### Step 2: Run Container

```bash
sudo docker run -d --name pcscf-container -p 5060:5060 pcscf
```

### Step 3: Access Container Shell

```bash
sudo docker exec -it pcscf-container /bin/bash
```

This gives you interactive access to the container shell for inspection or debugging.

### Step 4: Verify

To verify the container is running:

```bash
sudo docker ps
```

You should see `pcscf-container` in the running list.

To check logs:

```bash
sudo docker logs -f pcscf-container
```

---

### Stop and Remove Container (Optional)

```bash
sudo docker stop pcscf-container
sudo docker rm pcscf-container
```

---

### Rebuild After Changes

If you make changes to source code or `Dockerfile`, rebuild the image:

```bash
sudo docker build -t pcscf .
```


---

## Bare Metal Installation

### Step 1: Build the Project
[Refer](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.3.0/IMS/documentation/IOS-MCN%20IMS-pcscf-developer-guide.md)

### Step 2: Prepare Deployment

1. Rename the JAR file and move it to the deployment directory:

```bash
sudo mv cscf/pcscf/target/pcscf-0.0.1.jar /etc/ios-mcn/pcscf.jar
```

2. Create the systemd service file:

Create a new file at `/lib/systemd/system/ios-mcn-pcscf.service` with the required service definition.

Example (adjust paths as necessary):

```ini
[Unit]
Description=IMS P-CSCF Service
After=network.target

[Service]
ExecStart=/usr/bin/java -jar /etc/ios-mcn/pcscf.jar
SuccessExitStatus=143
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
```

### Step 3: Enable and Start Service

Reload systemd to detect the new service:

```bash
sudo systemctl daemon-reload
```

Enable service on boot:

```bash
sudo systemctl enable ios-mcn-pcscf.service
```

Start the service:

```bash
sudo systemctl start ios-mcn-pcscf.service
```

Check the service status:

```bash
sudo systemctl status ios-mcn-pcscf.service
```

If the output includes `Active: active (running)`, the P-CSCF has been successfully deployed and is running.

---

## Final Notes

Ensure the following configurations exist in `/etc/ios-mcn` before running the service:

- `pcscf` (configuration parameters including IP/Port)
- `pcscf-logging.xml` (logging configuration)
- `subscribers.json` (IMSI to MSISDN mapping)

Reference contents are available [here](https://docs.google.com/document/d/1Ek-rYGfBonGcgr0kIi2XRSh-aNQc_R847LkSfficHEs/edit?tab=t.0).
