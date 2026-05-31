.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

OAM Configuration
=================

This documents the configuration of the various components of Non-RT-RIC before deployment.

Important Configuration Parameters
----------------------------------

Only important configurations are documented here:

+-------------------+----------------------------------------------------------+-----------------------------------------------------+
| Parameter         | Description                                              | Location                                            |
+===================+==========================================================+=====================================================+
| ric               | User can add set of RICs for AI-PolicyManagementService. | config/a1pms/application_configuration.json         |
+-------------------+----------------------------------------------------------+-----------------------------------------------------+
| ics-base-url      | URL of the Information co-ordinator service              | config/dmaap-adapter/application.yaml               |
+-------------------+----------------------------------------------------------+-----------------------------------------------------+
| dmaap-base-url    | URL of the DMAAP Message Router                          | config/dmaap-adapter/application.yaml               |
+-------------------+----------------------------------------------------------+-----------------------------------------------------+
| bootstrap-servers | URL of Kafka                                             | config/dmaap-adapter/application.yaml               |
+-------------------+----------------------------------------------------------+-----------------------------------------------------+
| dmaapTopicUrl     | Preferred dmaapTopic                                     | config/dmaap-adapter/application_configuration.json |
+-------------------+----------------------------------------------------------+-----------------------------------------------------+
| kafkaInputTopic   | Preferred Kafka Topic                                    | config/dmaap-adapter/application_configuration.json |
+-------------------+----------------------------------------------------------+-----------------------------------------------------+
