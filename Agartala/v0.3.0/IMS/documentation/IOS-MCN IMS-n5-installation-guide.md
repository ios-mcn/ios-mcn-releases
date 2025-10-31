
# Installation Guide – N5 Interface v0.3.0

This guide will help you install and run the **IOS-MCN-N5 v0.3.0** using Docker. The interface is fully containerized, allowing fast deployment and easy integration into any 5G Core testbed or system.

---

## Prerequisites

- Docker installed on your system.  
- Already built `n5-service` image [Refer here](./n5-developer-guide.md)

---

## Step 1: Run the Container

Start the container using the following command:

```bash
sudo docker run -d --name n5-container -p 8080:8080 n5-service
```

> Ensure that port `8080` is available on your system. If needed, change the mapping as required.

---

## Step 2: Verify

To verify the container is running:

```bash
sudo docker ps
```

You should see `n5-container` in the running list.

To check logs:

```bash
sudo docker logs -f n5-container
```

---

## Stop and Remove Container (Optional)

```bash
sudo docker stop n5-container
sudo docker rm n5-container
```

---

## Rebuild After Changes

If you make changes to source code or `Dockerfile`, rebuild the image:

```bash
sudo docker build -t n5-service .
```
