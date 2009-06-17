"""
Utility for drawing annotations on sequences; uses pygr underneath.
"""

__version__ = "0.3"

import pygr

from annotation import Annotation, AnnotationGroup, convert_to_image_coords
from nlmsa import create_annotation_map
from stack import stack_annotations

from PDFSequencePicture import PDFSequencePicture
from BitmapSequencePicture import BitmapSequencePicture

from pygr import cnestedlist

def draw_annotation_maps(seq, annot_maps,
                         default_colors=None,
                         picture_class=BitmapSequencePicture,
                         wrappers=None):
    # make sure the list of default colors is the same length as the list
    # of input annotation maps.
    
    if default_colors is None:
        default_colors = [ 'black' ] * len(annot_maps)
    else:
        default_colors = list(default_colors)
        for i in range(len(default_colors), len(annot_maps)):
            default_colors.append('black')

    # make sure the list of feature wrappers is the same length as the
    # list of input annotation maps.
    if wrappers is None:
        wrappers = [ None ] * len(annot_maps)
    else:
        wrappers = list(wrappers)
        for i in range(len(wrappers), len(annot_maps)):
            wrappers.append(None)

    # create an instance of the picture class, whatever it may be.
    p = picture_class(len(seq))

    ### underneath, draw each set of annotations
    l = []
    maxmax_text_length = 0
    for n, annot_map in enumerate(annot_maps):
        default_color = default_colors[n]

        annots = annot_map[seq]
        new_map, max_text_length = \
                 convert_to_image_coords(seq, annots, p, default_color,
                                         wrappers[n])
        l.append(new_map)
        maxmax_text_length = max(maxmax_text_length, max_text_length)

    p.set_left_margin_offset(maxmax_text_length)
    
    ### draw the basic sequence line
    p.draw_sequence_line()

    start_slot = 0
    for new_map in l:
        n_slots = p.draw_annotations(new_map, start_slot=start_slot)
        start_slot += n_slots

    return p
