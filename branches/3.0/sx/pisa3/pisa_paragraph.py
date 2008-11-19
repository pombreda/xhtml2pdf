#!/bin/env/python
# -*- coding: utf-8 -*-

"""
A paragraph class to be used with ReportLab Platypus.

TODO
====

- Bullets
- Links
- Borders and margins (Box)
- Underline, Background
- Images
- Hyphenation
+ Alignment
- Breakline, empty lines
+ TextIndent

"""

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import Color

class Style(dict):

    """
    Style
    """

    DEFAULT = {
        "textAlign": TA_LEFT,
        "textIndent": 0.0,
        "width": None,
        "height": None,
        "fontName": "Times-Roman",
        "fontSize": 10.0,
        "color": Color(0,0,0),
        }

    def __init__(self, **kw):
        self.update(self.DEFAULT)
        self.update(kw)
        self.spaceBefore = 0
        self.spaceAfter = 0
        self.keepWithNext = False

class Box(dict):

    """
    Box.

    Handles the following styles:

        backgroundColor
        paddingLeft, paddingRight, paddingTop, paddingBottom
        marginLeft, marginRight, marginTop, marginBottom
        borderLeftColor, borderLeftWidth, borderLeftColor, borderLeftStyle
        borderRightColor, borderRightWidth, borderRightColor, borderRightStyle
        borderTopColor, borderTopWidth, borderTopColor, borderTopStyle
        borderBottomColor, borderBottomWidth, borderBottomColor, borderBottomStyle

    """

    '''
    def wrap(self, availWidth, availHeight):

        style = self.style

        deltaWidth = style.paddingLeft + style.paddingRight + style.borderLeftWidth + style.borderRightWidth
        deltaHeight = style.paddingTop + style.paddingBottom + style.borderTopWidth + style.borderBottomWidth

        # reduce the available width & height by the padding so the wrapping
        # will use the correct size
        availWidth -= deltaWidth
        availHeight -= deltaHeight

        # Modify maxium image sizes
        self._calcImageMaxSizes(availWidth, self.getMaxHeight() - deltaHeight)

        # call the base class to do wrapping and calculate the size
        Paragraph.wrap(self, availWidth, availHeight)

        # increase the calculated size by the padding
        self.width += deltaWidth
        self.height += deltaHeight

        return (self.width, self.height)

    def draw(self):

        # Draw the background and borders here before passing control on to
        # ReportLab. This is because ReportLab can't handle the individual
        # components of the border independently. This will also let us
        # support more border styles eventually.
        canvas = self.canv
        style = self.style
        bg = style.backColor
        leftIndent = style.leftIndent
        bp = style.borderPadding

        x = leftIndent - bp
        y = - bp
        w = self.width - (leftIndent + style.rightIndent) + 2 * bp
        h = self.height + 2 * bp

        if bg:
            # draw a filled rectangle (with no stroke) using bg color
            canvas.saveState()
            canvas.setFillColor(bg)
            canvas.rect(x, y, w, h, fill=1, stroke=0)
            canvas.restoreState()

        # we need to hide the bg color (if any) so Paragraph won't try to draw it again
        style.backColor = None

        # offset the origin to compensate for the padding
        canvas.saveState()
        canvas.translate(
            (style.paddingLeft + style.borderLeftWidth),
            -1 * (style.paddingTop + style.borderTopWidth)) # + (style.leading / 4)))

        # Call the base class draw method to finish up
        Paragraph.draw(self)
        canvas.restoreState()

        # Reset color because we need it again if we run 2-PASS like we
        # do when using TOC
        style.backColor = bg

        canvas.saveState()

        def _drawBorderLine(bstyle, width, color, x1, y1, x2, y2):
            # We need width and border style to be able to draw a border
            if width and getBorderStyle(bstyle):
                # If no color for border is given, the text color is used (like defined by W3C)
                if color is None:
                    color = style.textColor
                # print "Border", bstyle, width, color
                if color is not None:
                    canvas.setStrokeColor(color)
                    canvas.setLineWidth(width)
                    canvas.line(x1, y1, x2, y2)

        _drawBorderLine(style.borderLeftStyle,
                        style.borderLeftWidth,
                        style.borderLeftColor,
                        x, y, x, y + h)
        _drawBorderLine(style.borderRightStyle,
                        style.borderRightWidth,
                        style.borderRightColor,
                        x + w, y, x + w, y + h)
        _drawBorderLine(style.borderTopStyle,
                        style.borderTopWidth,
                        style.borderTopColor,
                        x, y + h, x + w, y + h)
        _drawBorderLine(style.borderBottomStyle,
                        style.borderBottomWidth,
                        style.borderBottomColor,
                        x, y, x + w, y)

        canvas.restoreState()
    '''

