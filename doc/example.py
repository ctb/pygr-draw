#! /usr/bin/env python
"""
Example script showing how to use pygr_draw to draw annotations on a sequence.
"""

from pygr import seqdb
genome = seqdb.BlastDB('example.fa')
sequence_name = 'chrI'

import pygr_draw
from pygr_draw import Annotation

### set to either PDFSequencePicture or BitmapSequencePicture

#picture_class = pygr_draw.BitmapSequencePicture
picture_class = pygr_draw.PDFSequencePicture
colors = picture_class.colors

### create a bunch of annotations

annotations1 = {}
annotations1['exon1'] = Annotation('exon1', sequence_name, 0, 50,
                                   color=colors.blue)
annotations1['exon2'] = Annotation('exon2', sequence_name, 200, 500,
                                   color=colors.green)
annotations1['exon3'] = Annotation('exon3', sequence_name, 250, 300,
                                   color=colors.black)

for i in range(250, 500, 10):
    name = 'exon%d' % (i + 4)
    start = i
    end = 2000
    annotations1[name] = Annotation(name, sequence_name, start, end)

### convert annotations into an NLMSA annotations map

annotations_map = pygr_draw.create_annotation_map(annotations1, genome)

### draw me!

p = pygr_draw.draw_annotation_maps(genome[sequence_name], (annotations_map,),
                                   picture_class=picture_class)

### save image

filename = 'example' + p.SUFFIX            # build filename
image = p.finalize()                    # get raw data

open(filename, 'w').write(image)        # save!

print 'Wrote', filename
