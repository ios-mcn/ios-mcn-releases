# IOS-MCN-RAN

The **IOS-MCN RAN** project provides a robust, high-performance, and easily deployable 5G Radio Access Network (RAN) built using open-source components. This repository includes the required Git submodules for setting up a complete RAN based on OpenAirInterface5G (OAI), supporting integration with a Service Management and Orchestration (SMO) component via the O1 adapter, and a fronthaul interface library for PHY layer connectivity. The flexRIC submodule included in the OAI repository also enables E2 interface support.


This document guides you through building and installing the RAN components.
- [Overview](#overview)
- [Installation - Bare metal](#installation---bare-metal)
  - [Building the Project](#building-the-project)
  - [Installing the Project](#installing-the-project)
  - [Uninstalling the Project](#uninstalling-the-project)
  - [Available targets](#available-targets)
- [Containerized Deployment](#containerized-deployment)
- [Related Documentation](#related-documentation)

For instructions on running the components and setting up the environment, refer to the [User guide](IOS-MCN%20RAN-DIS%20User-guide.md)

## **Overview**

The IOS-MCN RAN enables seamless integration between the RAN, RIC (near-RT and non-RT), and fronthaul interfaces for efficient 5G network operations. The repository includes:

- **OAI RAN (OpenAirInterface5G)**: Implements RAN functionality. By default, it supports integration with O-RAN compliant split 7.2 radios. Detailed documentation can be found here [ORAN_FHI7.2_Tutorial](./IOS-MCN%20RAN-DIS%20ORAN-FHI7.2-Tutorial.md)
- **O1 Adapter**: Facilitates communication between the RAN and SMO via the O1 interface. Documentation: [O1-Adapter](https://gitlab.eurecom.fr/oai/o1-adapter)
- **Fronthaul Interface Library (PHY)**: Provides support for PHY layer fronthaul connectivity, enabling communication with remote radio units. Documentation: [o-ran-sc-o-du](https://docs.o-ran-sc.org/projects/o-ran-sc-o-du-phy/en/latest/Architecture-Overview_fh.html)

## **Installation - Bare metal**
### **Dependency:**

**System Requirement:**
- **Ubuntu 22.04 LTS** (required)
- **Fresh installation of the OS** (recommended)

To install all required system dependencies, run:
```
./build_ran --dependency
```
### **Building the Project**

Download the source from: [source-code](https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.4.0/RAN/source-code/)</br>
Untar the release-image and navigate to ios-mcn-ran folder:
```bash
tar -xvf ios-mcn-ran-0.4.0.iosmcn.ran.tar.gz
cd ios-mcn-ran
```
To build the RAN project from source:
>⚠️**NOTE:** This step is required only if you are building from source. If you downloaded a prebuilt package from the releases, this step can be skipped.
```
./build_ran --uhd
./build_ran --xran
./build_ran --ran
```
This will compile split 8 and split 7.2 compliant RAN components. The build process also creates appropriate directories for storing binaries and libraries.

The build process also creates appropriate directories for storing binaries and libraries.

### **Installing the Project**

Download the baremetal release image from: [release-image](https://github.com/ios-mcn/ios-mcn-releases/tree/main/Agartala/v0.4.0/RAN/release-images/RAN-DIS)</br>
Untar the release-image and navigate to ios-mcn-ran folder:
```bash
tar -xvf ios-mcn-ran-dis-baremetal-v0.4.0.tar.gz
cd ios-mcn-ran
```
To install the compiled binaries and libraries to system directories, run:
```bash
./build_ran --install
```
By default:
- Binaries are installed to: /usr/local/bin
- Libraries are installed to: /usr/local/lib

The system’s dynamic linker cache is also updated.
You can modify the installation paths via environment variables in `./scripts/.env` under ios-mcn-ran folder.
Refer to the [User guide](./IOS-MCN%20RAN-DIS%20User-guide.md) for details on launching RAN components. <br>
Helper scripts are also available here: [Helper](./IOS-MCN%20RAN-DIS%20scripts-README.md)

### **Uninstalling the Project**

To uninstall the RAN components from the system:
```
./build_ran --uninstall
```
This removes all installed binaries and libraries.

### **Available Targets**

The build_ran script supports the following targets:

- --all: Build all components (RAN, O1 adapter, E2 and fronthaul interface).
- --dependency: Install all necessary dependencies.
- --dpdk: Install the DPDK dependency only.
- --install: Install the built binaries and libraries to system directories.
- --uninstall: Uninstall the previously installed binaries and libraries.
- --xran: Build and install XRAN libraries.
- --ran: Build RAN for split 7.2,split 8, including CU-UP.
- --o1-adapter: Build the O1 adapter binary.
- --e2-agent: Build RAN with E2 interface.
- --clean: Remove all build artifacts.
- --help: Display available targets and usage information.

For a complete list of available Makefile targets, run:
```
./build_ran --help
```

## Containerized deployment

**System Requirement:**
- **Ubuntu 22.04 LTS** (required)
- **Fresh installation of the OS** (recommended)
- **Docker version 26.1.3**

### Building the docker images
Only pulling the docker images is added in this document for now. The steps to build the docker images will be added in the future releases.

### Pull the Docker Images
This version of the IOS-MCN-RAN also comes with a containerized way of deploying Radio Access Network using docker. Different ways of deployment can be found in cicd folder in ios-mcn-ran, configure the respective .env files in the respective deoployment,
The docker images can be downloaded from here: [Dcoker images](https://github.com/orgs/ios-mcn/packages?tab=packages&q=dis+)

For example:
```bash
docker pull ghcr.io/ios-mcn/ios-mcn-gnb-dis:v0.4.0 # Similarly for CU-UP and adapter-gnb(For O1 interface)
```

For more details on modifying the configuration for deployment, follow: [User Guide](./IOS-MCN%20RAN-DIS%20User-guide.md).<br/>
For the commands to bring up and bring down the containers, follow: [User Guide - Containerized Deployment](./IOS-MCN%20RAN-DIS%20User-guide.md#containerized-deployment)

## Related Documentation:
For instructions on running the components, refer to the [User guide](./IOS-MCN%20RAN-DIS%20User-guide.md).<br>
For more details on development, Please refer the [Developers guide](./IOS-MCN%20RAN-DIS%20developer-guide.md).<br>
Troubleshooting guide shared for the issues faced. [Troubleshooting](./IOS-MCN%20RAN-DIS%20Troubleshooting-guide.md).
