# **IOS-MCN UNI RAN TROUBLESHOOTING GUIDE**

Introduction
-----
This document provides a comprehensive guide to troubleshooting common issues encountered during the setup and operation of a BareMetal & Dockerized 5G RAN stack, including gNB, LPRU, and IOSMCN-CORE components. Each issue is clearly numbered with real-world symptoms, causes, and actionable solutions.

Purpose and Audience
-----

The purpose of this document is to serve as a structured and practical reference for identifying, diagnosing, and resolving common technical issues encountered during the deployment and operation of 5G RAN environment. The troubleshooting steps outlined provide actionable solutions to address problems efficiently and effectively.

This document is intended for system engineers, integration specialists, and network deployment teams involved in configuring, maintaining, or troubleshooting 5G RAN components including the gNB, LPRU, USRP-based systems, and IOSMCN-CORE. A working knowledge of Linux, Docker, Kubernetes, and radio access network architecture is assumed.


## CPU Core Mapping Reference (Example: 8-Core / 16-Thread CPU)

This section explains how CPU cores are configured for the optimal / Real Time performance of the RAN stack and associated timing/synchronization processes. This table is useful reference for debugging performance bottlenecks, real-time constraints, and thread conflicts.

| **Core ID** | **Purpose**                   | **Notes**                                       |
|-------------|-------------------------------|------------------------------------------------ |
| 2           | PTP Timing Sync               | Used for `ptp4l` and `phc2sys`                  |
| 3, 4, 5, 7  | Thread Pool                   | Possibly mapped dynamically (e.g., via systemd) |
| 6           | Free                          | Available for future assignment                 |
| 10          | `nr-softmodem`                | Main softmodem execution thread                 |
| 11          | L1 Tx Thread                  | Transmit physical layer (L1 parameter)          |
| 12          | L1 Rx Thread                  | Receive physical layer (L1 parameter)           | 
| 13          | FHI 7.2 Worker Core           | Handles RU uplink/downlink processing           |
| 14          | RU Thread Core                | Thread for Radio Unit control                   |
| 15          | IO Core (FHI 7.2 interface)   | Data movement between RU and stack              |


> **⚠️ Note:** Core IDs may differ depending on your CPU topology and hyperthreading. Use tools like `htop`, `taskset`, or `ps -eo pid,psr,comm` to verify during runtime.


I.	BIOS & Virtualization Issues 
----
**Issue #1: VT-d not enabled in BIOS**

**Description** :

PCI passthrough fails

Virtual machines unable to access NICs or accelerators directly

**Solution:**

Reboot system → Enter BIOS (Del/F2) → Advanced → Enable “VT-d”

Save & Exit

**Preventive Tip:** Set BIOS password to avoid accidental disablement

-----

**Issue #2: SR-IOV not working even after BIOS enable**

**Description :**

VFs (Virtual Functions) not visible under lspci

dmesg shows IOMMU or SR-IOV errors

**Causes:**

VT-d is disabled or IOMMU not configured in kernel

**Solution:**

Ensure VT-d is enabled

Update GRUB:

Run command:

```
sudo nano /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="intel_iommu=on iommu=pt"
``` 
```
sudo update-grub && reboot
```

**Check:**
```
lspci | grep -i virtual
```
**Preventive Tip:** Automate kernel param check in provisioning scripts

---

**Issue #3: Running inside VM, incorrect driver, or PCIe NIC not initialized properly.**
**Real-World Example:** 

Tool says *"No supported devices found"* even after download.

**Fix:** 

Boot into bare-metal OS, check with lspci if E810 is detected.

-----

**Issue #4: echo 2 > sriov_numvfs does nothing**

**Fix:**

Check NIC supports SR-IOV: lspci | grep -i e810

Kernel must have intel_iommu=on iommu=pt enabled

Check /sys/class/net/enp2s0f1/device/sriov_totalvfs > 0

-----

**Issue #5: BIOS Misconfiguration Not Actually Applied**

**Description:**

SR-IOV and VTd appear enabled in BIOS, but VFs still won’t create or IOMMU groups aren’t set up.

**Common Solutions:**

- After saving BIOS changes, reset to defaults and re-enable VT-d/SR-IOV to force the update.
- Update your motherboard’s firmware/BIOS to the latest revision.
  
-----

II.	NIC Issues
-----

**Issue #6: E810 NIC not detected / fails to initialize**

**Description :**

```
ip a doesn’t show E810 interfaces
```
```
dmesg | grep e810 shows driver errors
```

**Solution:**

Ensure driver version matches (e.g., 4.2.3)

Reinstall driver:

Run:

```
sudo rmmod ice
```

```
sudo modprobe ice
```

-----

**Issue #7: NIC firmware outdated → reduced performance or link issues**

**Description :**

ethtool shows unstable link status

SR-IOV VFs crash

**Solution:**

