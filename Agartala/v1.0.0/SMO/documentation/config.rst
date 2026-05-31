.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Configuration
=============

The application shows the actual values of all attributes of the
ONF-TR-532 for a selected physical network function (PNF). Each view of
a functional element is divided into capabilities, configuration,
status, current problem, current performance and history performance
information according to TR-532.

A separate window is available for modifying the configuration. All
changes made are sent to the device in a single NetConf bulk request.
The operator is notified about successfully configuring the device.

Implementation
--------------

The application is implemented as ODLUX web application using the
RestConf northbound interface of the SDN controller. The key frameworks
are: Typescript, React and material-ui.

Connection status information is updated automatically using a web
socket for notifications from OpenDaylight to the browser.
