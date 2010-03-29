"""
Utility for drawing annotations on sequences; uses pygr underneath.
"""

__version__ = "0.5"

import pygr                             # you'll need this installed...

__all__ = ['Annotation', 'AnnotationGroup', 'create_annotation_map',
           'Draw', 'draw_annotation_maps']

from annotation import Annotation, AnnotationGroup
from nlmsa import create_annotation_map
from draw import Draw, draw_annotation_maps
