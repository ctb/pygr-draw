from stack import stack_annotations

from pygr.sequence import Sequence
from pygr import seqdb, cnestedlist

class BaseSequencePicture(object):
    SUFFIX = None                       # must define
    colors = None                       # must define
    
    def __init__(self, sequence_length, resolution):
        # sequence_length is used only to calculate the tick spacing
        self.sequence_length = sequence_length

        # resolution controls the granularity used to calculate overlaps.
        self.resolution = resolution
        
        self.imageseq = Sequence('A'*resolution, 'bitmap')
        self.genome = dict(bitmap=self.imageseq)
        self.left_margin_offset = 0

    def draw_sequence_line(self):
        raise NotImplementedError

    def _draw_feature(self, slot, start, stop, color=None):
        raise NotImplementedError

    def finalize(self):
        raise NotImplementedError

    def set_left_margin_offset(self, x):
        self.left_margin_offset = x

    ###

    def _calc_tick_spacing(self):
        for tickunit in range(12, 0, -1):
            if int(self.sequence_length / (10**tickunit)) >= 2:
                break

        self.TICKSPACING = 10**tickunit

    def draw_annotations(self, nlmsa, start_slot=0):
        try:
            annotations = nlmsa[self.imageseq]
        except KeyError:
            return 0
        
        if not annotations:
            return 0

        slots_d = stack_annotations(self.imageseq, nlmsa)
        max_slot_used = max(slots_d.values())

        for annotation in annotations:
            is_group = getattr(annotation, 'group', False) 
           
            subseq = annotation.sequence

            slot = start_slot + slots_d[annotation.id]
            color = annotation.color

            feat_start = annotation.feature_start
            stop = annotation.sequence.stop

            if is_group:
                self._draw_feature_name(annotation.name, feat_start, slot)
                self._draw_thin_feature(slot, feat_start, stop, color=color)

                for (start, stop) in annotation.annots:
                    self._draw_feature(slot, start, stop, color)
            else:
                self._draw_feature(slot, feat_start, stop, color)
                self._draw_feature_name(annotation.name, feat_start, slot)

        return max_slot_used + 1
