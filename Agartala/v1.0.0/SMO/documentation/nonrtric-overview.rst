.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2021-2023 Nordix Foundation. All rights Reserved
.. Copyright (C) 2023 OpenInfra Foundation Europe. All Rights Reserved

.. |archpic| image:: ./images/nonrtric-architecture-I.png
  :alt: Image: O-RAN SC - NONRTRIC Overall Architecture

Introduction
------------

The Non-RealTime RIC (RAN Intelligent Controller) is an Orchestration and Automation function described by the O-RAN Alliance for non-real-time intelligent management of RAN (Radio Access Network) functions.

The primary goal of the Non-RealTime RIC is to support non-real-time radio resource management, higher layer procedure optimization, policy optimization in RAN, and providing guidance, parameters, policies and AI/ML models to support the operation of near-RealTime RIC functions in the RAN to achieve higher-level non-real-time objectives.

Non-RealTime RIC functions include service and policy management and RAN analytics for the RAN.
The Non-RealTime RIC platform hosts and coordinates rApps (Non-RT RIC applications) to perform Non-RealTime RIC tasks.
The Non-RealTime RIC also hosts the new R1 interface (between rApps and SMO/Non-RealTime-RIC services).

The O-RAN-SC (OSC) NONRTRIC project provides concepts, architecture and reference implementations as defined and described by the `O-RAN Alliance <https://www.o-ran.org>`_ architecture.
The OSC NONRTRIC implementation communicates with near-RealTime RIC elements in the RAN via the A1 interface. Using the A1 interface the NONRTRIC will facilitate the provision of policies for individual UEs or groups of UEs; monitor and provide basic feedback on policy state from near-RealTime RICs; provide enrichment information as required by near-RealTime RICs; and facilitate ML model training, distribution and inference in cooperation with the near-RealTime RICs.
The OSC NONRTRIC hosts rApps, and coordinates all interactions between the rApp and underlying SMo by way of the R1 Interface. 

|archpic|

NONRTRIC components
-------------------

For the Agartala release, these are the components that make up the Non-RT-RIC:

* Non-RT-RIC Control Panel
* Information Coordinator Service
* A1 Policy Management Service
* DMaaP/Kafka Information Producer Adapters
* Initial Non-RT-RIC App Catalogue
* Authentication Support
* PM rAPP


Non-RT-RIC Control Panel / NONRTRIC Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Graphical user interface.

- View and Manage A1 policies in the RAN (near-RT-RICs)
- Graphical A1 policy creation/editing is model-driven, based on policy type's JSON schema
- View and manage producers and jobs for the Information coordinator service
- Configure A1 Policy Management Service (e.g. add/remove near-rt-rics)
- Interacts with the A1-Policy Management Service & Information Coordination Service (REST NBIs) via Service Exposure gateway

Implementation:

- Frontend: Angular framework

Information Coordination Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ICS is a data subscription service which decouples data producers from data consumers. A data consumer can create a data subscription (Information Job) without any knowledge of its data producers (one subscription may involve several data producers). A data producer has the ability to produce one or several types of data (Information Type). One type of data can be produced by zero to many producers.

A data consumer can have several active data subscriptions (Information Job). One Information Job consists of the type of data to produce and additional parameters, which may be different for different data types. These parameters are not defined or limited by this service.

Maintains a registry of:

- Information Types / schemas
- Information Producers
- Information Consumers
- Information Jobs

The service is not involved in data delivery and hence does not put restrictions on this.

Implementation:

- Implemented as a Java Spring Boot application.

A1 Policy Management Service (from ONAP CCSDK)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A1 Controller Service above A1 Controller/Adapter that provides:

- Unified REST & DMaaP NBI APIs for managing A1 Policies in all near-RT-RICs.

  - Query A1 Policy Types in near-RT-RICs.
  - Create/Query/Update/Delete A1 Policy Instances in near-RT-RICs.
  - Query Status for A1 Policy Instances.

