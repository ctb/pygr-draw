# CTB: known bug in the final 'crop' (see 'finalize').  If the bitmap
# is extended by the crop, the extension will be black.  Half-assed
# solution: extend 'y' in the constructor, because it will be cropped
# to fit the max size anyway.

from stack import stack_annotations
from BaseSequencePicture import BaseSequencePicture

from cStringIO import StringIO
from PIL import Image, ImageDraw

class ColorList(object):
    pass

colors = ColorList()
colors.white = (255, 255, 255)
colors.red = (255, 0, 0)
colors.green = (0, 255, 0)
colors.blue = (0, 0, 255)
colors.orange = (255, 180, 0)
colors.purple = (255, 0, 255)
colors.black = (0, 0, 0)

class BitmapSequencePicture(BaseSequencePicture):
    SUFFIX = '.png'
    
    colors = colors
    
    SEQUENCE_HEIGHT = 2
    
    SEQUENCE_TICK_HEIGHT = 6
    SEQUENCE_TICK_WIDTH = 2
    
    SEQUENCE_BASE = 50                 # horizontal margin
    SEQUENCE_OFFSET = 50               # vertical margin
    SEQUENCE_TEXT_OFFSET = 48          # vertical margin for text

    FEATURE_HEIGHT = 8
    THIN_FEATURE_HEIGHT = 2
    THIN_FEATURE_OFFSET = 3
    FEATURE_SPACING = 12
    
    def __init__(self, sequence_length, size=(1000,5000)):
        self.size = size
        resolution = size[0] / 2        # good default?
        
        BaseSequencePicture.__init__(self, sequence_length, resolution)
        
        # for final y-cropping.
        self.max_y = 2*self.SEQUENCE_OFFSET + self.SEQUENCE_HEIGHT
        self.set_left_margin_offset(0)

    def set_left_margin_offset(self, x):
        x = int(x)
        self.left_margin_offset = x + self.SEQUENCE_BASE

        self.w = self.size[0] + x
        self.h = self.size[1]
        
        self.image = Image.new("RGB", (self.w + x, self.h), colors.white)
        self.draw = ImageDraw.Draw(self.image)

        canvas_width = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        self.seq_to_canvas = float(canvas_width) / float(self.resolution)
        
    def draw_sequence_line(self):
        start_x = self.left_margin_offset
        start_y = self.SEQUENCE_OFFSET + self.SEQUENCE_TICK_HEIGHT / 2 \
                  - self.SEQUENCE_HEIGHT / 2

        w = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        h = self.SEQUENCE_HEIGHT

        self.draw.rectangle((start_x, start_y, start_x + w, start_y + h),
                            fill=colors.black)

        self._calc_tick_spacing()
        n_ticks = self.sequence_length / self.TICKSPACING
        ticklocations = [ i * self.TICKSPACING for i in range(n_ticks + 1) ]

        start_y = self.SEQUENCE_OFFSET
        end_y = self.SEQUENCE_OFFSET + self.SEQUENCE_TICK_HEIGHT

        # conversion factor
        w = self.w - self.SEQUENCE_BASE - self.left_margin_offset
        seq_to_canvas = float(w) / float(self.sequence_length)

        for loc in ticklocations:
            start_x = self.left_margin_offset + int(loc * seq_to_canvas)
            
            end_x = start_x + self.SEQUENCE_TICK_WIDTH
            self.draw.rectangle((start_x, start_y, end_x, end_y),
                                fill=colors.black)
        
    def _draw_feature(self, slot, start, stop, color=None, name=''):
        if color is None:
            color = self.colors.red

        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING

        start_x = int(start*self.seq_to_canvas + 0.5) + self.left_margin_offset
        width = int( float(stop - start) * self.seq_to_canvas + 0.5 )
        width = max(width, 1)

        assert width > 0

        self.draw.rectangle((start_x, start_y,
                             start_x+width, start_y + self.FEATURE_HEIGHT),
                            fill=color, outline=colors.black)
        self.max_y = max(start_y + self.FEATURE_HEIGHT, self.max_y)

    def _draw_feature_name(self, name, start_x, slot):
        start_x = int( float(start_x) * self.seq_to_canvas + 0.5)
        start_x += self.left_margin_offset
        
        start_y = self.SEQUENCE_TEXT_OFFSET + (slot + 1)*self.FEATURE_SPACING

        xsize = self._calc_textsize(name)[0]
        self.draw.text((start_x - xsize, start_y), name, fill=colors.black)

    def _calc_textsize(self, text):
        return self.draw.textsize(text)

    def _draw_thin_feature(self, slot, start, stop, color=None):
        if color is None:
            color = self.colors.red
            
        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING +\
                  self.THIN_FEATURE_OFFSET

        start_x = int(start*self.seq_to_canvas+0.5) + self.left_margin_offset
        width = int( float(stop - start) * self.seq_to_canvas + 0.5)
        width = max(width, 1)

#        if width + start_x > self.w - self.SEQUENCE_OFFSET:
#            width = self.w - self.SEQUENCE_OFFSET - start_x

        self.draw.rectangle((start_x, start_y,
                             start_x+width, start_y + self.THIN_FEATURE_HEIGHT),
                            fill=color, outline=color)
        self.max_y = max(start_y + self.THIN_FEATURE_HEIGHT, self.max_y)

    def _draw_xy_plot(self, slot, start, stop, value_pairs, height=1,
                      color=None, fill=None):
        if color is None:
            color = self.colors.black

        y_base = self.SEQUENCE_OFFSET + ((slot+1) * self.FEATURE_SPACING)

        # point list to draw.
        pairs = []

        # are we drawing a filled histogram, or just a line plot?
        first_pos = value_pairs[0][0]
        first_x = int(first_pos * self.seq_to_canvas+0.5) + \
                  self.left_margin_offset

        y_bottom = y_base + (self.FEATURE_HEIGHT * height)

        pairs.append((first_x, y_bottom))

        # plot the interior points
        for (pos, value) in value_pairs:
            x = int(pos * self.seq_to_canvas+0.5) + self.left_margin_offset
            y = y_base + ((1.0 - value) * self.FEATURE_HEIGHT * height)

            pairs.append((x,y))

        pairs.append((x, y_bottom))

        # draw a filled histogram?
        if fill:
            self.draw.polygon(pairs, outline=color, fill=fill)
        else:
            self.draw.line(pairs, fill=color)

        # increment max_y (for later clipping) appropriately.
        self.max_y = self.max_y + self.FEATURE_SPACING*height

    def finalize(self):
        fp = StringIO()

        cropped_image = self.image.crop((0, 0, self.w, self.max_y + self.FEATURE_HEIGHT))
        cropped_image.save(fp, "PNG")

        return fp.getvalue()