class Fragment(Box):

    """
    Fragment.

    text:       String containing text
    fontName:
    fontSize:
    width:      Width of string
    height:     Height of string
    """

    # def __init__(self,

    def calc(self):
        """
        XXX Cache stringWith if not accelerated?!
        """
        self["width"] = stringWidth(self["text"], self["fontName"], self["fontSize"])

class Space(Fragment):

    def calc(self):
        self["width"] = stringWidth(" ", self["fontName"], self["fontSize"])

class LineBreak(Fragment):

    def calc(self):
        self["width"] = 0

class Image(Box):

    pass

ALIGNMENTS = (TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY)

class Line(list):

    """
    Container for line fragments.
    """

    LINEHEIGHT = 1.0

    def __init__(self, style):
        self.width = 0
        self.height = 0
        self.isLast = False
        self.style = style
        list.__init__(self)

    def doAlignment(self, width, alignment):
        " Apply alignment "
        if alignment != TA_LEFT:
            lineWidth = self[-1]["x"] + self[-1]["width"]
            emptySpace = width - lineWidth
            if alignment == TA_RIGHT:
                for j, frag in enumerate(self):
                    frag["x"] += emptySpace
            elif alignment == TA_CENTER:
                for j, frag in enumerate(self):
                    frag["x"] += emptySpace / 2.0
            elif alignment == TA_JUSTIFY and not self.isLast:
                delta = emptySpace / (len(self) - 1)
                for j, frag in enumerate(self):
                    frag["x"] += j * delta

    def doLayout(self, width):
        "Align words in previous line."

        # Calculate dimensions
        self.width = width
        self.height = self.lineHeight = max(frag["fontSize"] * self.LINEHEIGHT for frag in self)

        # Apply line height
        self.fontSize = max(frag["fontSize"] for frag in self)
        y = (self.lineHeight - self.fontSize) # / 2
        for frag in self:
            frag["y"] = y

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

    def __init__(self, data=[], style=None):
        self.lines = []
        self.width = 0
        self.height = 0
        self.maxWidth = 0
        self.maxHeight = 0
        self.style = style
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
            self.height += line.doLayout(self.width)
            self.minHeight = self.height
            self.lines.append(line)
        # Start in new line
        return 0, Line(self.style)

    def splitIntoLines(self, maxWidth, maxHeight, splitted=False):
        """
        Split text into lines and calculate X positions. If we need more
        space in height than available we return the rest of the text
        """
        self.lines = []
        self.height = 0
        self.maxWidth = self.width = maxWidth
        self.maxHeight = maxHeight

        style = self.style
        textIndent = style["textIndent"]
        x = textIndent

        pos = 0
        line = Line(style)
        for i, frag in enumerate(self):
            fragWidth = frag["width"]
            # Does it fit into current line?
            if isinstance(frag, LineBreak) or fragWidth + x > maxWidth:
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

        # Apply alignment
        self.lines[-1].isLast = True
        [line.doAlignment(maxWidth, style["textAlign"]) for line in self.lines]

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

    def __init__(self, text, style, debug=False, splitted=False, **kwDict):

        Flowable.__init__(self)
        # self._showBoundary = True

        self.text = text
        self.text.calc()
        self.style = style
        self.text.style = style

        self.debug = debug
        self.splitted = splitted

        # More attributes
        for k, v in kwDict.items():
            setattr(self, k, v)

        # set later...
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
        width = availWidth # - style.leftIndent - style.rightIndent
        self.splitIndex = self.text.splitIntoLines(width, availHeight)

        self.width, self.height = availWidth, self.text.height

        if self.debug:
            print "*** wrap (%f, %f) needed, splitIndex %r" % (self.width, self.height, self.splitIndex)

        return self.width, self.height

    #def visitFirstParagraph(self, para):
    #    return para

    #def visitOtherParagraph(self, para):
    #    return para

    def split(self, availWidth, availHeight):
        "Split ourself in two paragraphs."

        if self.debug:
            print "*** split (%f, %f)" % (availWidth, availHeight)

        splitted = []
        if self.splitIndex:
            text1 = self.text[:self.splitIndex]
            text2 = self.text[self.splitIndex:]
            p1 = Paragraph(Text(text1), self.style, debug=self.debug)
            p2 = Paragraph(Text(text2), self.style, debug=self.debug, splitted=True)
            splitted = [p1, p2]

            if self.debug:
                print "*** text1 %s / text %s" % (len(text1), len(text2))

        if self.debug:
            print '*** return %s' % self.splitted

        return splitted


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
                style.leftIndent,
                0,
                self.width,
                self.height,
                fill=1,
                stroke=1)

        y = 0
        dy = self.height
        for line in self.text.lines:
            y += line.height
            for frag in line:
                if frag.get("text", ""):
                    canvas.setFont(frag["fontName"], frag["fontSize"])
                    canvas.setFillColor(frag.get("color", style["color"]))
                    canvas.drawString(frag["x"], dy - y + frag["y"], frag["text"])

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
        text = Text(list(textGenerator(data, fn, fs)))
        return text

    def test():
        doc = SimpleDocTemplate("test.pdf")
        story = []

        style = Style(fontName = "Helvetica", textIndent = 24.0)
        fn = style["fontName"]
        fs = style["fontSize"]
        sampleText1 = createText(TEXT[:100], fn, fs)
        sampleText2 = createText(TEXT[100:], fn, fs)

        text = Text(sampleText1 + [
            Space(
                fontName = fn,
                fontSize = fs),
            Fragment(
                text = "TrennbarTrennbar",
                pairs = [("Trenn-", "barTrennbar")],
                fontName = fn,
                fontSize = fs),
            Space(
                fontName = fn,
                fontSize = fs),
            Fragment(
                text = "Normal",
                color = Color(1,0,0),
                fontName = fn,
                fontSize = fs),
            Space(
                fontName = fn,
                fontSize = fs),
            Fragment(
                text = "gGrößer",
                fontName = fn,
                fontSize = fs * 1.5),
            Space(
                fontName = fn,
                fontSize = fs),
            Fragment(
                text = "Bold",
                fontName = "Times-Bold",
                fontSize = fs),
            Space(
                fontName = fn,
                fontSize = fs),
            Fragment(
                text = "jItalic",
                fontName = "Times-Italic",
                fontSize = fs),
            Space(
                fontName = fn,
                fontSize = fs),
            LineBreak(
                fontName = fn,
                fontSize = fs),
            LineBreak(
                fontName = fn,
                fontSize = fs),
            ] + sampleText2)

        story.append(Paragraph(
            copy.copy(text),
            style,
            debug = 0))

        for i in range(10):
            style = copy.deepcopy(style)
            style["textAlign"] = ALIGNMENTS[i % 4]
            text = createText(("(%d) " % i) + TEXT, fn, fs)
            story.append(Paragraph(
                copy.copy(text),
                style,
                debug = 0))
        doc.build(story)

    test()
    os.system("start test.pdf")

    # createText(TEXT, styles["Normal"].fontName, styles["Normal"].fontSize)