Download Intel NVM tool from:
[Intel E810 Firmware Update Tool](https://www.intel.com/content/www/us/en/download/19626/non-volatile-memory-nvm-update-utility-for-intel-ethernet-network-adapters-e810-series-linux.html)

Run update:

```

./nvmupdate64e

Reboot system
```
-----
**Issue #8: Poor throughput / excessive retransmission**

**Description :** Packet drops, jitter in performance tests

**Solution:**

Set FEC to “Auto” or test with “Off” depending on switch compatibility

Use:

```

ethtool --set-fec ethX encoding auto
```
-----
**Issue #9: Adapter link status is down even though cables are plugged**

**Causes:**

DAC cables not supported

Firmware bug

**Solution:**

Replace cable with certified optical module

Re-check link negotiation via:

```
ethtool ethX
```
-----

**Issue #10: E810 interfaces not working even after installing ICE**

**Description :**

No interface under ip link

modinfo ice fails

**Solution:**

Make sure kernel headers match:

``` 
uname -r
```

```
ls /usr/src/linux-headers-*
```

Then compile as per README from:
[Intel ICE Driver Link](https://www.intel.com/content/www/us/en/download/19630/intel-network-adapter-driver-for-e810-series-devices-under-linux.html)

-----

**Issue #11: ICE driver fails with kernel errors**

**Solution:**

Ensure kernel-devel, kernel-headers are installed:

```
sudo apt install linux-headers-$(uname -r)
```

**Issue #12: nvmupdate64e fails or hangs**

**Description :**

Error: "Cannot detect device", "No compatible device found"

**Causes:**

Running inside VM

No root privileges

Wrong tool version

**Solution:**

Boot into bare metal (not VM)

Use tool from:
[Intel NVM Update Tool for E810](https://www.intel.com/content/www/us/en/download/19626/non-volatile-memory-nvm-update-utility-for-intel-ethernet-network-adapters-e810-series-linux.html)

Run as root:
```
sudo ./nvmupdate64e
```

-----
**Issue #13: NVM tool doesn't list NIC**

**Solution:**

Confirm with:

```

lspci | grep -i ethernet

ethtool -i <interface>

Check ice driver is loaded and compatible version
```
**Issue #14: ICE driver doesn’t match the kernel headers (especially real-time kernel).**

**Symptom:** Interface errors, NIC doesn’t initialize or ethtool fails.

**Fix:** Rebuild ICE driver after confirming kernel version:    

```

uname -r

dkms status
```
-----

**Issue #15: IP link set mtu fails if interface not up**

**Fix:**

```
sudo ip link set enp2s0f1 up
```

```
sudo ip link set enp2s0f1 mtu 8870
```
-----

III.	Ubuntu Pro & Real Time Kernel Issues
-----

**Issue #16: License attach fails**

**Description :**

Error: pro: command not found or license key invalid

**Solution:**

Ensure pro is available:

```
sudo apt install ubuntu-advantage-tools -y
```

Verify internet connectivity

Use the correct license key format from: <https://ubuntu.com/pro>

-----
**Issue #17: pro enable realtime-kernel gives error**

**Description :**

“Package not found” or “unsupported version”

**Solution:**

Only Ubuntu 20.04 or 22.04 Pro versions support realtime kernel

Use:

```

lsb_release -a
```
and check supported versions [on this link]((https://documentation.ubuntu.com/pro/))

**Tip:** After enabling, verify kernel installed:

```
uname -r
```

-----
**Issue #18: Ubuntu Pro license activation didn’t succeed or reboot didn’t switch kernel.**

**Symptom:** uname -r still shows generic kernel instead of realtime.

**Fix:** Run sudo pro status, verify license is active. Then sudo pro enable realtime-kernel and reboot. Also check GRUB is updated.

-----
IV.	Package Management Issues
-----

 **Issue #19: Duplicate installs or missing packages**

**Description :**

Confusion due to repeated commands

**Solution:**

Clean up and install all required packages in a single go:

```
sudo apt install -y linux-tools-common wget xz-utils libnuma-dev stress s-tui tuned build-essential
```

-----
V.	Tuned Profile / Real Time Profile Issues
-----
**Issue #20: tuned-adm profile realtime fails**

**Description :**

No such profile: realtime

**Solution:**

Install tuned-profiles-realtime if missing:

```
sudo apt install tuned tuned-utils tuned-profiles-realtime -y
```

-----
**Issue #21: Reboot resets tuned-adm profile**

**Fix:**

Bash:

```
sudo tuned-adm active  # should return "realtime"
```
-----
VI.	Bootloader & Kernel Parameter Issues
-----
**Issue #22: grub not updated properly**

**Description :**

After reboot, cat /proc/cmdline doesn’t show expected parameters

**Cause:**

Improper escape characters or syntax error in sed command

**Solution:**

Verify /etc/default/grub manually after running sed commands

Then:


```
sudo update-grub
```

```
sudo reboot
```
-----
**Issue #23: VF Not Created / Network Core Doesn’t Exist**

**Description:**  
Attempting to enable SR-IOV via `echo <num> > /sys/class/net/enpXs0fX/device/sriov_numvfs` results in:
- No virtual functions (VFs) created.
- Interface doesn’t respond or no network core detected for offload/bypass functions.

**Root Cause:**  
- The kernel was not booted with the correct IOMMU and SR-IOV support parameters.  
- BIOS settings for **VT-d** or **SR-IOV** may also be disabled.



**Common Symptoms:**
- `/sys/class/net/enpXs0fX/device/sriov_totalvfs` shows `0` or is missing.
- Error: `write error: Invalid argument` when trying to set `sriov_numvfs`.
- `lspci` does not show multiple VFs or virtual functions.

 **Verification Steps:**

Run:
```
cat /proc/cmdline
```


**Issue #24:** CPU isolation affects wrong cores or services

**Description :**

OS unstable or CPU usage uneven

**Solution:**

-Use lscpu to check physical cores

-Modify isolated_cores=2-7,10-15 based on actual NUMA node layout

-----

**Issue #25:** Typo in GRUB config or system didn’t apply hugepages=20 properly.

**Symptom:** 
cat /proc/meminfo | grep Huge shows 0 hugepages.

**Fix:**
Double-check GRUB entry and kernel boot params. Run:

```
grep -i huge /proc/cmdline
```
-----
**Issue #26. Kernel Version Mismatch**

**Description:**
Using a real-time kernel package (e.g. linux-image-5.15.0 rt) that doesn’t align with your tuning scripts or DPDK build can cause strange bind failures or timing drifts.
**Common Solutions:**

- Verify your running kernel with uname -r against the package you installed.
- If mismatched, install the exact version (**sudo apt install linux-image-5.15.0 rt**) and reboot.
-----

VII.	System Daemon & Service Issues
-----

**Issue #27: irqbalance still running after disabling**

**Description :**

top or htop shows irqbalance process

**Cause:**

Service override in systemd

**Solution:**

Ensure complete stop:


```
sudo systemctl stop irqbalance
```

```
sudo systemctl disable irqbalance
```

```
sudo systemctl mask irqbalance
```

Confirm:
```
ps aux | grep irqbalance
```
-----

**Issue #28: Power daemon still auto starts**

**Description :**

Power scaling features still active

**Solution:**

Run:

```
sudo systemctl disable power-profiles-daemon
```
```
sudo systemctl mask power-profiles-daemon.service
```

If required, uninstall:

```
sudo apt remove power-profiles-daemon -y
```
-----
**Issue #29: System auto-updates despite disabling**
**Description :**

Background updates visible in logs

**Solution:**

Stop it completly:

Bash:

```
sudo systemctl disable --now unattended-upgrades
```

```
sudo apt purge unattended-upgrades -y
```
-----
**Issue #30: irqbalance gets re-enabled by user or not fully masked.**
**Fix:** Run:

Bash:

```
sudo systemctl disable irqbalance
```

```
sudo systemctl mask irqbalance
```

-----
**Issue #31. Shared Core Resource Exhaustion**

**Description:**

Non RAN daemons (irqbalance, systemd-timer, unattended-upgrades) creep back onto “isolated” cores, killing realtime performance.

**Common Solutions:**

- Double check tuned-adm active shows your custom “realtime” profile.
- Explicitly mask or disable these services:

```
systemctl disable irqbalance

systemctl mask unattended-upgrades
```
-----

VIII.	VFIO & DPDK Binding Issues
-----
**Issue #32: PCI ID incorrect or driver vfio-pci not loaded**

**Fix:**

Load driver manually:

Bash:

```
sudo modprobe vfio-pci
```

Use dpdk-devbind.py -s to get correct PCI ID before binding

Example output:

Bash:

0000:02:09.0 'DeviceName' unused

-----

**Issue #33: Missing DPDK binding**

**Fix:**

Check with htop whether threads are on isolated cores

Start with simplified thread config:


```
sudo taskset -c 3,4 ./nr-softmodem -O <config.cfg> --sa
```
-----
**Issue #34. DPDK Devbind Binding Error**

**Description:**
```
dpdk-devbind.py --bind vfio-pci <PCI_ADDR> reports “driver not found” or fails to bind.
```
**Common Solutions:**

- Confirm the target PCI address with lspci -nn | grep Ethernet.
- Install the correct DPDK version (20.11.9) and its usertools before running the bind script.
- Unbind any existing driver first:

```

dpdk-devbind.py --unbind <PCI_ADDR>

dpdk-devbind.py --bind vfio-pci <PCI_ADDR>
```
-----

IX.	CPU Frequency & Power Management Issues
-----

**#Issue 35: Setting fixed GHz fails on some platforms**

**Fix:**

You can fall back to:

```
sudo cpupower frequency-set -g performance
```
-----
X.	Build Issues 
-----

**#Issue 36: Wrong rpath path or binary permission denied**

**Fix:**

Make sure you give full absolute path:

```
sudo patchelf --set-rpath ~/IOSMCN-RAN-Source/<path-to-the-executable/ nr-softmodem
```

Check file is executable: chmod +x nr-softmodem

Check with **ldd nr-softmodem** which it finds all .so files

-----

**#Issue 37: meson version incompatible or system lacks dependencies**

**Fix:**

Use python3.8+ for meson, verify with:

Bash:

python3 --version

pip install meson

Sometimes meson build fails if pkg-config or libnuma-dev is missing.

-----

**#Issue 38: nr-softmodem fails with lib.so: cannot open shared object file**

**Fix:**

Export LD_LIBRARY_PATH:

Bash:

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/username/v.0.0.2.baremetal/
```

Or copy all .so to /usr/local/lib and run:

Bash:

```
sudo ldconfig
```

-----
**Issue #39. DPDK Version Incompatibility**

**Description:**
Upgrading to a newer DPDK (e.g. v21+) without rebuilding your OAI libraries leads to ABI errors or softmodem crashes.
**Common Solutions:**

- Always build OAI against the exact DPDK release you install (check the Meson dpdk.version setting).
- If you must upgrade, rerun meson setup build && ninja -C build install.
-----
XI.	SDR Hardware Issues
-----

**Issue #40.USRP B210 Not Detected**

**Description:**
nr-softmodem or Docker container reports “No USRP devices found” when using a B210 over USB.
**Common Solutions:**

- Ensure the B210 is plugged into a **USB 3.0** port (not 2.0).
- Verify the device is listed:

``` 
lsusb | grep Ettus
```
- Install/verify UHD drivers and permissions (e.g. add udev rule for Ettus).

-----

**Issue #41. USB Bandwidth Saturation (USRP)**

**Description:**
Your B210 shows underruns or high RX latency because another USB device is hogging the same bus.

**Common Solutions:**

- Move the USRP to a dedicated USB 3.x root port or PCIe to USB card.
- Disconnect non critical USB peripherals during RAN tests.
-----

XII.    Radio Unit (RU) Issues
-----

**Issue #42: Power daemon still auto starts**

**Description :**

Power scaling features still active

**Solution:**

Run:
```
sudo systemctl disable power-profiles-daemon
```

```
sudo systemctl mask power-profiles-daemon.service
```

If required, uninstall:

```
sudo apt remove power-profiles-daemon -y
```
-----
**Issue #43: System auto-updates despite disabling**

**Description :**

Background updates visible in logs

**Solution:**

Stop it completely.

```
sudo systemctl disable --now unattended-upgrades
```

```
sudo apt purge unattended-upgrades -y
```

-----

**Issue #44: ptp4l / phc2sys Permission Denied**

**Description:**
Scripts phc2sys-master.sh or ptp4l abort with permission errors.

**Common Solutions:**

- Run as **root** or grant the binary CAP_NET_ADMIN / CAP_SYS_TIME via:

```
sudo setcap cap_net_admin,cap_sys_time+ep /usr/sbin/ptp4l
```

- Ensure /dev/ptpX exists and is owned by root.
-----

**Issue #45: XML MIMO Config Syntax Error**

**Description:**
xml_parser e_2x2.xml exits with “malformed XML” or your RU never activates the carrier.

**Common Solutions:**

- Run **xmllint** --**noout** **e_2x2.xml** to pinpoint line/column errors.
- Compare against a known-good sample and ensure all <antenna> tags are closed.

-----

**Issue #46: RU Memory**
Write Command Rejection

**Description:**
The command below fails with “permission denied” or “invalid address.”

```
mw.l a0010024 1919
```

**Common Solutions:**

- Ensure you’re **root** on the RU (ssh root@192.168.4.50) before issuing mw.l.
- Double check the PHY register address in your e_2x2.xml matches what the RU expects—some builds use a0010024 instead.
-----
**Issue #47: sysrepocfg Change Doesn’t Activate Carrier**

**Description:**
Running the below command **returns success but the RU still shows carrier “DOWN.”**

```
sysrepocfg --edit=/path/to/e_2x2.xml --datastore=running**
```


**Common Solutions:**

- After sysrepocfg, restart the radio fronthaul service on the RU:

```
systemctl restart radio-fronthaul
```
- Verify the configuration actually loaded:

```
sysrepocfg --xpath="/fronthaul/carrier" --datastore=running
```
-----
**Issue #48: xml_parser Won’t Parse MIMO File**

**Description:**
xml_parser e_2x2.xml exits silently or errors “file not found,” even though it’s in your home directory.
**Common Solutions:**

- Run the parser from the directory where e_2x2.xml lives, or supply an **absolute path**.
- Make the file executable and ensure it has UNIX line endings:

```
chmod +x xml_parser
dos2unix e_2x2.xml
```
-----
**Issue #49: LPRU Not Available or Not Reachable**

**Description:**
The RU (LPRU) doesn’t respond to ping, ssh, or fails to power up entirely.

**Common Solutions:**

- Ensure LPRU is physically powered and connected to the same Layer 2 network as the gNB.

- Check power LEDs on the RU and fronthaul port lights—if absent, verify the PSU or POE injector.

- Double‑check the RU's IP (default: 192.168.4.50) and your host IP is in the same subnet (e.g. 192.168.4.x).

- Use arp -a to verify if the RU's MAC appears; if not, try connecting directly to the RU with a static IP.

-----

**Issue #50: xml_parser Executes But RU Doesn’t Start**

**Description:**

You run xml_parser e_2x2.xml, and it finishes without error, but the RU shows no fronthaul activity.

**Common Solutions:**

- Ensure the parser is executed on the RU itself, not on the gNB.

- Confirm the RU has the correct XML parser binary (some versions are hardware-specific).

- Check that the XML config matches the LPRU’s supported antenna and MIMO layout**.

-----

**Issue #51: No LED Indication for Sync on RU**

**Description:**

Even after running PTP sync scripts, the RU’s front-panel sync LED remains red or off.

**Common Solutions:**

- Double-check that ptp4l is running on the correct interface (e.g. enp2s0f1 for master, enp2s0f0 for slave).

- Re-run phc2sys on the master to push system time to hardware clock.

- Some RUs require a reboot after the initial XML parsing and PTP config.

-----

**Issue #52: Carrier Activation Fails After XML Push**

**Description:**

You successfully edit and push XML using sysrepocfg, but ifconfig shows the fronthaul interface is still down.

**Common Solutions:**

- Verify the RU firmware is compatible with the XML format you used (some LPRUs expect different schema tags).

- Confirm the carrier ID matches expected values in the O-RU backend (carrier0, carrier1, etc.).

- Restart the fronthaul or carrier-management service on the RU.

-----

**Issue #53: SSH Key Authentication to RU Fails**

**Description:**

Attempting to ssh root@192.168.4.50 asks for a password even after you've set up SSH keys.

**Common Solutions:**

- Ensure the public key is added to /root/.ssh/authorized_keys on the RU.

- Check RU SSH config (/etc/ssh/sshd_config) has PubkeyAuthentication yes and restart the SSH service.

- If the key is too new (e.g. ed25519), switch to an RSA‑2048 key for broader compatibility.

-----

**Issue #54: RU Does Not Show Connected Antennas or Ports**

**Description:**

After XML parsing and carrier activation, the RU reports “0 active ports” or fails to show connected antennas.

**Common Solutions:**

- Confirm that the XML configuration file (e_2x2.xml) correctly defines <antenna> and <bandwidth> for each port.

- Physically check antenna cable connections—ensure the correct ports are used for TX/RX and that no loose connectors exist.

- Re-run xml_parser and validate with RU’s internal CLI/logs that the carrier mapping is applied.

-----

XIII.	Containerization / Docker Issues
-----

 **Issue #55: E810 NIC not detected / fails to initialize**

**Description :**

```
ip a #doesn’t show E810 interfaces
```
```
dmesg | grep e810  #shows driver errors
```

**Solution:**

Ensure driver version matches (e.g., 4.2.3)

Reinstall driver
```
sudo rmmod ice
```

```
sudo modprobe ice
```

-----

**#Issue #56: NIC firmware outdated → reduced performance or link issues**

**Description :**

ethtool shows unstable link status

SR-IOV VFs crash

**Solution:**

Download Intel NVM tool from:
[Intel E810 Firmware Update Tool](https://www.intel.com/content/www/us/en/download/19626/non-volatile-memory-nvm-update-utility-for-intel-ethernet-network-adapters-e810-series-linux.html)

Run update:

```
./nvmupdate64e

Reboot system
```
-----
**#Issue #57: Poor throughput / excessive retransmission**

**Description :** Packet drops, jitter in performance tests

**Solution:**

- Set FEC to “Auto” or test with “Off” depending on switch compatibility

Use:

```

ethtool --set-fec ethX encoding auto
```
-----
**Issue #58: Adapter link status is down even though cables are plugged**

**Causes:**

DAC cables not supported

Firmware bug

**Solution:**

- Replace cable with certified optical module

- Re-check link negotiation via:

```
ethtool ethX
```
-----

**Issue #59: Docker Image Version Mismatch**

**Description:**
The gNB container runs an image version (e.g. uni-ran-gnb:1.1) that isn’t compatible with your host scripts or config syntax.

**Common Solutions:**

- Tag/label each Docker image clearly and match your docker-compose.yaml to the correct tag.
- If unsure, run **docker images | grep uni-ran-gnb** and relaunch with the right version.
-----

**Issue #60: usrp_initialstart.sh Fails Inside Docker**

**Description:**

During docker-compose up, the usrp_initialstart.sh script inside the gNB container errors “/usr/bin/env: ‘’: No such file or directory.”

**Common Solutions:**

- Ensure your Dockerfile or image includes **** (not just sh):

```
dockerfile

RUN apt-get update && apt-get install -y 
```

- Mark the script executable and with the correct shebang:

```
chmod +x usrp_initialstart.sh
sed -i '1c#!/bin/' usrp_initialstart.sh
```
-----
**Issue #61: Checking IOSMCN-CORE**

-----
**#61.1: Load the Docker Image**

- **Copying UNI-RAN image tar file:** 

  **Description:** 

  - **Incorrect path to the .tar file**.
  - **Insufficient disk space** on the host machine to store the image.
  - **Corrupted .tar file**.

**Common Solutions**:

- Verify the correct and complete path to the .**tar** file.
- Check disk space on the host machine using commands like and free up space if necessary.
- Re-download or verify the integrity of the .**tar** file if corruption is suspected
- **Loading into Docker (sudo docker load -i /path/to/uni-ran-gnb.tar):** 

  **Description:** 

  - **Docker daemon not running** on the host machine.
  - **Incorrect file path** specified in the command.
  - **Permission issues** for Docker to access the file or load the image.

**Common Solutions**:

- Ensure the Docker daemon is running on the host machine.
- Double-check the file path provided to the docker load command for accuracy.
- Address permission issues to ensure Docker can access the .**tar** file and load the image.
- **Verifying it's loaded (sudo docker images):** 

  **Description:** 

  - The **image not appearing in the list**, indicating that the loading step failed.

**Common Solutions**:

- Re-run the **docker load** command and carefully observe its output for any error messages.
- Check **Docker** **logs** for more detailed information about why the image failed to load. -----

**#61.2: Prepare the Host Environment**

- **Copying config files:** 

**Description:** 

- **Incorrect destination path** for the **usrp gnb config** and **lpru config** files.
- Permissions issues preventing file copy.

**Common Solutions**:

- Verify the correct destination path for the configuration files.
- Use **sudo cp** or adjust directory permissions to allow copying the files.
- **Creating and running usrp_initialstart.sh:** 

**Description:** 

- **Syntax errors within the  script**.
- **Permissions issues** (sudo) preventing the commands from executing.
- **Commands failing to apply system settings**: 
  - **sudo timedatectl set-ntp false**: Issues with time synchronization if not correctly disabled.
  - **sudo sysctl -w net.core.rmem_max=62500000** (and similar for **wmem_max, rmem_default, wmem_default**): **Network buffer settings not applying**, potentially leading to packet loss or reduced performance for high-throughput applications.
  - **sudo sysctl -w net.core.default_qdisc=fq and sudo sysctl -w net.ipv4.tcp_congestion_control=bbr**: **Network queuing and congestion control settings not taking effect**, impacting network latency and throughput.
  - **sudo iptables -P FORWARD ACCEPT** and **sudo sysctl net.ipv4.conf.all.forwarding=1**:  **Firewall or IP forwarding not being correctly configured**, preventing network traffic from flowing between interfaces, which is crucial for routing.
  - **sudo ufw disable**: **UFW (Uncomplicated Firewall) not disabling**, which might still block necessary ports.
  - **sudo cpupower frequency-set and sudo cpupower idle-set**: **CPU power management settings not applying**, leading to the CPU not running at its full potential (e.g., not at 4.70GHz), which can significantly **impact gNB performance and latency**. These commands might also fail if **cpupower** utilities are not installed or if the hardware doesn't support the specified frequencies/idle states.

**Common Solutions**:

- Review the **usrp_initialstart.sh** script for syntax errors and correct them.
- Ensure the script has **execute permissions (chmod + x)** and is run with **sudo.**
- For **timedatectl**: Check time synchronization services and ensure they are compatible with disabling NTP.
- For **sysctl** commands: Verify kernel parameters are supported and not being overridden by other configurations.
- For **iptables** and **ufw**: Ensure these tools are installed and that firewall rules are correctly applied or disabled as intended.
- For **cpupower**: Install **cpupower-utils** if not present. Verify hardware support for specified CPU frequencies and idle states. Check BIOS settings for CPU power management
- 
-----
**#61.3: Create a docker-compose.yaml file**

**Description:** 

- **Syntax errors in the YAML file:** Even a small indentation error can prevent docker-compose from parsing the file.
- **Incorrect image name (oai-gnb:latest)** if the loaded image has a different tag.
- **Missing or incorrect privileged: true or cap_add (SYS_NICE, IPC_LOCK)**: These are crucial for the container to interact with hardware and manage resources, and their absence can prevent the gNB from running or performing optimally.
- **Incorrect ulimits for core**: An invalid setting for core dumps might cause issues.
- **Wrong environment variables** (e.g., USE_B2XX: 'yes') if the hardware setup is different.
- **Incorrect devices mapping (- /dev/bus/usb:/dev/bus/usb)**: If the USRP device is not correctly exposed to the container, it won't be able to communicate with it.
- **Incorrect volumes mapping**: 
  - **Wrong path for /home/ios-mcn/gnb.sa.band78.fr1.106PRB.usrpb210_.conf**: If this path is wrong or the file doesn't exist, the gNB inside the container will not find its configuration file, causing it to fail.
- **Incorrect network_mode: "host"**: This is required for direct network access but can lead to **port conflicts** if the host machine already has services running on the same ports the gNB intends to use.
- **Errors in the command arguments for nr-softmodem**: 
  - **Incorrect path to the configuration file (-O /opt/oai-gnb/etc/gnb.conf) inside the container**.
  - ****Missing or incorrect --RUs..sdr_addrs serial=34414CB:** This is explicitly highlighted as a common error where the **serial number must be changed to the actual USRP serial number**, otherwise the gNB won't find or connect to the SDR hardware.
  - Other command-line arguments might be incorrect or missing, preventing proper **softmodem** operation.
- **Healthcheck configuration issues**: If the test command is incorrect or the interval/timeout/retries are too aggressive, the container might be prematurely deemed unhealthy and restarted or stopped.

**Common Solutions**:

- Validate the **YAML** **file** for syntax errors, paying close attention to indentation.

- Use the exact **Docker image** name and tag that was successfully loaded.

- Ensure privileged: **true and cap_add (SYS_NICE, IPC_LOCK)** are correctly specified as they are crucial for hardware interaction.

- Set appropriate **ulimits** values.

- Correctly define environment variables to match your hardware setup.

- Ensure the USRP device is correctly mapped via devices mapping **(- /dev/bus/usb:/dev/bus/usb).**

- Verify the absolute and correct path for the gNB configuration file in the volumes mapping **(/home/ios-mcn/gnb.sa.band78.fr1.106PRB.usrpb210_.conf).**

- When using **network**_**mode**: "**host**", identify and resolve any port conflicts with other services running on the host.

- CRITICAL: Change **--RUs..sdr_addrs serial=34414CB** to the actual serial number of your USRP device. Verify the USRP is detected by the host system (e.g., **using lsusb** or **uhd_find_devices)**

- Review all **nr-softmodem** command-line arguments for accuracy and completeness.

- Adjust healthcheck **interval, timeout, and retries** if the gNB takes longer to start, and ensure the test command accurately reflects its readiness. -----

----
**#61.4: Launch the Container**

- Running **docker-compose up | tee output.txt:** 

**Description:** 

- **Docker daemon not running** or being in an unhealthy state.
- **docker-compose command not found** or not installed.
- **Errors in the docker-compose.yaml file** preventing the containers from starting.
- **Container crashing immediately after launch** due to internal application errors (e.g**., nr-softmodem failing to initialize**).
- **Resource limitations** on the host machine (CPU, RAM) preventing the container from running stable.
- **Port conflicts** if another process on the host is using a port required by the gNB, especially with **network_mode: "host**".

**Common Solutions**:

- Ensure the Docker daemon is running and healthy **(sudo systemctl status docker).**
- Install **docker-compose** if it's not found on the system.
- Correct any remaining errors in the **docker-compose.yaml** file.
- Monitor container logs (**docker-compose logs or docker logs <container_name>**) to diagnose immediate crashes or internal application errors.
- Check resource utilization (CPU, RAM) on the host machine and ensure sufficient resources are available for the container.
- Identify and resolve port conflicts by stopping conflicting services or modifying gNB port configurations, especially when using **network_mode: "host"**

-----
**Issue #62. Docker Compose Launch Errors**

**Description:**
```
docker-compose up fails with permission or volume errors, or container immediately exits.
```
**Common Solutions:**

- Ensure the UNI
RAN image is loaded:

```
sudo docker load -i uni-ran-gnb.tar

```
- Check that host paths in volumes: (e.g. config files) exist and are readable by Docker’s user.
- Confirm network_mode: "host" and privileged: true are set so USB and NICs are accessible.

----

XIV.	Interfacing Core
-----

**Issue #63:** tuned-adm profile realtime fails

**Description :**

No such profile: realtime

**Solution:**

Install tuned-profiles-realtime if missing:

```
sudo apt install tuned tuned-utils tuned-profiles-realtime -y
```

-----

**Issue #64:** grub not updated properly

**Description :**

After reboot, cat /proc/cmdline doesn’t show expected parameters

**Cause:**

Improper escape characters or syntax error in sed command

**Solution:**

Verify /etc/default/grub manually after running sed commands

Then:
```
sudo update-grub
```

```
sudo reboot
```
-----

**Issue #65. UE Attach/Call Flow Stalls**

**Description:**
Logs show the UE sends Attach Request but no Attach Accept arrives.

**Common Solutions:**

- Confirm gNB has properly established the SCTP association to the AMF (UDP 38412).
- Check firewall rules for SCTP/TCP ports between gNB and core.
- Validate that the AMF pod in Kubernetes is **Running** and service is exposed (**kubectl get pods -A / kubectl get svc -n iosmcn -o wide**).

-----

XV.	Interfacing gNB
-----

**Issue #66:** E810 interfaces not working even after installing ICE

**Description :**

No interface under ip link

modinfo ice fails

**Solution:**

Make sure kernel headers match:

```
uname -r
```

```
ls /usr/src/linux-headers-*
```

Then compile as per README from:
[Intel ICE Driver Link](https://www.intel.com/content/www/us/en/download/19630/intel-network-adapter-driver-for-e810-series-devices-under-linux.html)

-----

**Issue #67:** ICE driver fails with kernel errors

**Solution:**

Ensure kernel-devel, kernel-headers are installed:

```
sudo apt install linux-headers-$(uname -r)
```

-----

**Issue #68:** irqbalance still running after disabling

**Description :**

top or htop shows irqbalance process

**Cause:**

Service override in systemd

**Solution:**

Ensure complete stop:

```
sudo systemctl stop irqbalance
```

```
sudo systemctl disable irqbalance
```

```
sudo systemctl mask irqbalance
```

Confirm:

```
ps aux | grep irqbalance
```
-----

**Issue #69. Incorrect AMF/NGAP IP Configuration**

**Description:**
After startup, UE attach fails or gNB never registers with AMF.

**Common Solutions:**

- In your gNB conf, set both GNB_IPV_ADDRESS_FOR_NG_AMF and GNB_IPV_ADDRESS_FOR_NGU to your gNB’s IP (e.g. 192.168.108.149).
- Verify reachability:

```Bash:
ping <AMF_IP>
```
- Inspect gNB logs for NGAP errors.
-----

**#70. Checking gNB Configuration and Running the gNB**

- **Changing AMF IP in the gNB config file (test-xx.conf):** 

 **Description:** 

  - **Typographical errors** when entering the AMF Cluster IP.
  - **Incorrect AMF IP** obtained in the previous step, leading to the gNB being unable to connect to the AMF.
  - Permissions issues preventing modification or saving of the configuration file.

**Common Solution**:

- Carefully review the AMF Cluster IP for any typographical errors.
- Re-verify the correct AMF IP from the core network to ensure accuracy before entering it into the configuration file.
- Address permissions issues: Use sudo or modify file permissions to allow editing and saving the test-xx.conf file. 
- -----
- **Setting GNB_IPV_ADDRESS_FOR_NG_AMF and GNB_IPV_ADDRESS_FOR_NGU:** 

  **Description:** 

  - **Using the wrong IP address for the gNB Machine** (e.g., not 192.168.x.x if that's not the gNB's actual IP). This would prevent communication between the gNB and the core network functions.
  - Network misconfigurations on the gNB machine itself, such as incorrect subnet masks or gateways.

**Common Solutions**:

- Verify the actual IP address of the gNB machine and ensure GNB_IPV_ADDRESS_FOR_NG_AMF and GNB_IPV_ADDRESS_FOR_NGU are set to this correct IP.
- Check and correct network misconfigurations on the gNB machine, including subnet masks, default gateways, and routing tables. (This information about routing tables is not from the sources) 
- -----

- **Running the nr-softmodem (sudo taskset -c 10 ./nr-softmodem ...):** 

  **Description:** 

  - **Incorrect path to the nr-softmodem executable or the configuration file (./test-sd-latency-optimized.conf)**.
  - **CPU core 10 not being available or sufficient for the process**, leading to performance issues or the softmodem failing to start.
  - **Missing dependencies** for the nr-softmodem executable.
  - **Configuration file errors** (e.g., invalid parameters, missing required sections).
  - **Permission issues** (sudo) preventing the command from executing with the necessary privileges.
  - **Resource limitations** (memory, CPU) on the machine where the softmodem is running, causing it to crash or perform poorly.

**Common Solutions**:

- Verify the full and correct path to the nr-softmodem executable and its configuration file.
- Check CPU core availability and usage and adjust the taskset -c argument to an available and suitable CPU core if core 10 is not sufficient or available.
- Install any missing dependencies required by the nr-softmodem executable.
- Review the configuration file for errors, such as invalid parameters or missing sections.
- Ensure correct sudo usage and that the user has the necessary privileges to execute the command.
- Monitor system resources (CPU, memory) and address any limitations that might be causing the softmodem to crash or perform poorly.
-  -----

XVI.	IOSMCN-CORE / Kubernetes Issues
-----

**Issue #71:** CPU isolation affects wrong cores or services

**Description :**

OS unstable or CPU usage uneven

**Solution:**

Use lscpu to check physical cores

Modify isolated_cores=2-7,10-15 based on actual NUMA node layout

-----
**Issue #72:** Nothing changes post update

**Description :**

Tool shows "No update required"

**Explanation:**

Expected for re-runs — this is a **one-time update** unless:
-Hardware is replaced
-Intel releases critical security patch

-----
 **Issue #73: kubectl Commands Return “Not Found”**

**Description:**
On your IOSMCN-CORE box, kubectl get svc -n iosmcn shows “Error from server (NotFound): namespaces “iosmcn” not found.”

**Common Solutions:**

- Confirm you’re using the correct **KUBECONFIG** (e.g. /etc/kubernetes/admin.conf):

```
export KUBECONFIG=/etc/kubernetes/admin.conf
```
- If the iosmcn namespace really isn’t there, reapply the core manifests:

```
kubectl apply -f core-deployment.yaml
```
-----

**Issue #74: Accessing the IOSMCN-CORE server via SSH:** 

**Description:** 

- Incorrect IP address (192.168.x.x), **Wrong username or password** for administrator.

**Common Solutions:**

- Verify and use the correct IP address for the IOSMCN-CORE server. Confirm and use the correct username and password for the administrator.

**Description:**

- Network connectivity issues preventing the SSH connection (e.g., firewall blocking port 22, server being offline).

**Common Solutions:**

- Check network connectivity: Ensure the server is online, firewall rules allow SSH (port 22). You might use ping or traceroute to diagnose connectivity issues. Ensure the SSH service is running on the IOSMCN-CORE server. 
- -----
**Issue #75: Watching pod status (watch -n 1 kubectl get pods -A):** 

**Description:** 

- **Kubernetes cluster issues** where pods are not starting or are in CrashLoopBackOff, Error, or Pending states instead of Running.

**Common Solutions:**

- For **Pod** **status** issues: Inspect pod logs **(kubectl logs <pod-name> -n <namespace>)** and describe pods **(kubectl describe pod <pod-name> -n <namespace>)** to understand why they are not running.

**Description:**

- **kubectl** command not found or not configured correctly on the SSH machine; 
- **Permissions** issues preventing the **kubectl** command from accessing cluster information.

**Common Solutions**:

- For **kubectl** command issues: Ensure kubectl is installed and properly configured on the SSH machine, verifying that it can connect to the Kubernetes cluster.
- For **permissions** issues: Verify that the user has the necessary Role-Based Access Control (RBAC) permissions to execute **kubectl** commands and access cluster information. -----
-----
**Issue #76: Verifying Service Status**
- **Running kubectl get svc -n x -o wide:** 

  **Description:** 

  - **Incorrect namespace (-n x)**. The example uses iosmcn but it states -n x, indicating it's a placeholder. Using the wrong namespace will not show the services needed for verification.

**Common Solutions:**

- Use the correct namespace: Replace **-n x** with the actual namespace, -----

**Description:** 

- **Services not running or in an unhealthy state**, which would be indicated by the output of this command, showing missing services or incorrect CLUSTER-IP/EXTERNAL-IP.
- Network configuration issues preventing services from being correctly exposed or accessed.

**Common Solutions:**

- **Check associated pod status**: If services are missing or unhealthy, examine the status of the underlying pods that the services are supposed to expose.
- **Review network configurations**: Ensure firewall rules are not blocking ports and that network policies are correctly configured to allow service exposure and access.
 -----
XVII.	Network & Security Issues
-----

**Issue #77. Cloud/VM Security Group Blocking**

**Description:**
In virtual/cloud setups, UDP 319/320 (PTP) or SCTP 38412 (NGAP) are silently dropped by firewall rules.
**Common Solutions:**

- Inspect your cloud security-group or iptables rules and explicitly allow PTP and SCTP ports.
- Use **ss -u -a | grep 319** or **ss -sctp** to confirm sockets are listening.
-----

XVIII.	Common Troubleshooting
-----

**Issue  #78:** NVM tool doesn't list NIC

**Solution:**

Confirm with:

```Bash:

lspci | grep -i ethernet

ethtool -i <interface>

Check ice driver is loaded and compatible version
```
-----
**Issue #79:** Nothing changes post update

**Description :**

Tool shows "No update required"

**Explanation:**

Expected for re-runs — this is a **one-time update** unless:

Hardware is replaced

Intel releases critical security patch

-----




