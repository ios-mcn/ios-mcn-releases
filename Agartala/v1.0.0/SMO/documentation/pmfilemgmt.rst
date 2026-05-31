.. SPDX-License-Identifier: CC-BY-4.0

RAN PM File Management
======================
This work is taken from O-RAN-SC NON-RT-RIC RANPM Project.
Only the datafile collector is modified to meet the needs of IOSMCN project.


A PM report (containing aggregated PM measurements over a time interval) is
an XML file. The format is defined by 3GPP. The files are collected from the RAN and stored. An rApp can subscribe for chosen measurement types from measured resources in the network.



Components
----------

The picture illustrates the components involved.

* The PM Data File Collector fetches the XML files from the RAN.
* The PM File Converter converts these to a Json format. The structure and the contents
  is the same as the XML format.
* The PM Producer handles filtering and distribution of PM data to subscribers. These subscribers can be rApps.
* The Influx Logger stores selected PM measurements into a time series database.
* HTTPS-SERVER is for testing and implements functionality to simulate file transfer from RAN nodes.

.. image:: ./images/pmfr-components.png
   :width: 500pt

For more detailed documentation of the components, please refer to these external links.

* `Non-RT RIC - RAN PM - PM Data File Collector <https://docs.o-ran-sc.org/projects/o-ran-sc-nonrtric-plt-ranpm/en/latest/datafilecollector/index.html>`_
* `Non-RT RIC - RAN PM - PM File Converter <https://docs.o-ran-sc.org/projects/o-ran-sc-nonrtric-plt-ranpm/en/latest/pm-file-converter/index.html>`_
* `Non-RT RIC - RAN PM - PM Producer <https://docs.o-ran-sc.org/projects/o-ran-sc-nonrtric-plt-ranpm/en/latest/pmproducer/index.html>`_
* `Non-RT RIC - RAN PM - Influx Logger <https://docs.o-ran-sc.org/projects/o-ran-sc-nonrtric-plt-ranpm/en/latest/influxlogger/index.html>`_
* `Non-RT RIC - Information Coordinator Service <https://docs.o-ran-sc.org/projects/o-ran-sc-nonrtric-plt-informationcoordinatorservice/en/latest/index.html>`_


Data Flow
---------

The figure below gives an overview of the data flow through the components.

.. image:: ./images/DataFlow.png
   :width: 900pt

1. The RAN node sends a VES event with available PM measurement report files.
2. The VES event is put on a Kafka topic and picked up by the Data File Collector.
3. A PM report file is fetched from the RAN node by a file transfer protocol. Which protocol to use is defined in the VES event.
4. The collected file is stored
5. A File collected object is put on a Kafka topic and is picked up by the PM File Converter.
6. The file data is read from the file store.
7. A PM report in json format is stored (compressed with gzip).
8. A message (a Json object) indicating that a new PM report (in Json format) is available is put on a Kafka topic and is picked up by the PM Data Producer.
9. The PM data producer reads the Json file
10. The subscribed PM data is sent to the PM data consumers (over Kafka). An rApp may be a PM data consumer.
11. The Influx Logger, which is a PM data consumer, stores PM data in an Influx database.

At anytime an rApp can read logged PM data from the Influx database.

PM Data Subscription
--------------------

PM measurement data is subscribed by creating an Information Job using the Information Coordination Service (ICS).
This a subscription broker and is part of what is called Data Management an Exposure (DME) in O-RAN.
The ICS makes sure that all data producers gets its data subscriptions (jobs).

In the picture below, an rApp and the Influx Logger are consumers of PM data.

.. image:: ./images/ControlFlow.png
   :width: 500pt

The PM Data Influx logger will create a PM data subscription based on a configuration file. An rApp can create
PM data subscription. The PM Data producer will deliver received PM measurements according to the subscriptions.

The PM Data file collector will fetch all PM measurement files. The PM Data Converted will convert all fetched xml files
to json. So these does not use any subscriptions.

**************************************
PM Subscriber design time dependencies
**************************************

An rApp uses the ICS API to create and manage the subscription of PM Measurements.
The API documentation is available in :doc:`Non-RT RIC - Information Coordinator Service (Documentation site) <ics:index>`.

The schema for the PM Measurement information jobs is defined in :doc:`Non-RT RIC - RAN PM - PM Producer (Documentation <pmproducer:index>`.
This schema defines parameters used in the subscription (info job) and defines which measurements to subscribe for and on which
kafka topic the information shall be delivered to.

An application retrieving logged PM data from the Influx database needs to consider how the data is stored (the schema). That is
defined in :doc:`Non-RT RIC - RAN PM - Influx Logger (Documentation) <influxlogger:index>`.

.. image:: ./images/DesignTimeDependencies.png
   :width: 500pt
