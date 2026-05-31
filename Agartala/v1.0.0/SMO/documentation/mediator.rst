.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Mediator
========

A 'Mediator' provides an external -  to the physical network function - 
OAM interface.

Some physical network function manufactures use the
`generic mediator
framework <https://github.com/Melacon/NetConf2SNMP>`__. Such mediators
offer a management API to control mediator function.

New mediator servers can be added via the '+' button. Afterward, a
server can be selected to view all available mediator instances.

A mediator instance can be started, stopped and deleted using the
available actions. Additionally, its details can be viewed. The '+'
button allows the user to add a new instance. During the creation, at
least one 'ODL auto connect' configuration must be added.
