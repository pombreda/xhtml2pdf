# -*- coding: ISO-8859-1 -*-
#############################################
## (C)opyright by Dirk Holtwick, 2002-2007 ##
## All rights reserved                     ##
#############################################

__reversion__ = "$Revision: 20 $"
__author__    = "$Author: holtwick $"
__date__      = "$Date: 2007-10-09 12:58:24 +0200 (Di, 09 Okt 2007) $"

from reportlab.lib.pagesizes import *

PML_WARNING = "warning"
PML_ERROR = "error"
PML_EXCEPTION = "PML Exception"
PML_PREFIX = "pdf:"

#CLASS   = 1
BOOL    = 2
FONT    = 3
COLOR   = 4
FILE    = 5
SIZE    = 6
INT     = 7
STRING  = 8
BOX     = 9
POS     = 10
#STYLE   = 11
MUST    = 23

"""
Definition of all known tags. Also used for building the reference
"""

TAGS = {

    # FORMAT

    #"document": (1, {
    #    "format":               (["a0", "a1", "a2", "a3", "a4", "a5", "a6",
    #                              "b0", "b1", "b2", "b3", "b4", "b5", "b6",
    #                              "letter", "legal", "elevenseventeen"], "a4"),
    #    "orientation":          ["portrait", "landscape"],
    #    "fullscreen":           (BOOL, "0"),
    #    "author":               (STRING, ""),
    #    "subject":              (STRING, ""),
    #    "title":                (STRING, ""),
    #    "duration":             INT,
    #    "showoutline":          (BOOL, "0"),
    #    "outline":              INT,
    #    }),

    "pdftemplate": (1, {
        "name":                 (STRING, "body"),
        "format":               (["a0", "a1", "a2", "a3", "a4", "a5", "a6",
                                  "b0", "b1", "b2", "b3", "b4", "b5", "b6",
                                  "letter", "legal", "elevenseventeen"], "a4"),
        "orientation":          ["portrait", "landscape"],
        "background":           FILE,
        }),

    "pdfframe": (0, {
        "name":                 (STRING, ""),
        "box":                  (BOX, MUST),
        "border":               (BOOL, "0"),
        "static":               (BOOL, "0"),
        }),

    #"static": (1, {
    #    "name":                 STRING,
    #    "box":                  (BOX, MUST),
    #    "border":               (BOOL, "0"),
    #    }),

    "pdfnexttemplate": (0, {
        "name":                 (STRING, "body"),
        }),

    "pdfnextpage": (0, {
        "name":                 (STRING, ""),
        # "background":           FILE,
        }),

    "pdfnextframe": (0, {}),

    "pdffont": (0, {
        "src":                  (FILE, MUST),
        "name":                 (STRING, MUST),
        # "print":                (BOOL, "0"),
        "encoding":             (STRING, "WinAnsiEncoding"),
        }),

    "pdfdrawline": (0, {
        "from":                 (POS, MUST),
        "to":                   (POS, MUST),
        "color":                (COLOR, "#000000"),
        "width":                (SIZE, 1),
        }),

    "drawpoint": (0, {
        "pos":                  (POS, MUST),
        "color":                (COLOR, "#000000"),
        "width":                (SIZE, 1),
        }),

    "pdfdrawlines": (0, {
        "coords":               (STRING, MUST),
        "color":                (COLOR, "#000000"),
        "width":                (SIZE, 1),
        }),

    "pdfdrawstring": (0, {
        "pos":                  (POS, MUST),
        "text":                 (STRING, MUST),
        "color":                (COLOR, "#000000"),
        "align":                (["left", "center", "right"], "right"),
        "valign":               (["top", "middle", "bottom"], "bottom"),
        # "class":                CLASS,
        "rotate":               (INT, "0"),
        }),

    "pdfdrawimg": (0, {
        "pos":                  (POS, MUST),
        "src":                  (FILE, MUST),
        "width":                SIZE,
        "height":               SIZE,
        "align":                (["left", "center", "right"], "right"),
        "valign":               (["top", "middle", "bottom"], "bottom"),
        }),

    "pdfspacer" : (0, {
        "height":               (SIZE, MUST),
        }),

    "pdfpagenumber": (0, {
        "example":              (STRING, "0"),
        }),

    "pdftoc": (0, {
        }),        

    "pdfversion": (0, {     
        }),
    
    "pdfkeeptogether": (1, {      
        }),

    "pdfkeepinframe": (1, {    
        "maxwidth":             SIZE,
        "maxheight":            SIZE,
        "mergespace":           (INT, 1),
        "mode":                 (["error", "overflow", "shrink", "truncate"], "shrink"),
        "name":                 (STRING, "")
        }),

    # The chart example, see pml_charts
    "pdfchart": (1, {
        "type":                 (["spider","bar"], "bar"),
        "strokecolor":          (COLOR, "#000000"),
        "width":                (SIZE, MUST),
        "height":               (SIZE, MUST),
        }),

    "pdfchartdata": (0, {
        "set":                  (STRING, MUST),
        "value":                (STRING),
        # "label":                (STRING),
        "strokecolor":          (COLOR),
        "fillcolor":            (COLOR),
        "strokewidth":          (SIZE),
        }),

    "pdfchartlabel": (0, {       
        "value":                (STRING, MUST),
       }),

    "pdfbarcode": (0, {
        "value":                (STRING, MUST),
        "align":                (["left", "center", "right"], "left"),
        }),     
                 
    # ========================================================
    
    "link": (0, {
        "href":                (STRING, MUST),
        "rel":                 (STRING, ""),
        "type":                (STRING, ""),
        "media":               (STRING, "screen"),
        "charset":             (STRING, "latin1"), # XXX Must be something else...
        }),

    "meta": (0, {
        "name":                (STRING, ""),
        "content":             (STRING, ""),
        }),
        
    "style": (0, {
        "type":                (STRING, ""),
        "media":               (STRING, "all"),
        }),

    "img": (0, {
        "src":                  (FILE, MUST),
        "width":                SIZE,
        "height":               SIZE,
        "align":                (["top", "middle", "bottom", "left", "right", 
                                "texttop", "absmiddle", "absbottom", "baseline"], 
                                "bottom"),
        }),

    "table": (1, {
        "align":                (["left", "center", "right"], "left"),
        "valign":               (["top", "bottom", "middle"], "middle"),
        "border":               (SIZE, "0"),
        "bordercolor":          (COLOR, "#000000"),
        "bgcolor":              COLOR,
        "cellpadding":          (SIZE, "0"),
        "cellspacing":          (SIZE, "0"),
        "repeat":               (INT, "0"),  # XXX Remove this! Set to 0 
        "width":                STRING,
        "keepmaxwidth":         SIZE,
        "keepmaxheight":        SIZE,
        "keepmergespace":       (INT, 1),
        "keepmode":             (["error", "overflow", "shrink", "truncate"], "shrink"),
        }),

    "tr": (1, {
        "bgcolor":              COLOR,
        "valign":               ["top", "bottom", "middle"],
        "border":               SIZE,
        "bordercolor":          (COLOR, "#000000"),
        }),

    "td": (1, {
        "align":                ["left", "center", "right", "justify"],
        "valign":               ["top", "bottom", "middle"],
        "width":                STRING,
        "bgcolor":              COLOR,
        "border":               SIZE,
        "bordercolor":          (COLOR, "#000000"),
        "colspan":		        INT, 
        "rowspan":		        INT,
        }),

    "th": (1, {
        "align":                ["left", "center", "right", "justify"],
        "valign":               ["top", "bottom", "middle"],
        "width":                STRING,
        "bgcolor":              COLOR,
        "border":               SIZE,
        "bordercolor":          (COLOR, "#000000"),
        "colspan":		        INT, 
        "rowspan":		        INT,
        }),

    "dl": (1, {
        }),

    "dd": (1, {
        }),

    "dt": (1, {
        }),

    "ol": (1, {
        "type":                 (["1", "a", "A", "i", "I"], "1"),
        }),

    "ul": (1, {
        "type":                 (["circle", "disk", "square"], "disk"),
        }),

    "li": (1, {
        }),

    "hr": (0, {
        "color":                (COLOR, "#000000"),
        "size":                 (SIZE, "1"),
        "align":                ["left", "center", "right", "justify"],
        }),

    "div": (1, {
        "align":                ["left", "center", "right", "justify"],
        }),

    "p": (1, {
        "align":                ["left", "center", "right", "justify"],
        }),

    "br": (0, {
        }),

    "h1": (1, {
        "outline":              STRING,
        "closed":               (INT, 0),
        "align":                ["left", "center", "right", "justify"],
        }),

    "h2": (1, {
        "outline":              STRING,
        "closed":               (INT, 0),
        "align":                ["left", "center", "right", "justify"],
        }),

    "h3": (1, {
        "outline":              STRING,
        "closed":               (INT, 0),
        "align":                ["left", "center", "right", "justify"],
        }),

    "h4": (1, {
        "outline":              STRING,
        "closed":               (INT, 0),
        "align":                ["left", "center", "right", "justify"],
        }),

    "h5": (1, {
        "outline":              STRING,
        "closed":               (INT, 0),
        "align":                ["left", "center", "right", "justify"],
        }),

    "h6": (1, {
        "outline":              STRING,
        "closed":               (INT, 0),
        "align":                ["left", "center", "right", "justify"],
        }),

    "font": (1, {
        "face":                 FONT,
        "color":                COLOR,
        "size":                 STRING,
        }),

    "a": (1, {
        "href":                 STRING,
        "name":                 STRING,
        }),

    "input": (0, {        
        "name":                 STRING,
        "value":                STRING,
        "type":                 (["text", "hidden", "checkbox"], "text"),
        }),

    "textarea": (1, {        
        "name":                 STRING,    
        }),
        
    "select": (1, {        
        "name":                 STRING,
        "value":                STRING,        
        }),
               
    "option": (0, {                
        "value":                STRING,
        }),
    }

