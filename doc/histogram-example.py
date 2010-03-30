from pygr import seqdb
genome = seqdb.BlastDB('example.fa')
sequence_name ='chrI'

import pygr_draw
from pygr_draw import Annotation
from pygr_draw.xyplot import SpanValue, SpanMap, build_span_value_list
from pygr_draw import nlmsa

image = pygr_draw.Draw('histogram-example.png')
colors = image.colors

###

# layer on some basic annotations

annots = []
annots.append(Annotation('exon1', sequence_name, 0, 500, color=colors.blue))
annots.append(Annotation('exon2', sequence_name, 200, 500, color=colors.green))
annots.append(Annotation('exon3', sequence_name, 250, 300, color=colors.black))

annot_map = nlmsa.create_annotation_map(annots, genome)
image.add_feature_map(annot_map)

###

# also add a histogram, increasing from 0-1000 and then repeating, up to 4k.

x = []
for k in range(0, 4000, 100):
    value = float(k % 1000) / 1000.
    a = SpanValue(sequence_name, k, 100, value)
    x.append(a)
msa = nlmsa.create_annotation_map(x, genome)
map = SpanMap(msa, height=5, line_color='green', fill_color='black')

image.add_feature_map(map)

###

# add another histogram, representing per-base features.
sv_list = build_span_value_list(genome[sequence_name], annot_map, 1)
msa = nlmsa.create_annotation_map(sv_list, genome)
map = SpanMap(msa, height=5, line_color='black')
image.add_feature_map(map)

# add another histogram, representing binned features/10
sv_list = build_span_value_list(genome[sequence_name], annot_map, 10)
msa = nlmsa.create_annotation_map(sv_list, genome)
map = SpanMap(msa, height=5, line_color='red', fill_color='green')
image.add_feature_map(map)

# add another histogram, representing binned features/50
sv_list = build_span_value_list(genome[sequence_name], annot_map, 50)
msa = nlmsa.create_annotation_map(sv_list, genome)
map = SpanMap(msa, height=5, line_color='red', fill_color='green')
image.add_feature_map(map)

###

subsequence = genome[sequence_name][0:2000]
image.save(subsequence)

print 'Output in', image.filename
