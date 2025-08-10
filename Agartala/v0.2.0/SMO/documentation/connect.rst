.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Connect
=======

The 'Connect' application on OpenDaylight provides up-to-date
connectivity information about the wireless devices in the network. It
automatically displays new Network Elements and their connection status.
Usually, the Network Elements mount themselves. If necessary, they can
be mounted manually by right-clicking on the element and selecting the
'mount' action. For better understanding of alarms and status, a
connection status log lists all the connection status changes of
OpenDaylight mount points.

Views
-----

The graphical user interface is divided into two sections.

Network Elements
~~~~~~~~~~~~~~~~

Network Elements are physical network functions (PNFs). A table view
shows all configured and connected NetConf Servers of the SDN-R cluster.
This view also allows to manually configure/mount a device via the '+'
button. The SDN controller will start connecting to the NetConf server.

Network Elements can be marked as 'required'. If an element is required,
it will stay available even if disconnected. If an element is not
required, it will be deleted once disconnected.

By right-clicking on an element, an action menu opens. The menu allows
to mount, unmount, view the details, edit and remove the element.
Additionally, it links to several applications like
`Fault <fault.rst>`__ and
`Configure <config.rst>`__, which will be filtered to
display information relevant to the selected element.

Connection Status Log
~~~~~~~~~~~~~~~~~~~~~

The log lists the connection status changes between SDN Controller and
NetConf servers (devices).
