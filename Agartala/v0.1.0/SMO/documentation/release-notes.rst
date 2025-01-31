.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0


IOS-MCN SMO: Operation and Maintenance Release Notes
====================================================

This document provides the release notes for IOS-MCN Operation and Maintenance (OAM) project.

Version Summary
---------------

Version Number: 0.0.3,
Version Name: Agartala,
Date: 26-01-2025

Version Number: 0.0.2,
Verson Name: Agartala,
Date: 18-12-2024

Version Number: 0.0.1,
Version Name: Agartala
Date: 31-10-2024

Projects/Repos Included in this release: ios-mcn-smo/oam, ios-mcn-smo/nfo, ios-mcn-smo/focom.


Version 0.0.3, 2025-01-26
-------------------------


Highlights:
***********

* RIC and Non-Functional Testing

* New version of PM-File-Converter - includes CPU consumption issue fix.

* Better configuration of elasticserach - heap-memory management.

* Better configuration for PM-Logger - removes the need for runtime configuration update.

* Improved Documentation


Version 0.0.2, 2024-12-18
-------------------------


Highlights:
***********

* Fault Handling - Display and clearing of faults received from gNB

* Non-RT-RIC Basic
  
    * rAPP Catalogue
    * A1 Policy Management Service
    * Data Producer

* Telegraf to collect metrics from Core and O-Cloud

* Logs from gNB and Core.
 

Version 0.0.1, 2024-10-31
-------------------------


Highlights:
***********

* Connectivity/registration:
      * OAM to register gNBs (both event-based and Manual) and RUs (both CallHome and Manual)
* Configuration:
     *  OAM to configure Network functions through GUI
* Performance Management
     * OAM to receive and process performance metrics from all Network fumctions and O-Cloud
* Logs Handling
     * OAM to receive, store and display logs from all network-function and O-Cloud
