
# **IOS MCN v0.1.0 Agartala Release** **User Guide: IOSMCN-Core v0.1**

## Introduction

The guide describes to use the management and monitoring of IOSMCN-Core platform, run the emulated UE provided with the core and connect UEs to core. Bandwidth between UEs can be tested for evaluating the performance of core.

## Purpose and Audience

This document is to access the IOSMCN-Core management interface, connect simulated gNB and provision subscribers

## IOS MCN Test Information

This IOSMCN-Core is tested with 4 core CPU and 16GM RAM systems with Ubuntu 22.04 operating systems running on intel 64-bit platform.

##  Supported Features

The core supports the management interface to access the system. It allows to connect emulated RAN, provisioning of subscribers from simulator or real UEs.

##  Supported Hardware

Intel IA64 platforms with minimum of 4 core CPU and 16GB RAM

## How to use the features

###  Feature 1: Access management interface

1. Configuration/Setup: Identify the IP address on the IOSMCN-Core installed machine. Also install any browser for accessing the management interface URL.

2. How to test: Open the browser and navigate to http://<server_ip>:31194 and http://<server_ip>:30950

###  Feature 2: Run emulated RAN test

1. Configuration/Setup: The IOSMCN-Core software includes emulated RAN for testing.

2. How to test: Run the RAN using the command ‘make aether-gnbsim-run’. It will be attached to IOSMCN-Core

###  Feature 3: Provisioning subscribers

1. Configuration/Setup: This requires the modification of a yaml configuration file. Update ‘subscribers’  block in the ‘sdcore-5g-values.yaml’ for IMSI, OPc, and Key values of SIM cards

2. How to test: Connect UE with the provisioned SIM and observe the device is connected with the IOSMCN-Core. Verify the upload and download speed using test application.

##  How to use connect the supported hardware

###  Device 1: UE 1

1. Configuration/Setup: Identify the IMSI, OPc and key value of SIM to be connected with IOSMCN-Core. Then update ‘subscribers’ in IOSMCN-Core provision module.

2. How to test: Insert SIM on UE and turn ON/flight mode OFF. Observe the connection to the IOSMCN-Core network

###  Device UE 2:

1. Configuration/Setup: Flash SIM with IMSI, OPc and key value on the SIM and update the subscriber information on core.

2. How to test: Insert SIM on UE and turn ON/flight mode OFF. Observe the connection to the IOSMCN-Core network. Check the bandwidth of connectivity.

## Related Artifacts & links

| **Document Name** | **Purpose** | **Link** |
|--|--|--|
| Installation Guide | Installation of IOSMCN-Core | [Click here](./Installation%20Guide.md) |
| Troubleshooting Guide  | Troubleshooting guide for IOSMCN-Core | [Click here](./Troubleshooting%20Guide.md)|
| API Guide | API guide | [Click here](./API%20Guide.md)|
| Developer Guide | Guide for IOSMCN-Core developers | [Click Here](./Developer%20Guide.md)|
















