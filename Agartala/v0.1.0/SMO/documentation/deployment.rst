.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

Deployment
==========

OAM Components are deployed in different context and for different use cases.
The main OAM Components are:

- OAM-Controller from ONAP SDN-R using OpenDaylight for O1-NETCONF and OpenFronthaul-Management-NETCONF support.
- VES-Collector from ONAP DCAE for processing O1-VES messages.
- Message-router from ONAP DMaaP using Kafka
- Identity service from Keycloak for AAA support.


This page focus on a lightweight deployment using docker-compose on an Ubuntu system for experience with SMO OAM Components and/or development.


Prerequisites
-------------

The following command are used to verify your system and it installed software package.
In general new version then display here should be fine.::

   $ cat /etc/os-release | grep PRETTY_NAME
   PRETTY_NAME="Ubuntu 20.04.2 LTS"

   $ docker --version
   Docker version 20.10.7, build 20.10.7-0ubuntu1~20.04.2

   $ docker-compose version
   docker-compose version 1.29.1, build c34c88b2
   docker-py version: 5.0.0
   CPython version: 3.7.10
   OpenSSL version: OpenSSL 1.1.0l  10 Sep 2019

   $ git --version
   git version 2.25.1

Please ensure you have keytool support, which comes with JRE, in your system.
If keytool is not found - refer this `stackoverflow-query <https://stackoverflow.com/questions/16333635/keytool-error-bash-keytool-command-not-found>`_

The communication between the components bases on domain-names. For a lightweight
deployment on a single laptop or virtual-machine the /etc/hosts file should be
modified as a simple DNS.

Please modify the /etc/hosts of your system.

* \<host-name>: Hostname of your system. Ex: smo

* \<your-system>: is the combination of hostname and domain-name. Ex: smo.iosmcn.org

* \<deployment-system-ipv4>: is the IP address of the system where the solution will be deployed

For development purposes <your-system> and <deployment-system> may reference the same system.::

   $ cat /etc/hosts
   127.0.0.1	               localhost
   127.0.1.1	               <host-name>
   # SMO OAM development system
   <deployment-system-ipv4>                   <your-system>
   <deployment-system-ipv4>           gateway.<your-system> 
   <deployment-system-ipv4>          identity.<your-system>
   <deployment-system-ipv4>          messages.<your-system>
   <deployment-system-ipv4>      kafka-bridge.<your-system>
   <deployment-system-ipv4>         odlux.oam.<your-system>
   <deployment-system-ipv4>         flows.oam.<your-system>
   <deployment-system-ipv4>         tests.oam.<your-system>
   <deployment-system-ipv4>    controller.dcn.<your-system>
   <deployment-system-ipv4> ves-collector.dcn.<your-system>

Docker Enable IPv6
^^^^^^^^^^^^^^^^^^

The O-RAN Alliance specifications target the support of IPv6.
To support IPv6 by docker the docker configuration must be modified.

Please see:
https://docs.docker.com/config/daemon/ipv6/

1. Edit /etc/docker/daemon.json, set the ipv6 key to true and the fixed-cidr-v6 key to your IPv6 subnet. In this example we are setting it to 2001:db8:1::/64.

.. code-block:: json

  {
      "dns": ["1.1.1.1"],
      "registry-mirrors": [
          "https://nexus3.o-ran-sc.org:10002",
          "https://nexus3.onap.org:10001"
      ],
      "log-driver": "json-file",
      "log-opts": {
          "max-size": "10m",
          "max-file": "3"
      },
      "ipv6": true,
      "fixed-cidr-v6": "2001:db8:1::/64"
  }

2. Reload the Docker configuration file.

.. code-block:: bash

  $ systemctl reload docker

It is beneficial (but not mandatory) adding the following line add the
end of your ~/.bashrc file. I will suppress warnings when python script
do not verify self signed certificates for HTTPS communication.::

   export PYTHONWARNINGS="ignore:Unverified HTTPS request"

Usage
-----

Bring Up Solution
^^^^^^^^^^^^^^^^^

Run the below command first to prepare the .env file::

   python3 adapt_to_environment.py --i <IP-ADDR-OF-THE-SYSTEM> --d <HOSTNAME.DOMAINNAME>
   python3 adapt_to_environment.py --i 192.168.0.100 -d smo.iosmcn.org

Then, just run: ::

   ./docker-setup.sh

Terminate solution
^^^^^^^^^^^^^^^^^^

To stop all container please run the below command::

   ./docker-teardown.sh
