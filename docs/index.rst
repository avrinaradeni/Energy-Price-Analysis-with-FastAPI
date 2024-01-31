.. IN3110 Assignment5 documentation master file, created by
   sphinx-quickstart on Sun Dec  3 20:26:35 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Strompris's documentation!
==============================================

Is your wallet bleeding every time you turn on the heater? This module will help you find out!

The code retrieves electricity prices using data from `Hva koster strømmen`_ and displays it as a chart.

.. _`Hva koster strømmen`: https://www.hvakosterstrommen.no/strompris-api


To create the webpage run 

``python app.py``


Uvicorn will then give you a link. Copy-paste this link into your browser to see the webpage.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


   api.rst 
   apiStrom.rst 


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
