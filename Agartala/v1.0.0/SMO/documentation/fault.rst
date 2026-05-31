.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Fault Management
================

To operate a network, it is important to get an overview about the
currently raised alarms. The application offers basic fault management
of devices supporting ONF-TR-532. The alarms are classified according to
the severity level (warning, minor, major, critical).

Views
-----

The graphical user interface is separated into three views.

Current Problem List
~~~~~~~~~~~~~~~~~~~~

Lists all current active faults in the network. In addition, it also
lists alarms sent by the SDN controller itself, which detects connection
losses to the NetConf server (connectionLossOAM) or to a device via a
mediator to a device (connectionLossNeOAM).

Alarm Notifications
~~~~~~~~~~~~~~~~~~~

As long as the view is open, all alarm notifications received by the SDN
Controller are listed. Please note that refreshing the view will start
the collection again. Previous alarm notification can be viewed in the
alarm log.

Alarm Log
~~~~~~~~~

Next to the current active alarms an alarm log lists all alarm
notifications of the past.

Implementation
--------------

The application has two parts. While the server is listening for NetConf
notifications to store them in the database, the client retrieves the
information from the database and displays them in a table.

The server synchronizes with the current alarm lists of the devices.
Based on raised and cleared notifications, the current alarm status of
the network is calculated. The current alarms are stored in a database.
In addition, all Problem Notifications received by the SDN controller
are stored. There is no logic implemented on the client side.

An alarm status bar in the header of the web application informs the
operator about the health status of the network.

The ODLUX web application uses web sockets to update the graphical user
interface of the Alarm Notifications (devices) and Connection Status
Notifications in real-time.
