from stack import stack_annotations
from BaseSequencePicture import BaseSequencePicture

from cStringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors

class PDFSequencePicture(BaseSequencePicture):
    SUFFIX = '.pdf'
    
    colors = colors
    
    SEQUENCE_HEIGHT = 2
    
    SEQUENCE_TICK_HEIGHT = 6
    SEQUENCE_TICK_WIDTH = 2
    
    SEQUENCE_BASE = 100                 # horizontal margin
    SEQUENCE_OFFSET = 100               # vertical margin

    TEXT_OFFSET = 8
    
    FEATURE_HEIGHT = 8
    THIN_FEATURE_HEIGHT = 2
    THIN_FEATURE_OFFSET = 3
    FEATURE_SPACING = 12
    
    def __init__(self, sequence_length):
        self.w, self.h = landscape(letter)
        BaseSequencePicture.__init__(self, sequence_length, int(self.w))
        
        self.data_fp = StringIO()
        self.canvas = canvas.Canvas(self.data_fp, pagesize=(self.w,self.h))

        self.seqlen = sequence_length

        # conversion factor
        self.seq_to_canvas = float((self.w - 2*self.SEQUENCE_BASE) /
                                   self.resolution)
        print "AA",self.w,self.seqlen
        
    def draw_sequence_line(self):
        start_x = self.SEQUENCE_BASE
        start_y = self.SEQUENCE_OFFSET + self.SEQUENCE_TICK_HEIGHT / 2 -\
                  self.SEQUENCE_HEIGHT / 2
        start_y = self.h - start_y

        w = self.w - 2*self.SEQUENCE_BASE
        h = self.SEQUENCE_HEIGHT
        
        self.canvas.rect(start_x, start_y, w, -h, fill=1)

        ## draw ticks

        self._calc_tick_spacing()
        n_ticks = self.seqlen / self.TICKSPACING
        ticklocations = [ i * self.TICKSPACING for i in range(n_ticks + 1) ]

        start_y = self.SEQUENCE_OFFSET
        start_y = self.h - start_y
        
        h = -self.SEQUENCE_TICK_HEIGHT
        w = self.SEQUENCE_TICK_WIDTH

        for loc in ticklocations:
            print loc,w
            start_x = self.SEQUENCE_BASE + int(loc * self.seq_to_canvas / float(self.seqlen) * self.resolution)
            print start_x, self.seq_to_canvas
            self.canvas.rect(start_x, start_y, w, h, fill=1)

    def _calc_textsize(self, name):
        text_size = len(name)*7
        return [text_size]
    
    def _draw_feature(self, slot, start, stop, color=None, name=''):
        print "YY",slot,start,stop
        if color is None:
            color = self.colors.red
            
        start_y = (self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING)
        start_y = self.h - start_y

        start = int(self.seq_to_canvas * start)
        stop = int(self.seq_to_canvas * stop)
        
        start_x = start + self.SEQUENCE_BASE
        width = stop - start
        
        width = max(width, 1)

        print start, stop
        print self.seq_to_canvas
        assert width > 0

        self.canvas.setFillColor(color)
        self.canvas.setStrokeColor(self.colors.black)
        self.canvas.rect(start_x, start_y, width, -self.FEATURE_HEIGHT, fill=1)

    def _draw_feature_name(self, name, start_x, slot):
        start_y = self.SEQUENCE_OFFSET + self.TEXT_OFFSET + (slot + 1) * self.FEATURE_SPACING
        start_y = self.h - start_y
        start_x = start_x + self.SEQUENCE_BASE - self._calc_textsize(name)[0]
        self.canvas.setFillColor(self.colors.black)
        self.canvas.drawString(start_x, start_y, name)

    def _draw_thin_feature(self, slot, start, stop, color=None):
        print "XX",slot,start,stop
        if color is None:
            color = self.colors.red
            
        start_y = self.SEQUENCE_OFFSET + (slot+1)*self.FEATURE_SPACING +\
                  self.THIN_FEATURE_OFFSET
        start_y = self.h - start_y

        start = int(self.seq_to_canvas * start)
        stop = int(self.seq_to_canvas * stop)

        start_x = start + self.SEQUENCE_BASE
        width = stop - start
        width = max(width, 1)

        if width + start_x > self.w - self.SEQUENCE_BASE:
            width = self.w - self.SEQUENCE_BASE - start_x

        self.canvas.setFillColor(color)
        self.canvas.setStrokeColor(color)
        self.canvas.rect(start_x, start_y, width, -self.THIN_FEATURE_HEIGHT,
                         fill=1)

    def finalize(self):
        self.canvas.showPage()
        self.canvas.save()
        return self.data_fp.getvalue()
