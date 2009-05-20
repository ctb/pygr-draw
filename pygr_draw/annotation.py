from pygr import cnestedlist, seqdb

TEXT_OFFSET = 6

class Annotation:
    def __init__(self, name, id, start, stop, color=None):
        self.name = name 
        self.id = id
        self.start = start
        self.stop = stop
        self.color = color

class AnnotationGroup:
    group = True
    
    def __init__(self, name, seq, annots, color=None):
        self.name = name
        self.id = seq

        # put the start/stop for the sub-annots in order
        self.annots = [ (min(a), max(a)) for a in annots ]

        start = min([ a[0] for a in annots ])
        stop = max([ a[1] for a in annots ])
        
        self.start = min(start, stop) 
        self.stop = max(start, stop)

        self.color = color

###

class _PictureCoordAnnot(object):
    group = False
    def __init__(self, name, start, stop, color, feature_start, text_length):
        self.id = 'bitmap'
        self.name = name
        self.start = start
        self.stop = stop
        self.feature_start = feature_start
        self.color = color
        self.text_length = text_length

class _PictureCoordAnnotGroup(object):
    group = True
    
    def __init__(self, name, annots, color, feature_start, text_length):
        self.id = 'bitmap'
        self.name = name
        
        self.annots = [(min(a), max(a)) for a in annots]

        start = min([ a[0] for a in annots ])
        stop = max([ a[1] for a in annots ])
        
        self.start = min(start, stop) 
        self.stop = max(start, stop)

        self.feature_start = feature_start
        self.color = color
        self.text_length = text_length

def convert_to_image_coords(seq, all_annotations, picture_obj, default_color):
    """
    @CTB
    """
    
    new_annot_d = convert_object_coords(all_annotations, seq.start,
                                        len(seq), picture_obj,
                                        default_color)

    # build nlmsa
    new_map = cnestedlist.NLMSA('test', mode='memory', use_virtual_lpo=True)

    # map them as annotations
    max_text_length = 0

    adb = seqdb.AnnotationDB(new_annot_d, picture_obj.genome)
    for v in adb.values():
        new_map.addAnnotation(v)

        z = v.feature_start - v.text_length
        if z < 0:
            max_text_length = max(max_text_length, -z)

    new_map.build()
    return (new_map, max_text_length)

def convert_object_coords(all_annotations, seq_start, seq_length, picture_obj,
                          default_color):
    """
    @CTB
    """
    image_width = len(picture_obj.genome['bitmap'])
    length_ratio = float(image_width) / float(seq_length)

    d = {}
    
    for n, annot in enumerate(all_annotations):
        name = getattr(annot, 'name', '')
        is_group = getattr(annot, 'group', False)
        color = getattr(annot, 'color', default_color)
        
        text_length = picture_obj._calc_textsize(name)[0]

        corrected_start = annot.sequence.start - seq_start
        feature_start = float(corrected_start) * length_ratio

        corrected_start = annot.sequence.start - seq_start

        feature_start = float(corrected_start) * length_ratio
        block_start = feature_start - text_length
        block_start = int(round(block_start))
        block_start = max(block_start, 0)

        corrected_stop = annot.sequence.stop - seq_start
        block_stop = float(corrected_stop) * length_ratio
        block_stop = int(round(block_stop))
        block_stop = max(block_stop, 0)

        if not is_group:
            new_annot = _PictureCoordAnnot(name, block_start, block_stop,
                                           color, feature_start, text_length)
        else:
            # still have to transform annot blocks
            
            sub_annots = []

            for (start, stop) in annot.annots:
                new_start = start - seq_start
                new_start = float(new_start) * length_ratio
                new_stop = stop - seq_start
                new_stop = float(new_stop) * length_ratio

                new_start = int(round(new_start))
                new_stop = int(round(new_stop))

                new_start = max(new_start, 0)
                new_stop = max(new_stop, 0)

                sub_annots.append((new_start, new_stop))

            new_annot = _PictureCoordAnnotGroup(name, sub_annots, color,
                                                feature_start, text_length)
            
        # add into dict
        d[n] = new_annot

    return d
    
