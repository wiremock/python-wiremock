.. _changelog:

ChangeLog
=========

Changes to the library are recorded here.

v2.2.0
------
  * Adds missing Metadata serde options thanks to @andreroggeri

v2.1.3
------
  * Fix on startup thanks to @Enforcer

v2.1.2
------
  * Python3.8 lint fixes thanks to @tirkarthi

v2.1.1
------
  * Fixes startup error on connection error thanks to @vasuarez

v2.1.0
------
  * Enables Templating thanks to @mauricioalarcon

v2.0.0
------
  * Fixes issue #14
  * Drops support for Python 2.x as this is EOL.

v1.2.0
------
  * Add custom cert/verification options to be passed normally through the singleton config
  * Upgrades minimum requests version to 2.20.0 for known CVE-2018-18074

v1.1.5
------
  * Looser requirements everywhere, run free!

v1.1.4
------
  * Update links in setup.py and docs

v1.1.3
------
  * Looser dependency constraint in setup.py

v1.1.2
------
  * Allow looser dependency constraint for requests

v1.1.1
------
  * Fixed bug when wiremock jar not found.

v1.1.0
------
  * Added Ability to stand up wiremock server (requires standalone jar being available).

v1.0.3
------
  * Fix support for Python 3.4.

v1.0.2
------
  * Wiremock 2.6.x uses 201 response code instead.

v1.0.1
------
  * Bug Fix on dictionary klass deserialization fix.

v1.0.0
------
  * First Release - included admin feature set for wiremock 2.5.1 standalone

