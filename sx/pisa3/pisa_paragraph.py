#!/bin/env/python
# -*- coding: utf-8 -*-

"A simple paragraph class to be used with ReportLab Platypus."

import re

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import Color

class Box(dict):

    """
    Box.
    """

    pass

class Fragment(Box):

    """
    Fragment.

    text:       String containing text
    fontName:
    fontSize:
    width:      Width of string
    height:     Height of string
    """

    def calc(self):
        """
        XXX Cache stringWith if not accelerated?!
        """
        self["width"] = stringWidth(self["text"], self["fontName"], self["fontSize"])

class Space(Fragment):

    def calc(self):
        self["width"] = stringWidth(" ", self["fontName"], self["fontSize"])

class Image(Box):

    pass

class Line(list):

    """
    Container for line fragments.
    """

    def __init__(self, firstElementPosition):
        self.width = 0
        self.height = 0
        self.firstElementPosition = firstElementPosition
        list.__init__(self)

    def doLayout(self, width, alignment, isLast=False):
        "Align words in previous line."

        # Calculate dimensions
        self.width = width
        self.height = max(frag["fontSize"] for frag in self)

        # Apply alignment
        if alignment != TA_LEFT:
            lineWidth = self[-1]["x"] + self[-1]["width"]
            emptySpace = width - lineWidth
            for j, frag in enumerate(self):
                x = frag["x"]
                if alignment == TA_RIGHT:
                    frag["x"] += emptySpace
                elif alignment == TA_CENTER:
                    frag["pos"] += emptySpace / 2.0
                elif alignment == TA_JUSTIFY:
                    # and not isLast and not self.isLast:
                    delta = emptySpace / (len(self) - 1)
                    frag["pos"] += j * delta

        return self.height

    def dumpFragments(self):
        for frag in self:
            print "%r[%.1f]" % (frag["text"], frag["x"]),
        print

class Text(list):

    """
    Container for text fragments.

    Helper functions for splitting text into lines and calculating sizes
    and positions.
    """

    def __init__(self, data=[]):
        self.lines = []
        self.width = 0
        self.height = 0
        self.maxWidth = 0
        self.maxHeight = 0
        self.minHeight = 0
        list.__init__(self, data)

    def calc(self):
        """
        Calculate sizes of fragments.
        """
        [word.calc() for word in self]

    def pushLine(self, line):
        """
        Push line on the line stack and return a new position and line Element.
        """
        # Remove trailing white spaces
        while line and isinstance(line[-1], Space):
            line.pop()
        # Add line to list
        if line:
            self.height += line.doLayout(self.width, self.alignment)
            self.minHeight = self.height
            self.lines.append(line)
        # Start in new line
        return 0, Line(999)

    def splitIntoLines(self, maxWidth, maxHeight, alignment = TA_LEFT):
        """
        Split text into lines and calculate X positions. If we need more
        space in height than available we return the rest of the text
        """
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.alignment = alignment
        x = 0
        pos = 0
        line = Line(0)
        for i, frag in enumerate(self):
            fragWidth = frag["width"]
            # Does it fit into current line?
            if fragWidth + x > maxWidth:
                x, line = self.pushLine(line)
                if self.height > maxHeight:
                    return pos
                pos = i
            # First element of line should not be a space
            if x==0 and isinstance(frag, Space):
                continue
            # Add fragment to line and update x
            frag["x"] = x
            x += fragWidth
            line.append(frag)
        self.pushLine(line)
        if self.height > maxHeight:
            return pos
        return None

    def dumpLines(self):
        """
        For debugging dump all line and their content
        """
        i = 0
        for line in self.lines:
            print "Line %d:" % i,
            line.dumpFragments()
            i += 1

