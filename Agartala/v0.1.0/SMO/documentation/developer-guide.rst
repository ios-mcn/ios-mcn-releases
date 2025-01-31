.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

OAM Developer Guide
===================

This document provides a quickstart for developers of the IOSMCN OAM components.

Containers of IOSMCN OAM
------------------------
These are the containers that can be custom built. The remaining containers of OAM are suggested to use AS-IS.

.. csv-table:: Containers of IOSMCN OAM
   :file: ./containerscsv.csv
   :widths: 80, 70, 30
   :header-rows: 1


How to build these containers
-----------------------------

Use the below commands to build each and every container.

A1-PMS
******

.. code-block:: console

   cd deps/a1policymanagementservice
   mvn clean install -Dmaven.test.skip=true

Authentication Token
********************

.. code-block:: console

   cd deps/auth-token-fetch
   docker build -t nonrtric-plt-auth-token-fetch .


Control Panel and Gateway
*************************

.. code-block:: console

    cd deps/cp-gw/nonrtric-gateway
    mvn clean install
    docker build -t nonrtric-gateway .
    cd deps/cp-gw/webapp-frontend
    mvn clean install

datafile-collector
******************
.. code-block:: console

    cd datafilecollector
    mvn clean install
    mvn -Ddocker.image.name=docker.io/openjdk:17-jdk install docker:build


dmaap-mediator
**************
.. code-block:: console

    cd deps/dmaapmediator
    docker build -t o-ran-sc/nonrtric-plt-dmaapmediatorproducer:1.2.0 .

dmaap-adapter
*************
.. code-block:: console

    cd deps/dmaapadapter
    mvn clean install -Dmaven.test.skip=true


Information Co-Ordinator Service
********************************
.. code-block:: console

    cd deps/ics
    mvn clean install
    mvn install docker:build

RAN-PM file-converter, influxlogger, and pm-producer
****************************************************
.. code-block:: console

    cd pm-file-converter
    chmod +x build.sh
    ./build.sh no-push

    cd deps/ranpm/pmproducer
    mvn clean install -Dmaven.test.skip=true
    mvn install docker:build -Dmaven.test.skip=true

    cd deps/ranpm/influxlogger
    mvn clean install -Dmaven.test.skip=true
    mvn install docker:build -Dmaven.test.skip=true

    cd deps/ranpm/pm-file-converter
    chmod +x build.sh
    ./build.sh no-push

rAPP Catalogue
**************
.. code-block:: console

    cd deps/rappcatalogue
    mvn clean install -Dmaven.test.skip=true
    cd catalogue-enhanced
    docker build -t nonrtric-plt-rappcatalogue:1.2.0 .

SDNC
****

    cd deps/sdnc-oam
    mvn clean install -P docker -Ddocker.pull.registry=nexus3.onap.org:10001

VES-Collector
*************
.. code-block:: console

    cd deps/ves-collector
    mvn clean install -Dmaven.test.skip=true
    cp ./src/docker/Dockerfile ./target/VESCollector-1.12.3-SNAPSHOT/
    cd ./target/VESCollector-1.12.3-SNAPSHOT/
    docker build -t ves-collector:1.12.3 .

How to use the custom-built containers
--------------------------------------

To use the custom built containers, you just have to update the .env file the home OAM folder with values of newly built images.