# XXX use "html" not "*" as default!
DEFAULT_CSS = """
html {
    font-family: Helvetica; 
    font-size: 10px; 
    font-weight: normal;
    color: #000000; 
    background-color: transparent;
    margin: 0; 
    padding: 0;
    line-height: 150%;
    border: 1px none;
    display: inline;
    width: auto;
    height: auto;
    white-space: normal;    
}

b, 
strong { 
    font-weight: bold; 
}

i, 
em { 
    font-style: italic; 
}

u {
    text-decoration: underline;
}

s,
strike {
    text-decoration: line-through;
}

a {
    text-decoration: underline;
    color: blue;
}

ins {
    color: green;
    text-decoration: underline;
}
del {
    color: red;
    text-decoration: line-through;
}

pre,
code,
kbd,
samp,
tt {
    font-family: "Courier New";
}

h1,
h2,
h3,
h4,
h5,
h6 {
    font-weight:bold;
    -pdf-outline: true;    
    -pdf-outline-open: false;
}

h1 {
    /*18px via YUI Fonts CSS foundation*/
    font-size:138.5%; 
    -pdf-outline-level: 0;
}

h2 {
    /*16px via YUI Fonts CSS foundation*/
    font-size:123.1%;
    -pdf-outline-level: 1;
}

h3 {
    /*14px via YUI Fonts CSS foundation*/
    font-size:108%;
    -pdf-outline-level: 2;
}

h4 {
    -pdf-outline-level: 3;
}

h5 {
    -pdf-outline-level: 4;
}

h6 {
    -pdf-outline-level: 5;
}

h1,
h2,
h3,
h4,
h5,
h6,
p,
pre,
img,
hr {
    margin:1em 0;
}

address,
blockquote,
body,
center,
dl,
dir,
div,
fieldset,
form,
h1,
h2,
h3,
h4,
h5,
h6,
hr,
isindex,
img,
menu,
noframes,
noscript,
ol,
p,
pre,
table,
th,
tr,
td,
ul,
li,
dd,
dt,
pdftoc {
    display: block;
}

tr,
th,
td {
    vertical-align: top;
    width: auto;
}

center {
    text-align: center;
}

big {
    font-size: 125%;
}

small {
    font-size: 75%;
}


ul {
    margin-left: 1.5em;
    list-style-type: disc;
}

ul ul {
    list-style-type: circle;
}

ul ul ul {
    list-style-type: square;
}

ol {
    list-style-type: decimal;
    margin-left: 1.5em;
}

pre {
    white-space: pre;
}
"""

