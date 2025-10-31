.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Frequently asked questions
==========================

Which browser should I use to operate OpenDaylight SDN-R User interface?
------------------------------------------------------------------------

An actual version of `Google
Chromium <https://www.chromium.org/getting-involved/download-chromium>`__
or `Google
Chrome <https://www.google.de/search?q=chrome+download&oq=chrome+download&aqs=chrome..69i57j0l5.2718j0j4&sourceid=chrome&ie=UTF-8>`__
is recommended.

--------------

How to enable detailed logs in karaf for SDN-R applications
-----------------------------------------------------------

If you like to see more details in karaf logs for the NetConf
communication between ODL and NetConf servers (mediators/devices) please
invoke the following commands in the karaf console.

::

    # Logging settings (on)
    log:set DEBUG org.onap.ccsdk.features.sdnr
    log:set TRACE org.opendaylight.netconf
    log:set TRACE com.highstreet.technologies.odl.app

Please note, setting the debug level to 'TRACE' may impact the
performance on the controller. In production environment make sure to
set back the debug level to 'INFO' as soon possible.

::

    # Logging settings (off)
    log:set INFO org.onap.ccsdk.features.sdnr
    log:set INFO org.opendaylight.netconf
    log:set INFO com.highstreet.technologies.odl.app

--------------

Which commands should be used to analyze karaf logs?
----------------------------------------------------

::

    cd $ODL_KARAF_HOME/data/log
    rm *.txt
    grep -anr --include=*.log* "| ERROR |" . | grep 2018 >> 01-error.txt
    grep -anr --include=*.log* "RemoteDevice{" . | grep 2018 >> 02-devices.txt
    grep -anr --include=*.log* "RemoteDevice{" . | grep "Unable to build schema context, unsatisfied imports" | grep 2018 >> 03-schema-issue.txt
    grep -anr --include=*.log* "Matched request:" . | grep 2018 >> 04-matched-request.txt
    grep -anr --include=*.log* "network-element" . | grep 2018 >> 05-network-element.txt
    grep -anr --include=*.log* "urn:onf:params:xml:ns:yang:core-model" . | grep 2018 >> 06-core-module.txt
    grep -anr --include=*.log* "PerformanceManagerTask" . | grep 2018 >> 07-pm-tick.txt
    grep -anr --include=*.log* "Unable to read NE data for mountpoint" . | grep 2018 >> 08-unable-to-read.txt
    grep -anr --include=*.log* "LKCYFL79Q01M01MSS801" . | grep 2018 >> 09-LKCYFL79Q01M01MSS801.txt

How to report an odlux issue
----------------------------

If you would like to report an odlux issue which you have noticed in the
Graphical User Interface, please provide the following information:

1. **Description**: In which application you have noticed the issue?

2. **Environment**:

   -  Which browser is used and the version of the browser. eg: *Google
      chrome - version 71.0.3578.80 / Mozilla Firefox.*
   -  Which Operating system and version. eg: *Linux/ Windows 10 -
      version 1803.*
   -  In which language you are using the application.
   -  The application URL which is available on the browser address bar.
      eg: *http://hostname/odlux/index.html#/connectApp*

3. **Expected Result**: What is the expected result you are looking for?

4. **Actual Result**: What is the actual result you got?

5. **Steps to reproduce**: Describe the steps to reproduce the scenario.
   If possible, please provide the screenshots

The above information helps us to analyze the problem quicker.
