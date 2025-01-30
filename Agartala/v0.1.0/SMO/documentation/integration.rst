.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

.. contents::
   :depth: 3


Post-Deployment Integration: OAM & NON-RT-RIC
=============================================

OAM
---
OAM integrates with almost all the network functions in southbound. Below list summarizes these integrations.

1. Integration with VES-Collector. gNB's O1-adapter must be configured with IP address of the OAM system and the port number 8080, to send O1 messages.
2. gNBs and RUs can be configured with the IP address of the OAM system for any netconf callhome-based connectivity.
3. For sending logs to OAM, please run fluentd in your setup. You can use reference `docker-compose.yaml <https://github.com/ios-mcn-smo/nfo/blob/main/docker/ran-distributed/docker-compose-logging.yaml>`_ and  `configuration <https://github.com/ios-mcn-smo/nfo/tree/main/docker/ran-distributed/config/fluentd>`_
4. To get Core performance metrics.
    a. Get the kubeconfig file and store it in the standard location (~/.kube).
    b. Run read-core-cluster.py in the scripts folder.
    c. Check the influxdb GUI - you should be able to see the Core performance metrics.
5. For Northbound interaction with the OAM, please refer to the :ref:`oam_interfaces`.