DEFAULT_FONT = {
    "courier": "Courier",
    "courier-bold": "Courier-Bold",
    "courier-boldoblique": "Courier-BoldOblique",
    "courier-oblique": "Courier-Oblique",
    "helvetica": "Helvetica",
    "helvetica-bold": "Helvetica-Bold",
    "helvetica-boldoblique": "Helvetica-BoldOblique",
    "helvetica-oblique": "Helvetica-Oblique",
    "times": "Times-Roman",
    "times-roman": "Times-Roman",
    "times-bold": "Times-Bold",
    "times-boldoblique": "Times-BoldOblique",
    "times-oblique": "Times-Oblique",
    "symbol": "Symbol",
    "zapfdingbats": "ZapfDingbats",
    "zapf-dingbats": "ZapfDingbats",
    
    # Alias
    "arial": "Helvetica",
    "times new roman": "Times-Roman",
    "georgia": "Times-Roman",
    'serif':'Times-Roman',
    'sansserif':'Helvetica',
    'sans':'Helvetica',
    'monospaced':'Courier', 
    'monospace':'Courier', 
    'mono':'Courier', 
    'courier new':'Courier',    
    'verdana':'Helvetica',
    'geneva':'Helvetica',
    }

PML_PAGESIZES = {
        "a0": A0, 
        "a1": A1, 
        "a2": A2, 
        "a3": A3, 
        "a4": A4, 
        "a5": A5, 
        "a6": A6, 
        "b0": B0, 
        "b1": B1, 
        "b2": B2, 
        "b3": B3, 
        "b4": B4, 
        "b5": B5, 
        "b6": B6, 
        "letter": LETTER, 
        "legal": LEGAL, 
        "ledger": ELEVENSEVENTEEN,
        "elevenseventeen": ELEVENSEVENTEEN, 
        }