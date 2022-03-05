.. asciinema-sphinx documentation master file, created by
   sphinx-quickstart on Sun Feb 20 16:42:47 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to asciinema-sphinx's documentation!
============================================


Text

.. asciinema_run_cmd:: python -m rich.panel
   :autoPlay: true


.. asciinema_timed_cmd_interaction:: python -m sphinx_auto_asciinema.test
   :autoPlay: true

   - n

.. asciinema_scripted_cmd_interaction:: python -m sphinx_auto_asciinema.test

   - [":", "y"]
   - [":", "apple"]

.. asciinema_run_cmd:: python -m rich.panel
   :autoPlay: false