class Paragraph(Flowable):
    """A simple Paragraph class respecting alignment.

    Does text without tags.

    Respects only the following global style attributes:
    fontName, fontSize, leading, firstLineIndent, leftIndent,
    rightIndent, textColor, alignment.
    (spaceBefore, spaceAfter are handled by the Platypus framework.)

    """

    def __init__(self, text, style, debug=False, **kwDict):

        Flowable.__init__(self)

        self.text = text
        self.text.calc()

        self.style = style
        self.debug = debug
        for k, v in kwDict.items():
            setattr(self, k, v)

        # set later...
        self.splitted = None
        self.splitIndex = None

    # overwritten methods from Flowable class

    def wrap(self, availWidth, availHeight):
        "Determine the rectangle this paragraph really needs."

        # memorize available space
        self.avWidth = availWidth
        self.avHeight = availHeight

        if self.debug:
            print "*** wrap (%f, %f)" % (availWidth, availHeight)

        if not self.text:
            if self.debug:
                print "*** wrap (%f, %f) needed" % (0, 0)
            return 0, 0

        style = self.style

        # Split lines
        width = availWidth - style.leftIndent - style.rightIndent
        self.splitIndex = self.text.splitIntoLines(width, availHeight, style.alignment)

        neededWidth, neededHeight = availWidth, self.text.height

        if self.debug:
            print "*** wrap (%f, %f) needed, splitIndex %r" % (neededWidth, neededHeight, self.splitIndex)

        return neededWidth, neededHeight

    #def visitFirstParagraph(self, para):
    #    return para

    #def visitOtherParagraph(self, para):
    #    return para

    def split(self, availWidth, availHeight):
        "Split ourself in two paragraphs."

        if self.debug:
            print "*** split (%f, %f)" % (availWidth, availHeight)

        if self.splitIndex:
            text1 = self.text[:self.splitIndex]
            text2 = self.text[self.splitIndex:]
            p1 = Paragraph(Text(text1), self.style, debug=self.debug)
            p2 = Paragraph(Text(text2), self.style, debug=self.debug)
            self.splitted = [p1, p2]

            if self.debug:
                print "*** text1 %s / text %s" % (len(text1), len(text2))
        else:
            # don't split
            self.splitted = []

        if self.debug:
            print '*** return %s' % self.splitted

        return self.splitted


    def draw(self):
        "Render the content of the paragraph."

        if self.debug:
            print "*** draw"

        if not self.text:
            return

        canvas = self.canv
        style = self.style

        canvas.saveState()

        if self.debug:
            bw = 0.5
            bc = Color(1,1,0)
            bg = Color(0.9,0.9,0.9)
            canvas.setStrokeColor(bc)
            canvas.setLineWidth(bw)
            canvas.setFillColor(bg)
            canvas.rect(
                0,
                0,
                self.text.width,
                -self.text.height,
                fill=1,
                stroke=1)

        y = 0
        dy = self.text.height
        for line in self.text.lines:
            for frag in line:
                if not isinstance(frag, Space):
                    canvas.setFont(frag["fontName"], frag["fontSize"])
                    canvas.setFillColor(style.textColor)
                    canvas.drawString(frag["x"], dy - y, frag["text"])
            y += line.height

        canvas.restoreState()

if __name__=="__main__":
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.styles import *
    from reportlab.rl_config import *
    from reportlab.lib.units import *

    import os
    import copy
    import re
    import pprint

    styles = getSampleStyleSheet()

    TEXT = """
    Lörem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """.strip()

    def textGenerator(data, fn, fs):
        for word in re.split('\s+', data):
            if word:
                yield Fragment(
                    text = word,
                    fontName = fn,
                    fontSize = fs
                    )
                yield Space(
                    text = " ",
                    fontName = fn,
                    fontSize = fs
                    )

    def createText(data, fn, fs):
        text = Text()
        text += list(textGenerator(data, fn, fs))
        # text.calc()
        # pprint.pprint(text)
        # v = text.splitIntoLines(100, 20)
        # text.dumpLines()
        # print "###", len(v)
        return text

    def test():
        doc = SimpleDocTemplate("test.pdf")
        story = []

        style = styles["Normal"]
        text = createText(TEXT, style.fontName, style.fontSize)

        for i in range(10):
            text = createText(("(%d) " % i) + TEXT, style.fontName, style.fontSize)
            story.append(Paragraph(
                copy.copy(text),
                styles["Normal"],
                debug = True))
        doc.build(story)

    test()
    os.system("start test.pdf")

    # createText(TEXT, styles["Normal"].fontName, styles["Normal"].fontSize)
