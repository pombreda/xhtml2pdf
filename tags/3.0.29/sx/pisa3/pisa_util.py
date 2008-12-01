# -*- coding: ISO-8859-1 -*-
#############################################
## (C)opyright by Dirk Holtwick, 2002-2007 ##
## All rights reserved                     ##
#############################################

__reversion__ = "$Revision: 20 $"
__author__    = "$Author: holtwick $"
__date__      = "$Date: 2007-10-09 12:58:24 +0200 (Di, 09 Okt 2007) $"

from reportlab.lib.units import inch, cm
from reportlab.lib.styles import *
from reportlab.lib.enums import *
from reportlab.lib.colors import *
from reportlab.lib.pagesizes import *
from reportlab.pdfbase import pdfmetrics

# from reportlab.platypus import *
# from reportlab.platypus.flowables import Flowable
# from reportlab.platypus.tableofcontents import TableOfContents
# from reportlab.platypus.para import Para, PageNumberObject, UNDERLINE, HotLink

import reportlab
import copy
import types
import os
import os.path
import pprint
import sys
import string
import re

rgb_re = re.compile("^.*?rgb[(]([0-9]+).*?([0-9]+).*?([0-9]+)[)].*?[ ]*$")

if not(reportlab.Version[0] == "2" and reportlab.Version[2]>="1"):
    raise ImportError("Reportlab Version 2.1+ is needed!")

REPORTLAB22 = (reportlab.Version[0] == "2" and reportlab.Version[2] >= "2")
# print "***", reportlab.Version, REPORTLAB22, reportlab.__file__

import logging
log = logging.getLogger("ho.pisa")

try:
    import cStringIO as StringIO
except:
    import StringIO

try:
    import pyPdf
except:
    pyPdf = None

try:
    from reportlab.graphics import renderPM
except:
    renderPM = None

try:
    from reportlab.graphics import renderSVG
except:
    renderSVG = None

def ErrorMsg():
    """
    Helper to get a nice traceback as string
    """
    import traceback, sys, cgi
    type = value = tb = limit = None
    type, value, tb = sys.exc_info()
    list = traceback.format_tb(tb, limit) + traceback.format_exception_only(type, value)
    return "Traceback (innermost last):\n" + "%-20s %s" % (
        string.join(list[:-1], ""),
        list[-1])

def toList(value):
    if type(value) not in (types.ListType, types.TupleType):
        return [value]
    return list(value)

