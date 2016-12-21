Introduction
------------

"daemonmgr" is a shell script launching a python program allowing to manage daemons on your system.

Installation
------------

Install, upgrade and uninstall influxsql with the following commands:

::

    $ pip install daemonmgr
    $ pip install --upgrade daemonmgr
    $ pip uninstall daemonmgr

Dependencies
------------

None

Documentation
-------------

There is no specific documentation for daemonmgr except the examples
below.

Examples
--------

Registering a daemon.

A name (an id) must be given to the daemon. In addition, the command to be launched must be provided as well as standard output and error redirections

::

    $ daemonmgr -register --daemon sample_daemon --stdout /tmp/sample_daemon.out --stderr /tmp/sample_daemon.err --command "sleep 100" --name "sleep 100"

Listing all daemons

::

    $ daemonmgr -list

Listing a particular daemon

::

    $ daemonmgr -list --daemon sample_daemon

Unregistering a daemon

::

    $ daemonmgr -unregister --daemon sample_daemon

Starting a daemon

::

    $ daemonmgr -start --daemon sample_daemon

Stopping a daemon

::

    $ daemonmgr -stop --daemon sample_daemon

Restarting a daemon

::

    $ daemonmgr -restart --daemon sample_daemon

Checking the status of a particular daemon

::

    $ daemonmgr -status --daemon sample_daemon

Checking the status of all registered daemons

::

    $ daemonmgr -status

