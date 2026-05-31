.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

Network Function Orchestration (NFO)
====================================

Introduction
------------
The primary role of the NFO is to provide for the lifecycle management of the cloud deployments for th 5G NFs.


Deployment of RAN-Distributed as Docker Containers (USRP ONLY)
--------------------------------------------------------------

Go to the repo nfo/docker/ran-distributed. To perform the gNB Configuration the Target File is nfo/docker/ran-distributed/.env. Please do following configurations depending on your environment

Configuration: Common across all 3 (CUCP, CUUP, DU)
***************************************************
MCC and MNC should be set according to the values configured in Core.


Configuration: Common across all CUs
************************************
Update NIC_IP_AMF - This is the gNB Host IP address of the Interface connecting to the AMF.

Configuration: Specific to CUCP
*******************************
CUCP_AMF_IP: AMF_IPV4 and IPV6 should be set with the AMF. If AMF is running in the K8S Cluster, then considering the existence of SCTPLB, the Node-IP of the cluster can be used.

Configuration: Specific to CUUP
*******************************
NIC_IP_NGU - IP of the Ng interface - It's the IP of the CU system itself, and it can be same IP as the gNB System IP.

Configuration: Specific to DU
*****************************
NONE.

Configuration: O1-Adapter-Settings
**********************************
1. NETWORK_HOST: Host IP where O1 adapter settings.
2. USERNAME/PASSWORD: Credentials of the Host where O1 adapter is running.
3. TELNET_HOST; Host where gNB is running
4. VES_URL: URL to reach VES-Collector.

gNB Deployment
**************

```
./conf-update.sh
docker compose -p gNB -f docker-compose.yaml up -d
```

gNB Teardown
************
```
docker compose -p gNB -f docker-compose.yaml down
```

Deployment of SD-Core on Kubernetes Cluster
-------------------------------------------
This section is derived from the documentation provided by SD-Core. The repo to use is: ios-mcn-smo/nfo/kubernetes/aether-5gc.

The 5gc repository builds a standalone Aether core with a physical RAN setup.
It depends a k8 cluster which can be deployed using k8 repository that can help to create a multi-node cluster.

To set up the 5gc repository, you need to provide the following:

1. Node configurations with IP addresses in the host.ini file.
   - You can specify both master and worker nodes.
2. Aether configuration parameters, such as RAN_Interface, in the ./var/main.yaml file.


Step-by-Step Installation
*************************

To install the 5g-core, follow these steps:

1. Set the configuration variables in the vars/main.yaml file.
    * Set the "standalone" parameter to deploy the core independently from roc.
    * Specify the "data_iface" parameter as the network interface name of the machine.
    * Set the "values_file" parameter:
        * Use "sdcore-5g-values.yaml" for a stateful 5g core.
        * Use "hpa-5g-values.yaml" for a stateless 5g core.
    * The "custom_ran_subnet" parameter if left empty, core will use the subnet of "data_iface" for UPF.
2. Add the hosts to the init file.
3. Run `make ansible`.
4. In the running Ansible docker terminal:
    * Make sure you have dployed a k8 cluster using `k8s-install` from k8s repo.
    * run `make 5gc-install`
    * It creates networking interfaces for UPF, such as access/core, using `5gc-router-install`.
    * Finally, it installs the 5g core using the values specified in `5gc-core-install`.
        * The installation process may take up to 3 minutes.

One-Step Installation
*********************
To install 5gc in one go, run `make 5gc-install`.

Uninstall
*********
   - run `make 5gc-uninstall`
