.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

.. contents::
   :depth: 3
..

General functionality
=====================

The following functionality is common to all applications.

Table data export
-----------------

Every table can export its data via the '︙' button. The data, which
gets exported is the currently viewed data in the table. As the default
pagination is set to 10, only the first 10 rows or filtered rows will be
exported. To increase the number of exported rows, change the
pagination.

The behavior of the export can vary based on the browser:

a) Some browsers allow you to save the file with the predefined name
   export.csv. In case your browser does not offer this function please
   use the 'Save as...' option and define the filename with extension
   csv.

b) Some browsers save the file automatically with the alphanumeric name
   but without an extension. In such a case navigate to the downloaded
   file location and rename the file. The extension (csv) must be
   appended to the name. The result should look like 'export\_file.csv'.

Table filters
-------------

The following filters are supported by all tables based on the data type
of the column.

+------------+------------------+------------+
| Data type  | Possible Filter  | Example    |
+============+==================+============+
| Text       | Any characters   | Test,      |
|            | or numbers,      | Tes\ \*,   |
|            | matches exactly  | \*\ t      |
|            | unless a \* is   |            |
|            | used. The \*     |            |
|            | acts as a        |            |
|            | wildcard and can |            |
|            | be used for      |            |
|            | contains, ends   |            |
|            | with and begins  |            |
|            | with queries.    |            |
+------------+------------------+------------+
| Numeric    | < or <= or > or  | >5000, 20, |
|            | >= or exact      | <=82       |
|            | number           |            |
+------------+------------------+------------+
| Boolean    | None (no filter  | true,      |
|            | set), true or    | false      |
|            | false            |            |
+------------+------------------+------------+
