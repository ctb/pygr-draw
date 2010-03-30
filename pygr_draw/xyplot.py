class SpanValue(object):
    def __init__(self, seq_id, start, width, value):
        self.id = seq_id
        self.start = start
        self.stop = start + width
        self.value = value

class SpanMap(object):
    def __init__(self, nlmsa, height=1, color=None):
        self.nlmsa = nlmsa
        self.height = height
        self.color = color

    def transform_coords_to_picture(self, seq, picture):
        image_width = len(picture.genome['bitmap'])
        length_ratio = float(image_width) / float(len(seq))

        try:
            slice = self.nlmsa[seq]
        except KeyError:
            pass

        values = slice.keys()

        pairs = []

        # first value: extend thru beginning
        v = values[0]
        pairs.append((min((v.sequence.start + v.sequence.stop) / 2, seq.start),
                      v.value))

        # intermediate values
        for v in values[1:-1]:
            pairs.append(((v.sequence.start + v.sequence.stop) / 2, v.value))

        # last value: extend to end
        v = values[-1]
        pairs.append((max((v.sequence.start + v.sequence.stop) / 2, seq.stop),
                      v.value))

        # scale to canvas coordinates.
        new_pairs = []
        for pos, value in pairs:
            new_pos = pos - seq.start
            new_pos = float(new_pos) * length_ratio
            new_pairs.append((new_pos, value))

        return new_pairs
