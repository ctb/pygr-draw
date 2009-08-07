from pygr import seqdb
genome = seqdb.BlastDB('example.fa')
sequence_name = 'chrI'

import pygr_draw
from pygr_draw import AnnotationGroup

picture_class = pygr_draw.PDFSequencePicture
colors = picture_class.colors

annotations2 = {}
annotations2['gene1'] = AnnotationGroup('gene1', sequence_name,((0, 1000),(2000, 3000),(5000, 7000)),color=colors.red)

annotations2['gene2'] = AnnotationGroup('gene2', sequence_name,((2000, 4220),(5020, 6460),(6600, 7120)),color=colors.blue)

annotations2['gene3'] = AnnotationGroup('gene3', sequence_name,((500, 700),(1000, 2500)), color=colors.green)

annotations2['gene4'] = AnnotationGroup('gene4', sequence_name,((4675, 6475), (7500,8250)),color=colors.purple)

annotations2['gene5'] = AnnotationGroup('gene5', sequence_name,((7500, 8500), (10500,12250)),color=colors.orange)

annotations2['gene6'] = AnnotationGroup('gene6', sequence_name,((500, 600), (13000,14250)),color=colors.red)

annotations2['gene7'] = AnnotationGroup('geneStart', sequence_name,((0, 600), (3000,4250)),color=colors.green)

annotations2['gene8'] = AnnotationGroup('NoDraw', sequence_name,((10000,12000),(13000,17250)),color=colors.yellow)

annotations_map = pygr_draw.create_annotation_map(annotations2, genome)

p = pygr_draw.draw_annotation_maps(genome[sequence_name],(annotations_map,),picture_class=picture_class)
print len(genome[sequence_name])
image = p.finalize()
open('group2.pdf', 'w').write(image)
