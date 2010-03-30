from pygr import seqdb
genome = seqdb.BlastDB('example.fa')
sequence_name ='chrI'

import pygr_draw
from pygr_draw import Annotation

image = pygr_draw.Draw('simple-example.png')
colors = image.colors

###

annots = []
annots.append(Annotation('exon1', sequence_name, 0, 500, color=colors.blue))
annots.append(Annotation('exon2', sequence_name, 200, 500, color=colors.green))
annots.append(Annotation('exon3', sequence_name, 250, 300, color=colors.black))

for i in range(250, 500, 10):
    name = 'exon%d' % (i+4)
    start = i
    end = 2000

    annots.append(Annotation(name, sequence_name, start, end,color=colors.red))

image.add_track(annots, genome)

###

from pygr_draw.xyplot import SpanValue, SpanMap
from pygr_draw import nlmsa

x = []
for k in range(0, 4000, 100):
    value = float(k % 1000) / 1000.
    a = SpanValue(sequence_name, k, 100, value)
    x.append(a)
msa = nlmsa.create_annotation_map(x, genome)
map = SpanMap(msa, height=5)

image.add_feature_map(map)

###

subsequence = genome[sequence_name][0:1000]
image.save(subsequence)

print 'Output in', image.filename
