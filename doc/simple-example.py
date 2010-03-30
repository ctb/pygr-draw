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

subsequence = genome[sequence_name][0:1000]
image.save(subsequence)

print 'Output in', image.filename
