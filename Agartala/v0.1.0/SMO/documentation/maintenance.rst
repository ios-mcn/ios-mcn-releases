.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Maintenance
===========

The 'Maintenance' application on OpenDaylight provides information about
planned maintenances of Network Elements, currently or in the future.
Users can manage devices to set the maintenance mode so that no
unnecessary alarms are created. When the device is in maintenance mode,
alarms are not forwarded to DCAE. As soon as the maintenance is
finished, the alarms will start flowing again.

The 'active' field in the table shows if the Network Element is
currently in maintenance mode or not. If it is 'active' it means the
Network Element is currently undergoing maintenance, if 'not active' it
means maintenance might have been set for a future date or is already
completed.

Users can disable the maintenance mode or change its start and end dates
by using the available options in the actions column.
