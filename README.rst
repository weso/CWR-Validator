CWR Data Model Validator
========================

Validator service for CWR files. It receives a file following the CISAC CWR
standard v2.1 and returns a JSON containing the data from that same file.

While right now it only handles parsing CWR files, in the future it will allow
generating acknowledgement files, create validation reports, and will also
support receiving the CWR files as a JSON.

It uses the `CWR Data Model`_ API, and it is recommended using that same
library to read the JSON created by the service.

Documentation
-------------

The current version is under development. No public documentation is still offered.

Status
------

The project is still in the development phase.

Issues management
~~~~~~~~~~~~~~~~~

Issues are managed at the GitHub `project issues page`_.

Building the code
-----------------

The application has been coded in Python, without using any particular framework.

Prerequisites
~~~~~~~~~~~~~

The project has been tested in the following versions of the interpreter:

- Python 2.6
- Python 2.7
- Python 3.3
- Python 3.4
- Pypy
- Pypy 3

All other dependencies are indicated on requirements.txt. The included makefile can install them with the command:

``make requirements``

Getting the code
~~~~~~~~~~~~~~~~

The code can be found at the `GitHub project page`_.

License
-------

The project has been released under the `MIT License`_.

.. _CWR Data Model: https://github.com/weso/CWR-DataApi
.. _project issues page: https://github.com/weso/CWR-Validator/issues
.. _GitHub project page: https://github.com/weso/CWR-Validator
.. _MIT License: http://www.opensource.org/licenses/mit-license.php