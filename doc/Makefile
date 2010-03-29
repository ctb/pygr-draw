%.html : %.txt
	run-doctests.py $<
	rst2html.py $< $@

all: simple-example.html group-example.html wrapper-example.html index.html

