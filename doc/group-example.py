from pygr import seqdb
genome = seqdb.BlastDB('example.fa')
sequence_name = 'chrI'

import pygr_draw
from pygr_draw import AnnotationGroup

picture_class = pygr_draw.BitmapSequencePicture
colors = picture_class.colors

annotations2 = {}
annotations2['gene1'] = AnnotationGroup('gene1', sequence_name, ((50, 100), (200, 300), (500, 1500)),color=colors.red)

annotations2['gene2'] = AnnotationGroup('gene2', sequence_name, ((100, 300), (1500, 2000), (3000, 3750)),color=colors.blue)

annotations_map = pygr_draw.create_annotation_map(annotations2, genome)

p = pygr_draw.draw_annotation_maps(genome[sequence_name][:4000],(annotations_map,),picture_class=picture_class)

image = p.finalize()

filename = 'group-example.png'
open(filename, 'w').write(image)
print 'Output in', filename
