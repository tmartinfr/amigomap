
.. image:: https://circleci.com/gh/tmartinfr/amigomap/tree/master.svg?style=shield
    :target: https://circleci.com/gh/tmartinfr/amigomap/tree/master

Description
===========

This app brings you the best recommandations for places around you, from people
you like.

Create a map, and let your friends, colleagues or family adding new places,
commenting, and evaluating them.

Choose to open your map to the public or keep it private.

List restaurants, sport spots, museums, bars, everything is possible!

Initial setup
=============
First, in order to load the few example maps provided, you will have to add
this line to your ``/etc/hosts`` file : ::

    127.0.0.1 resto.localhost coworking.localhost running.localhost

Then, check and execute the ``./bin/quickstart`` script (Docker powered).

Finally, try to open one the example map in your browser, for example
http://coworking.localhost:8000/.

Additional notes
================
In development mode, Django admin is available at
http://resto.localhost:8000/admin/ (reusing one the map domain created above)
with credentials `admin/admin`.

In production mode (`config.settings.base` is used), default Django logging is
fully disabled. It's up to the system administrator to configure logging before
executing Django `get_wsgi_application()` (if WSGI is used).
