"""
Code & machinery for plotting (y) values against (x) sequence coordinates.

"""

class SpanValue(object):
    def __init__(self, seq_id, start, width, value):
        self.id = seq_id
        self.start = start
        self.stop = start + width
        self.value = value

class SpanMap(object):
    def __init__(self, nlmsa, height=1, line_color=None, fill_color=None):
        self.nlmsa = nlmsa
        self.height = height
        self.line_color = line_color
        self.fill_color = fill_color

    def transform_coords_to_picture(self, seq, picture):
        image_width = len(picture.genome['bitmap'])
        length_ratio = float(image_width) / float(len(seq))

        try:
            slice = self.nlmsa[seq]
        except KeyError:
            pass

        values = slice.keys()

        pairs = []

        # here, for the first and last points, we need to see if we got
        # SpanValue annotations that overlap the beginning and/or end of
        # the sequence interval.  If we did, extend the drawing to the
        # end(s) of the sequence interval; if not, that's fine, just
        # calculate to the midpoint.

        # first value: extend thru beginning, if it overlaps.
        v = values[0]
        if v.path.sequence.start <= seq.start:
            pairs.append((seq.start, v.value))
        else:
            pairs.append(((v.sequence.start + v.sequence.stop) / 2, v.value))

        # intermediate values
        for v in values[1:-1]:
            pairs.append(((v.sequence.start + v.sequence.stop) / 2, v.value))

        # last value: extend to end?
        v = values[-1]
        if v.path.sequence.stop >= seq.stop: # passes end of seq, extend.
            pairs.append((seq.stop, v.value))
        else:
            # just use the midpoint.
            pairs.append(((v.sequence.start + v.sequence.stop) / 2, v.value))

        # scale to canvas coordinates.
        new_pairs = []
        for pos, value in pairs:
            new_pos = pos - seq.start
            new_pos = float(new_pos) * length_ratio
            new_pairs.append((new_pos, value))

        return new_pairs

def build_span_value_list(sequence, nlmsa, resolution):
    try:
        slice = nlmsa[sequence]
    except KeyError:
        return None

    features = slice.keys()

    feature_start = min([ f.sequence.start for f in features ])
    feature_stop = max([ f.sequence.stop for f in features ])

    path = sequence.path
    value_list = []
    max_count = 0
    for i in range(feature_start, feature_stop, resolution):
        ival = path[i:i+resolution]
        try:
            count = len(nlmsa[ival])
            if count > max_count:
                max_count = count
        except KeyError:
            count = 0

        value_list.append((i, count))

    sv_list = []
    for (start, count) in value_list:
        ratio = count / float(max_count)
        sv_list.append(SpanValue(sequence.id, start, resolution, ratio))

    return sv_list
