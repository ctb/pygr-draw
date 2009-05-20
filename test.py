from pygr import seqdb
import pygr_draw

class TestStack:
    def setup(self):
        self.genome = seqdb.BlastDB('doc/example.fa')

    def test_no_stack_at_all(self):
        seq = self.genome['chrI']
        
        annots = {}
        annots['a'] = pygr_draw.Annotation('a', 'chrI', 0, 50)

        map = pygr_draw.create_annotation_map(annots, self.genome)

        slots = pygr_draw.stack_annotations(seq, map)
        
        assert slots['a'] == 0           # should be on level 0

    def test_stack_two(self):
        seq = self.genome['chrI']
        annots = {}
        
        annots['a'] = pygr_draw.Annotation('a', 'chrI', 0, 50)
        annots['b'] = pygr_draw.Annotation('b', 'chrI', 35, 100)

        map = pygr_draw.create_annotation_map(annots, self.genome)
        slots = pygr_draw.stack_annotations(seq, map)

        assert slots['a'] == 1           # the short annot should be on level 1
        assert slots['b'] == 0
        
    def test_stack_many(self):
        seq = self.genome['chrI']
        annots = {}

        length = len(seq)
        for i in range(0, length, 100):
            name = 'annot%d' % (i,)
            annots[name] = pygr_draw.Annotation(name, 'chrI', i, length)

        map = pygr_draw.create_annotation_map(annots, self.genome)
        slots = pygr_draw.stack_annotations(seq, map)

        assert max(slots.values()) == len(annots) - 1
        
