========
HPmiko
========

HPmiko is a middle-man script to simplify extracting data from HP/Aruba Procurve switches using Netmiko

Installation
------------

To install HPmiko, simply use pip:

.. code-block::

  $ pip install HPmiko

HPmiko has the following requirements (which pip will install for you)

- netmiko >= 2.4.0

Documentation
-------------

https://andytruett.github.io/HPmiko/

Usage
-----

.. code-block::

  import HPmiko

  ip = 127.0.0.1
  username = "admin"
  password = "password"

  my_switch = HPmiko.HP(ip, username, password)

  my_switch.connect()

  hostname = my_switch.get_hostname()
  print(hostname)
