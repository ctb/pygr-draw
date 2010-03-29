pygr-draw is a library for drawing features on sequences.

It requires pygr v0.8+, ReportLab for drawing PDFs, and/or the Python
Imaging Library (PIL) for drawing PNGs.

Development happens on github:

   http://github.com/ctb/pygr-draw/

And you can get the source code like so:

   git clone git://github.com/ctb/pygr-draw.git

---

Getting started
---------------

Check out the files in doc/, starting with `the index <doc/index.html>`__.

To run .py files in doc/, you have to set up the environment properly.
First, set the PYTHONPATH: start in the top level pygr-draw directory and do,
::

   export PYTHONPATH=`pwd`
   cd doc/

Now type 'make' to build all of the HTML (you'll need docutils...) or
you can run the various examples yourself, e.g. ::

   python simple-example.py
   python group-example.py

To run all the doctests, do ::

   python run-doctests.py *.txt

or to run a single one, do ::

   python run-doctests.py simple-example.txt

