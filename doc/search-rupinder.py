#! /Users/t/fiz/bin/python
import motility, pygr, pygr_draw
from pygr.seqdb import SequenceFileDB
from pygr_draw import Annotation

# load rupinder's sequence
evedb = SequenceFileDB('rupinder-eve.fa')
eveseq = evedb['eve-region']
eveseq = str(eveseq)

# do a simple search
matches = motility.find_iupac(eveseq, "WGATAR")

# now create a picture
picture_class = pygr_draw.BitmapSequencePicture
colors = picture_class.colors

# create the annotations
annotations = {}

for n, (start, stop, o, match) in enumerate(matches):
    if o > 0:
        color = colors.red
    if o < 0:
        color = colors.green

    name = str(n)
    a = Annotation(name, 'eve-region', start, stop, color=color)
    annotations[name] = a

###

annotations_map = pygr_draw.create_annotation_map(annotations, evedb)

region = evedb['eve-region']
subregion = region[0:1000]
p = pygr_draw.draw_annotation_maps(subregion, (annotations_map, annotations_map),
                                   picture_class=picture_class)

image = p.finalize()

filename = 'rupinder-eve.png'
open(filename, 'w').write(image)
print 'Output in', filename
