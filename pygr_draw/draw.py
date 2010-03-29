from PythonList import PythonList
from nlmsa import create_annotation_map
from annotation import convert_to_image_coords

def get_picture_class(suffix='png'):
    suffix = suffix.lower()
    if suffix == 'pdf':
        from PDFSequencePicture import PDFSequencePicture as klass
    elif suffix == 'png':
        from BitmapSequencePicture import BitmapSequencePicture as klass

    return klass

class Draw(object):
    def __init__(self, filename=None, picture_class=None, default_colors=None):
        if filename and not picture_class:
            if '.' in filename:
                suffix = filename.rsplit('.')[-1]
                picture_class = get_picture_class(suffix)
            else:
                picture_class = get_picture_class(suffix)

        self.filename = filename
        self.picture_class = picture_class
        self.colors = picture_class.colors
        self.default_colors = None

        self.maps = []
        self.wrappers = []

    def add_track(self, annotations, sequence_db, wrapper=None):
        map = create_annotation_map(annotations, sequence_db)
        self.add_feature_map(map, wrapper)

    def add_feature_map(self, map, wrapper=None):
        self.maps.append(map)
        self.wrappers.append(wrapper)

    def draw(self, seq):
        picture = draw_annotation_maps(seq, self.maps,
                                       default_colors=self.default_colors,
                                       picture_class=self.picture_class,
                                       wrappers=self.wrappers)

        return picture

    def save(self, seq, fp_or_filename=None):
        if not fp_or_filename:
            if not self.filename:
                raise Exception("no file given, either in constructor or in save()")

            fp_or_filename = self.filename
        
        try:
            fp_or_filename.write
            fp = fp_or_filename         # it's a file handle!
            do_close = False
        except AttributeError:
            fp = open(fp_or_filename, 'w') # it's a filename!
            do_close = True

        picture = self.draw(seq)
        image = picture.finalize()
        fp.write(image)

        if do_close:
            fp.close()
        

def draw_annotation_maps(seq, annot_maps,
                         default_colors=None,
                         picture_class=None,
                         wrappers=None):

    if picture_class is None:
        picture_class = get_picture_class 

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

        try:
            annots = annot_map[seq]
        except (KeyError, TypeError): # sequence not in map, or map is None
            continue
        
        new_map, max_text_length = \
                 convert_to_image_coords(seq, annots, p, default_color,
                                         wrappers[n])
        
        if new_map:
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
