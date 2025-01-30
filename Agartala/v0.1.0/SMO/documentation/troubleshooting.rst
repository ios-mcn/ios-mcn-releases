.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

.. contents::
   :depth: 3
..

Troubleshooting
===============

* Deployment failures.
    * There can be multiple reasons for the deployment failures. If documentation has been followed correctly, then the possible failure-causes are minimal. Please share the output of the following commands in a github issue.
        * ./docker-setup.sh (main script).
        * docker ps -a
        * docker logs -f <name_of_the_failing_container>

* Containers are running but GUIs are not accessible.
    * This page lists all the exposed port numbers - /docs-oam/docs/interfaces.rst.
    * Check if you are using the correct port number.
    * check if firewall is blocking any of the ports.
    * If you are accessing it remotely, contact your IT administrator to see if any of these ports are blocked.

* gNB is not seen in the ODLUX.

    * Check if pNF Registration message is present in the kafka bus - use redpanda to verify.
    * If yes, then check the pnf message content for netconf credentials. The message should have right login/password - and that account should be present in the system.
    * If no, then check if gNB has right configuration of VES collector.


* Faults are not seen in in ODLUX.
    * Check if fault message are present in kafka bus - use redpanda to verify.
    * If Yes, In ODLUX GUI, go to settings, and select 'Enable Notifications'.
    * If No, then check if gNB has right configuration of VES collector.


* gNB Performance metrics is missing in InfluxDB.
    * Check if PerformanceAssurance messages are present in kafka bus - use redpanda to verify.
    * If Yes, then check the PerformanceAssurance message content for ftp path and credentials. The message should have right file-location path and right login/password.
    * If No, then check if gNB has right configuration of VES collector.


* Cloud and gNB Logs are missing.
    * Check if fluentd container is running.
    * If yes, check the fluentd configuration (config/fluentd/conf/fluent.conf) - the values for host and port should match the elasticsearch configuration. The port is 9200, and the host should be either the IP address or the service-name of the elasticsearch.
