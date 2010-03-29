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

---

From lyorn, to view your files thru the Web: ::

   mkdir ~/.html
   ln -fs /path/to/pygr-draw /u/<username>/.html

(replace /path/to/ and <username> appropriately). Now the files should
be accessible at

   http://lyorn.idyll.org/~<username>/pygr-draw/

---

JavaScript toolkit/drawing options:

http://ivory.idyll.org/blog/may-08/lazyweb-javascript-image-stuff

Some good references in there; ixany on SVG, but check out

   http://plugins.jquery.com/project/Draw
   http://hackmap.blogspot.com/2008/04/comparative-genomics-with-openlayers.html
   http://openlayers.org/dev/examples/
   http://processingjs.org/

We can always go with image maps, if necessary, but they're not as nice
as JS could be.
