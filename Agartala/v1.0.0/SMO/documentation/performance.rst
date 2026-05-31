.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

Performance
===========

Performance Monitoring values measured by the devices are necessary to
analyze and optimize the network. Therefore the application
automatically retrieves all historical performance values from the
devices and stores them in a database. The client retrieves the values
from the database and displays them in a graphical user interface.

Performance history values
--------------------------

After selecting a connected PNF supporting ONF-TR-532 and a physical
interface, the application collects the received and centralized stored
performance values for this interface.

The values are visualized using two views: a line chart and a table,
with the chart always shown first. To switch between them, toggle
buttons can be used. The chart view offers a filter to quickly limit the
shown values. To keep both views in sync, the filters of the chart and
the table are connected. If one view is filtered, the other one gets
updated in the background.
