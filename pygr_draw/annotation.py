from pygr import cnestedlist, seqdb
from pygr.nlmsa_utils import EmptyAlignmentError

class Annotation(object):
    def __init__(self, name, id, start, stop, color=None):
        self.name = name 
        self.id = id
        self.start = start
        self.stop = stop
        self.color = color

class AnnotationGroup(object):
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

default_arg = object()
class FeatureWrapper(object):
    def __init__(self, parent, feature, values):
        self.parent = parent            # factory class
        self.feature = feature          # *unwrapped* feature
        self.values = values            # override values, e.g. color

    def __getattr__(self, wrapped_feature, attrname, default=default_arg):
        # override?
        if attrname in self.values:
            return self.values[attrname]

        # nope; use getattr.
        if default is not default_arg:
            return getattr(self.feature, attrname, default)
        else:
            return getattr(self.feature, attrname)

class FeatureWrapperFactory(object):
    def __init__(self, klass=FeatureWrapper, **values):
        self.klass = klass
        self.values = values

    def __call__(self, feature):
        return self.klass(self, feature, self.values)

class SequenceWrapper(FeatureWrapper):
    def __getattr__(self, attrname, default=default_arg):
        # override?
        if attrname in self.values:
            return self.values[attrname]
        elif attrname == 'name':
            return self.feature.id

        # nope; use getattr.
        if default is not default_arg:
            return getattr(self.feature, attrname, default)
        else:
            return getattr(self.feature, attrname)


class SequenceWrapperFactory(FeatureWrapperFactory):
    def __init__(self, klass=SequenceWrapper, **values):
        FeatureWrapperFactory.__init__(self, klass=klass, **values)

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
    
    def __init__(self, name, start, stop,
                 annots, color, feature_start, text_length):
        self.id = 'bitmap'
        self.name = name
        
        self.annots = [(min(a), max(a)) for a in annots]

        self.start = start
        self.stop = stop

        self.feature_start = feature_start
        self.color = color
        self.text_length = text_length

def convert_to_image_coords(seq, slice, picture_obj, default_color,
                            wrapper):
    """
    @CTB
    """
    
    new_annot_d = convert_object_coords(slice, seq.start, len(seq),
                                        picture_obj, default_color, wrapper)

    # build nlmsa
    new_map = cnestedlist.NLMSA('test', mode='memory', use_virtual_lpo=True)

    # map them as annotations
    max_text_length = 0

    adb = seqdb.AnnotationDB(new_annot_d, picture_obj.genome)
    for v in adb.values():
        try:
            new_map.addAnnotation(v)
        except IndexError:
            continue

        z = v.feature_start - v.text_length
        if z < 0:
            max_text_length = max(max_text_length, -z)

    try:
        new_map.build()
    except EmptyAlignmentError:
        new_map = None
    
    return (new_map, max_text_length)

def convert_object_coords(slice, seq_start, seq_length, picture_obj,
                          default_color, wrapper):
    """
    Build a set of annotation objects in 'picture' coordinate space.
    
    'slice' is an NLMSASlice object containing the objects aligned to
    our sequence interval of interest.

    'seq_start' is the interval start, in parent path sequence coordinates.

    'seq_length' is the interval length (stop - start).

    'picture_obj' is the drawing object (e.g. BitmapSequencePicture).

    'default_color' is the default color.

    'wrapper' is a callable that returns an object that will be queried for
    name, color, group, and (if 'group' is true) annots attributes.
    """
    image_width = len(picture_obj.genome['bitmap'])
    length_ratio = float(image_width) / float(seq_length)

    d = {}
    
    for n, (seq, feature, _) in enumerate(slice.edges()):
        # Here, 'seq' is the source sequence, or the sequence to which
        # the annotation/alignment is aligned; 'feature' is the object
        # with information about the aligned sequence.
        
        if wrapper:
            feature = wrapper(feature)
            
        is_group = getattr(feature, 'group', False)
        color = getattr(feature, 'color', default_color)
        
        name = getattr(feature, 'name', '')
        text_size = picture_obj._calc_textsize(name)
        text_length = text_size[0]

        sequence = seq
        corrected_start = sequence.start - seq_start
        feature_start = float(corrected_start) * length_ratio

        block_start = feature_start - text_length
        block_start = int(round(block_start))
        block_start = max(block_start, 0)

        corrected_stop = sequence.stop - seq_start
        block_stop = float(corrected_stop) * length_ratio
        block_stop = int(round(block_stop))
        block_stop = max(block_stop, 0)

        # make sure features are at least size 1 even after scaling!
        if block_start == block_stop:
            block_stop += 1

        if not is_group:
            new_feature = _PictureCoordAnnot(name, block_start, block_stop,
                                           color, feature_start, text_length)
        else:
            # for group annotations, we need to transform sub-annotation
            # blocks into the right coordinate space, too.
            sub_annots = []

            for (start, stop) in feature.annots:
                new_start = start - seq_start
                new_start = float(new_start) * length_ratio
                new_stop = stop - seq_start
                new_stop = float(new_stop) * length_ratio

                new_start = int(round(new_start))
                new_stop = int(round(new_stop))

                new_start = max(new_start, 0)
                new_stop = max(new_stop, 0)

                sub_annots.append((new_start, new_stop))

            new_feature = _PictureCoordAnnotGroup(name, block_start, block_stop,
                                                  sub_annots, color,
                                                  feature_start, text_length)
            
        # add new 'picture' feature into dict...
        d[n] = new_feature

    return d