Maintains (persistent) cache of RAN's A1 Policy information.

- Support RAN-wide view of A1 Policy information.
- Streamline A1 traffic.
- Enable (optional) re-synchronization after inconsistencies / near-RT-RIC restarts.
- Supports a large number of near-RT-RICs (& multi-version support).

- Converged ONAP & O-RAN-SC A1 Adapter/Controller functions in ONAP SDNC/CCSDK (Optionally deploy without A1 Adapter to connect direct to near-RT-RICs).
- Support for different Southbound connectors per near-RT-RIC - e.g. different A1 versions, different near-RT-RIC version, different A1 adapter/controllers supports different or proprietary A1 controllers/EMSs.

Implementation:

- Implemented as a Java Spring Boot application.
- Wiki: `A1 Policy Management Service in ONAP <https://wiki.onap.org/pages/viewpage.action?pageId=84672221>`_ .

A1/SDNC Controller & A1 Adapter (Controller plugin)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mediation point for A1 interface termination in SMO/NONRTRIC.

- Implemented as CCSDK OSGI Feature/Bundles.
- A1 REST southbound.
- RESTCONF Northbound.
- NETCONF YANG > RESTCONF adapter.
- SLI Mapping logic supported.
- Can be included in an any controller based on ONAP CCSDK.

Implementation:

- Wiki: `A1 Adapter/Controller Functions in ONAP <https://wiki.onap.org/pages/viewpage.action?pageId=84672221>`_ .

DMaaP Information Producer Adapters (Kafka)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurable mediators to take information from DMaaP and Kafka and present it as a coordinated Information Producer.

These mediators/adapters are generic information producers, which register themselves as information producers of defined information types in Information Coordination Service (ICS).
The information types are defined in a configuration file.
Information jobs defined using ICS then allow information consumers to retrieve data from DMaaP MR or Kafka topics (accessing the ICS API).

There are two alternative implementations to allow Information Consumers to consume DMaaP or Kafka events as coordinated Information Jobs.

Implementation:
- Implementation in Java Spring (DMaaP Adapter),
- Implementation in Go (DMaaP Mediator Producer), 

Initial App Catalogue
~~~~~~~~~~~~~~~~~~~~~

Register for Non-RT-RIC Apps.

- Non-RT-RIC Apps can be registered / queried.
- Limited functionality/integration for now.
- *More work required in coming releases as the rApp concept matures*.

Implementation:

- Implemented as a Java Spring Boot application and in Python.
- Repo: *nonrtric/plt/rappcatalogue*
- Documentation at the :doc:`rApp Catalogue documentation site <rappcatalogue:index>`.

Authentication Support (Keycloak)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The auth-token-fetch provides support for authentication.
It is intended to be used as a sidecar and does the authentication procedure, gets and saves the access token
in the local file system. This includes refresh of the token before it expires.
This means that the service only needs to read the token from a file.

It is tested using Keycloak as authentication provider.

.. image:: ./images/AuthSupport.png
   :width: 500pt

So, a service just needs to read the token file and for instance insert it in the authorization header when using HTTP.
The file needs to be re-read if it has been updated.

The auth-token-fetch is configured by the following environment variables.

* CERT_PATH - the file path of the cert to use for TSL, example: security/tls.crt
* CERT_KEY_PATH - the file path of the private key file for the cert, example: "security/tls.key"
* ROOT_CA_CERTS_PATH - the file path of the trust store.
* CREDS_GRANT_TYPE - the grant_type used for authentication, example: client_credentials
* CREDS_CLIENT_SECRET - the secret/private shared key used for authentication
* CREDS_CLIENT_ID - the client id used for authentication
* OUTPUT_FILE - the path where the fetched authorization token is stored, example: "/tmp/authToken.txt"
* AUTH_SERVICE_URL - the URL to the authentication service (Keycloak)
* REFRESH_MARGIN_SECONDS - how long in advance before the authorization token expires it is refreshed