def flatten(x):
    """flatten(sequence) -> list

    copied from http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def _toColor(arg, default=None):
    '''try to map an arbitrary arg to a color instance'''
    if isinstance(arg, Color): return arg
    tArg = type(arg)
    if tArg in (types.ListType, types.TupleType):
        assert 3<=len(arg)<=4, 'Can only convert 3 and 4 sequences to color'
        assert 0<=min(arg) and max(arg)<=1
        return len(arg)==3 and Color(arg[0], arg[1], arg[2]) or CMYKColor(arg[0], arg[1], arg[2], arg[3])
    elif tArg == types.StringType:
        C = getAllNamedColors()
        s = arg.lower()
        if C.has_key(s): return C[s]
        try:
            return toColor(eval(arg))
        except:
            pass
    try:
        return HexColor(arg)
    except:
        if default is None:
            raise ValueError('Invalid color value %r' % arg)
        return default

def getColor(value, default=None):
    " Convert to color value "
    try:
        original = value
        if isinstance(value, Color):
            return value
        value = str(value).strip().lower()
        if value=="transparent" or value=="none":
            return default
        if value in COLOR_BY_NAME:
            return COLOR_BY_NAME[value]
        if value.startswith("#") and len(value)==4:
            value = "#" + value[1] + value[1] + value[2] + value[2] + value[3] + value[3]
        elif rgb_re.search(value):
            # e.g., value = "<css function: rgb(153, 51, 153)>", go figure:
            r, g, b = [int(x) for x in rgb_re.search(value).groups()]
            value = "#%02x%02x%02x" % (r, g, b)
        else:
            # Shrug
            pass

        # XXX Throws illegal in 2.1 e.g. toColor('none'),
        # therefore we have a workaround here
        return _toColor(value)
    except ValueError, e:
        log.warn("Unknown color %r", original)
    return default

def getBorderStyle(value, default=None):
    # log.debug(value)
    if value and (str(value).lower() not in ("none", "hidden")):
        return value
    return default

mm = cm / 10.0
dpi96 = (1.0 / 96.0 * inch)

_absoluteSizeTable = {
    "1": 50.0/100.0,
    "xx-small": 50.0/100.0,
    "x-small": 50.0/100.0,
    "2": 75.0/100.0,
    "small": 75.0/100.0,
    "3": 100.0/100.0,
    "medium": 100.0/100.0,
    "4": 125.0/100.0,
    "large": 125.0/100.0,
    "5": 150.0/100.0,
    "x-large": 150.0/100.0,
    "6": 175.0/100.0,
    "xx-large": 175.0/100.0,
    "7": 200.0/100.0,
    "xxx-large": 200.0/100.0,
    #"xx-small" : 3./5.,
    #"x-small": 3./4.,
    #"small": 8./9.,
    #"medium": 1./1.,
    #"large": 6./5.,
    #"x-large": 3./2.,
    #"xx-large": 2./1.,
    #"xxx-large": 3./1.,
}

_relativeSizeTable = {
    "larger": 1.25,
    "smaller": 0.75,
    "+4": 200.0/100.0,
    "+3": 175.0/100.0,
    "+2": 150.0/100.0,
    "+1": 125.0/100.0,
    "-1": 75.0/100.0,
    "-2": 50.0/100.0,
    "-3": 25.0/100.0,
    }

MIN_FONT_SIZE = 1.0

def getSize(value, relative=0, base=None, default=0.0):
    """
    Converts strings to standard sizes
    """
    try:
        original = value
        if value is None:
            return relative
        elif type(value) is types.FloatType:
            return value
        elif type(value) is types.IntType:
            return float(value)
        elif type(value) in (types.TupleType, types.ListType):
            value = "".join(value)
        value = str(value).strip().lower().replace(",", ".")
        if value[-2:]=='cm':
            return float(value[:-2].strip()) * cm
        elif value[-2:]=='mm':
            return (float(value[:-2].strip()) * mm) # 1mm = 0.1cm
        elif value[-2:]=='in':
            return float(value[:-2].strip()) * inch # 1pt == 1/72inch
        elif value[-2:]=='inch':
            return float(value[:-4].strip()) * inch # 1pt == 1/72inch
        elif value[-2:]=='pt':
            return float(value[:-2].strip())
        elif value[-2:]=='pc':
            return float(value[:-2].strip()) * 12.0 # 1pc == 12pt
        elif value[-2:]=='px':
            return float(value[:-2].strip()) * dpi96 # XXX W3C says, use 96pdi http://www.w3.org/TR/CSS21/syndata.html#length-units
        elif value[-1:]=='i':  # 1pt == 1/72inch
            return float(value[:-1].strip()) * inch
        elif value in ("none", "0", "auto"):
            return 0.0
        elif relative:
            if value[-2:]=='em': # XXX
                return (float(value[:-2].strip()) * relative) # 1em = 1 * fontSize
            elif value[-2:]=='ex': # XXX
                return (float(value[:-2].strip()) * (relative/2.0)) # 1ex = 1/2 fontSize
            elif value[-1:]=='%':
                # print "%", value, relative, (relative * float(value[:-1].strip())) / 100.0
                return (relative * float(value[:-1].strip())) / 100.0 # 1% = (fontSize * 1) / 100
            elif value in ("normal", "inherit"):
                return relative
            elif _relativeSizeTable.has_key(value):
                if base:
                    return max(MIN_FONT_SIZE, base * _relativeSizeTable[value])
                return max(MIN_FONT_SIZE, relative * _relativeSizeTable[value])
            elif _absoluteSizeTable.has_key(value):
                if base:
                    return max(MIN_FONT_SIZE, base * _absoluteSizeTable[value])
                return max(MIN_FONT_SIZE, relative * _absoluteSizeTable[value])
        try:
            value = float(value)
        except:
            log.warn("getSize: Not a float %r", value)
            return default #value = 0
        return max(0, value)
    except Exception:
        log.warn("getSize %r %r", original, relative, exc_info=1)
        # print "ERROR getSize", repr(value), repr(value), e
        return default

def getCoords(x, y, w, h, pagesize):
    """
    As a stupid programmer I like to use the upper left
    corner of the document as the 0,0 coords therefore
    we need to do some fancy calculations
    """
    #~ print pagesize
    ax, ay = pagesize
    if x < 0:
        x = ax + x
    if y < 0:
        y = ay + y
    if w != None and h != None:
        if w <= 0:
            w = (ax - x + w)
        if h <= 0:
            h = (ay - y + h)
        return x, (ay - y - h), w, h
    return x, (ay - y)

def getBox(box, pagesize):
    """
    Parse sizes by corners in the form:
    <X-Left> <Y-Upper> <Width> <Height>
    The last to values with negative values are interpreted as offsets form
    the right and lower border.
    """
    box = str(box).split()
    if len(box)!=4:
        raise Exception, "box not defined right way"
    x, y, w, h = map(getSize, box)
    return getCoords(x, y, w, h, pagesize)

def getPos(position, pagesize):
    """
    Pair of coordinates
    """
    position = str(position).split()
    if len(position)!=2:
        raise Exception, "position not defined right way"
    x, y = map(getSize, position)
    return getCoords(x, y, None, None, pagesize)

def getBool(s):
    " Is it a boolean? "
    return str(s).lower() in ("y", "yes", "1", "true")

_uid = 0
def getUID():
    " Unique ID "
    global _uid
    _uid += 1
    return str(_uid)

_alignments = {
    "left": TA_LEFT,
    "center": TA_CENTER,
    "middle": TA_CENTER,
    "right": TA_RIGHT,
    "justify": TA_JUSTIFY,
    }

def getAlign(value, default=TA_LEFT):
    return _alignments.get(str(value).lower(), default)

#def getVAlign(value):
#    # Unused
#    return str(value).upper()

import base64
import re
import urlparse
import mimetypes
import urllib2

_rx_datauri = re.compile("^data:(?P<mime>[a-z]+/[a-z]+);base64,(?P<data>.*)$", re.M|re.DOTALL)

class pisaFileObject:

    """
    XXX
    """

    def __init__(self, uri, basepath=None):
        self.basepath = basepath
        self.mimetype = None
        self.file = None
        self.data = None
        self.uri = None
        self.local = None
        uri = str(uri)

        # Data URI
        if uri.startswith("data:"):
            m = _rx_datauri.match(uri)
            self.mimetype = m.group("mime")
            self.data = base64.decodestring(m.group("data"))

        else:

            # Check if we have an external scheme
            if basepath:
                urlParts = urlparse.urlparse(basepath)
            else:
                urlParts = urlparse.urlparse(uri)

            # Drive letters have len==1 but we are looking for things like http:
            if len(urlParts[0])>1:

                # External data
                if basepath:
                    uri = urlparse.urljoin(basepath, uri)

                #path = urlparse.urlsplit(url)[2]
                #mimetype = getMimeType(path)
                urlResponse = urllib2.urlopen(uri)
                self.mimetype = urlResponse.info().get("Content-Type", None).split(";")[0]
                self.uri = urlResponse.geturl()
                self.file = urlResponse

            else:

                # Local data
                if basepath:
                    uri = os.path.normpath(os.path.join(basepath, uri))

                if os.path.isfile(uri):
                    self.uri = uri
                    self.local = uri
                    self.setMimeTypeByName(uri)
                    self.file = open(uri, "rb")

    def getFile(self):
        if self.file is not None:
            return self.file
        if self.data is not None:
            return StringIO.StringIO(self.data)
        return None

    def getData(self):
        if self.data is not None:
            return self.data
        if self.file is not None:
            self.data = self.file.read()
            return self.data
        return None

    def notFound(self):
        return (self.file is None) and (self.data is None)

    def setMimeTypeByName(self, name):
        " Guess the mime type "
        mimetype = mimetypes.guess_type(name)[0]
        if mimetype is not None:
            self.mimetype = mimetypes.guess_type(name)[0].split(";")[0]

def getFile(*a , **kw):
    file = pisaFileObject(*a, **kw)
    if file.notFound():
        return None
    return file

COLOR_BY_NAME = {
 'activeborder': Color(212,208,200),
 'activecaption': Color(10,36,106),
 'aliceblue': Color(.941176,.972549,1),
 'antiquewhite': Color(.980392,.921569,.843137),
 'appworkspace': Color(128,128,128),
 'aqua': Color(0,1,1),
 'aquamarine': Color(.498039,1,.831373),
 'azure': Color(.941176,1,1),
 'background': Color(58,110,165),
 'beige': Color(.960784,.960784,.862745),
 'bisque': Color(1,.894118,.768627),
 'black': Color(0,0,0),
 'blanchedalmond': Color(1,.921569,.803922),
 'blue': Color(0,0,1),
 'blueviolet': Color(.541176,.168627,.886275),
 'brown': Color(.647059,.164706,.164706),
 'burlywood': Color(.870588,.721569,.529412),
 'buttonface': Color(212,208,200),
 'buttonhighlight': Color(255,255,255),
 'buttonshadow': Color(128,128,128),
 'buttontext': Color(0,0,0),
 'cadetblue': Color(.372549,.619608,.627451),
 'captiontext': Color(255,255,255),
 'chartreuse': Color(.498039,1,0),
 'chocolate': Color(.823529,.411765,.117647),
 'coral': Color(1,.498039,.313725),
 'cornflowerblue': Color(.392157,.584314,.929412),
 'cornsilk': Color(1,.972549,.862745),
 'crimson': Color(.862745,.078431,.235294),
 'cyan': Color(0,1,1),
 'darkblue': Color(0,0,.545098),
 'darkcyan': Color(0,.545098,.545098),
 'darkgoldenrod': Color(.721569,.52549,.043137),
 'darkgray': Color(.662745,.662745,.662745),
 'darkgreen': Color(0,.392157,0),
 'darkgrey': Color(.662745,.662745,.662745),
 'darkkhaki': Color(.741176,.717647,.419608),
 'darkmagenta': Color(.545098,0,.545098),
 'darkolivegreen': Color(.333333,.419608,.184314),
 'darkorange': Color(1,.54902,0),
 'darkorchid': Color(.6,.196078,.8),
 'darkred': Color(.545098,0,0),
 'darksalmon': Color(.913725,.588235,.478431),
 'darkseagreen': Color(.560784,.737255,.560784),
 'darkslateblue': Color(.282353,.239216,.545098),
 'darkslategray': Color(.184314,.309804,.309804),
 'darkslategrey': Color(.184314,.309804,.309804),
 'darkturquoise': Color(0,.807843,.819608),
 'darkviolet': Color(.580392,0,.827451),
 'deeppink': Color(1,.078431,.576471),
 'deepskyblue': Color(0,.74902,1),
 'dimgray': Color(.411765,.411765,.411765),
 'dimgrey': Color(.411765,.411765,.411765),
 'dodgerblue': Color(.117647,.564706,1),
 'firebrick': Color(.698039,.133333,.133333),
 'floralwhite': Color(1,.980392,.941176),
 'forestgreen': Color(.133333,.545098,.133333),
 'fuchsia': Color(1,0,1),
 'gainsboro': Color(.862745,.862745,.862745),
 'ghostwhite': Color(.972549,.972549,1),
 'gold': Color(1,.843137,0),
 'goldenrod': Color(.854902,.647059,.12549),
 'gray': Color(.501961,.501961,.501961),
 'graytext': Color(128,128,128),
 'green': Color(0,.501961,0),
 'greenyellow': Color(.678431,1,.184314),
 'grey': Color(.501961,.501961,.501961),
 'highlight': Color(10,36,106),
 'highlighttext': Color(255,255,255),
 'honeydew': Color(.941176,1,.941176),
 'hotpink': Color(1,.411765,.705882),
 'inactiveborder': Color(212,208,200),
 'inactivecaption': Color(128,128,128),
 'inactivecaptiontext': Color(212,208,200),
 'indianred': Color(.803922,.360784,.360784),
 'indigo': Color(.294118,0,.509804),
 'infobackground': Color(255,255,225),
 'infotext': Color(0,0,0),
 'ivory': Color(1,1,.941176),
 'khaki': Color(.941176,.901961,.54902),
 'lavender': Color(.901961,.901961,.980392),
 'lavenderblush': Color(1,.941176,.960784),
 'lawngreen': Color(.486275,.988235,0),
 'lemonchiffon': Color(1,.980392,.803922),
 'lightblue': Color(.678431,.847059,.901961),
 'lightcoral': Color(.941176,.501961,.501961),
 'lightcyan': Color(.878431,1,1),
 'lightgoldenrodyellow': Color(.980392,.980392,.823529),
 'lightgray': Color(.827451,.827451,.827451),
 'lightgreen': Color(.564706,.933333,.564706),
 'lightgrey': Color(.827451,.827451,.827451),
 'lightpink': Color(1,.713725,.756863),
 'lightsalmon': Color(1,.627451,.478431),
 'lightseagreen': Color(.12549,.698039,.666667),
 'lightskyblue': Color(.529412,.807843,.980392),
 'lightslategray': Color(.466667,.533333,.6),
 'lightslategrey': Color(.466667,.533333,.6),
 'lightsteelblue': Color(.690196,.768627,.870588),
 'lightyellow': Color(1,1,.878431),
 'lime': Color(0,1,0),
 'limegreen': Color(.196078,.803922,.196078),
 'linen': Color(.980392,.941176,.901961),
 'magenta': Color(1,0,1),
 'maroon': Color(.501961,0,0),
 'mediumaquamarine': Color(.4,.803922,.666667),
 'mediumblue': Color(0,0,.803922),
 'mediumorchid': Color(.729412,.333333,.827451),
 'mediumpurple': Color(.576471,.439216,.858824),
 'mediumseagreen': Color(.235294,.701961,.443137),
 'mediumslateblue': Color(.482353,.407843,.933333),
 'mediumspringgreen': Color(0,.980392,.603922),
 'mediumturquoise': Color(.282353,.819608,.8),
 'mediumvioletred': Color(.780392,.082353,.521569),
 'menu': Color(212,208,200),
 'menutext': Color(0,0,0),
 'midnightblue': Color(.098039,.098039,.439216),
 'mintcream': Color(.960784,1,.980392),
 'mistyrose': Color(1,.894118,.882353),
 'moccasin': Color(1,.894118,.709804),
 'navajowhite': Color(1,.870588,.678431),
 'navy': Color(0,0,.501961),
 'oldlace': Color(.992157,.960784,.901961),
 'olive': Color(.501961,.501961,0),
 'olivedrab': Color(.419608,.556863,.137255),
 'orange': Color(1,.647059,0),
 'orangered': Color(1,.270588,0),
 'orchid': Color(.854902,.439216,.839216),
 'palegoldenrod': Color(.933333,.909804,.666667),
 'palegreen': Color(.596078,.984314,.596078),
 'paleturquoise': Color(.686275,.933333,.933333),
 'palevioletred': Color(.858824,.439216,.576471),
 'papayawhip': Color(1,.937255,.835294),
 'peachpuff': Color(1,.854902,.72549),
 'peru': Color(.803922,.521569,.247059),
 'pink': Color(1,.752941,.796078),
 'plum': Color(.866667,.627451,.866667),
 'powderblue': Color(.690196,.878431,.901961),
 'purple': Color(.501961,0,.501961),
 'red': Color(1,0,0),
 'rosybrown': Color(.737255,.560784,.560784),
 'royalblue': Color(.254902,.411765,.882353),
 'saddlebrown': Color(.545098,.270588,.07451),
 'salmon': Color(.980392,.501961,.447059),
 'sandybrown': Color(.956863,.643137,.376471),
 'scrollbar': Color(212,208,200),
 'seagreen': Color(.180392,.545098,.341176),
 'seashell': Color(1,.960784,.933333),
 'sienna': Color(.627451,.321569,.176471),
 'silver': Color(.752941,.752941,.752941),
 'skyblue': Color(.529412,.807843,.921569),
 'slateblue': Color(.415686,.352941,.803922),
 'slategray': Color(.439216,.501961,.564706),
 'slategrey': Color(.439216,.501961,.564706),
 'snow': Color(1,.980392,.980392),
 'springgreen': Color(0,1,.498039),
 'steelblue': Color(.27451,.509804,.705882),
 'tan': Color(.823529,.705882,.54902),
 'teal': Color(0,.501961,.501961),
 'thistle': Color(.847059,.74902,.847059),
 'threeddarkshadow': Color(64,64,64),
 'threedface': Color(212,208,200),
 'threedhighlight': Color(255,255,255),
 'threedlightshadow': Color(212,208,200),
 'threedshadow': Color(128,128,128),
 'tomato': Color(1,.388235,.278431),
 'turquoise': Color(.25098,.878431,.815686),
 'violet': Color(.933333,.509804,.933333),
 'wheat': Color(.960784,.870588,.701961),
 'white': Color(1,1,1),
 'whitesmoke': Color(.960784,.960784,.960784),
 'window': Color(255,255,255),
 'windowframe': Color(0,0,0),
 'windowtext': Color(0,0,0),
 'yellow': Color(1,1,0),
 'yellowgreen': Color(.603922,.803922,.196078)}

