# -*- coding: ISO-8859-1 -*-
#############################################
## (C)opyright by Dirk Holtwick, 2002-2007 ##
## All rights reserved                     ##
#############################################

__reversion__ = "$Revision: 20 $"
__author__ = "$Author: holtwick $"
__date__ = "$Date: 2007-10-09 12:58:24 +0200 (Di, 09 Okt 2007) $"

from pisa_tags import pisaTag
from pisa_util import *
from pisa_reportlab import PmlTable, TableStyle, KeepInFrame

import copy
import sys

class PmlKeepInFrame(KeepInFrame):
  
    def wrap(self, availWidth, availHeight):
        self.maxWidth = availWidth
        self.maxHeight = availHeight       
        return KeepInFrame.wrap(self, availWidth, availHeight)
            
    """
    def __init__(self, maxWidth, maxHeight, content=[], mergeSpace=1, mode='shrink', name=''):
        '''mode describes the action to take when overflowing
            error       raise an error in the normal way
            continue    ignore ie just draw it and report maxWidth, maxHeight
            shrink      shrinkToFit
            truncate    fit as much as possible
        '''
        self.name = name
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.mode = mode
        assert mode in ('error','overflow','shrink','truncate'), '%s invalid mode value %s' % (self.identity(),mode)
        assert maxHeight>=0,  '%s invalid maxHeight value %s' % (self.identity(),maxHeight)
        if mergeSpace is None: mergeSpace = overlapAttachedSpace
        self.mergespace = mergeSpace
        self._content = content

    def _getAvailableWidth(self):
        return self.maxWidth - self._leftExtraIndent - self._rightExtraIndent

    def identity(self, maxLen=None):
        return "<%s at %s%s%s> size=%sx%s" % (self.__class__.__name__, hex(id(self)), self._frameName(),
                getattr(self,'name','') and (' name="%s"'% getattr(self,'name','')) or '',
                getattr(self,'maxWidth','') and (' maxWidth=%s'%fp_str(getattr(self,'maxWidth',0))) or '',
                getattr(self,'maxHeight','')and (' maxHeight=%s' % fp_str(getattr(self,'maxHeight')))or '')

    def wrap(self,availWidth,availHeight):
        from doctemplate import LayoutError
        mode = self.mode
        maxWidth = availWidth
        maxHeight = float(min(self.maxHeight or availHeight,availHeight))
        W, H = _listWrapOn(self._content,maxWidth,self.canv)
        if (mode=='error' and (W>maxWidth+_FUZZ or H>maxHeight+_FUZZ)):
            ident = 'content %sx%s too large for %s' % (W,H,self.identity(30))
            #leave to keep apart from the raise
            raise LayoutError(ident)
        elif W<=maxWidth+_FUZZ and H<=maxHeight+_FUZZ:
            self.width = W-_FUZZ      #we take what we get
            self.height = H-_FUZZ
        elif mode in ('overflow','truncate'):   #we lie
            self.width = min(maxWidth,W)-_FUZZ
            self.height = min(maxHeight,H)-_FUZZ
        else:
            def func(x):
                W, H = _listWrapOn(self._content,x*maxWidth,self.canv)
                W /= x
                H /= x
                return W, H
            W0 = W
            H0 = H
            s0 = 1
            if W>maxWidth+_FUZZ:
                #squeeze out the excess width and or Height
                s1 = W/maxWidth
                W, H = func(s1)
                if H<=maxHeight+_FUZZ:
                    self.width = W-_FUZZ
                    self.height = H-_FUZZ
                    self._scale = s1
                    return W,H
                s0 = s1
                H0 = H
                W0 = W
            s1 = H/maxHeight
            W, H = func(s1)
            self.width = W-_FUZZ
            self.height = H-_FUZZ
            self._scale = s1
            if H<min(0.95*maxHeight,maxHeight-10) or H>=maxHeight+_FUZZ:
                #the standard case W should be OK, H is short we want
                #to find the smallest s with H<=maxHeight
                H1 = H
                for f in 0, 0.01, 0.05, 0.10, 0.15:
                    #apply the quadratic model
                    s = _qsolve(maxHeight*(1-f),_hmodel(s0,s1,H0,H1))
                    W, H = func(s)
                    if H<=maxHeight+_FUZZ and W<=maxWidth+_FUZZ:
                        self.width = W-_FUZZ
                        self.height = H-_FUZZ
                        self._scale = s
                        break

        return self.width, self.height

    def drawOn(self, canv, x, y, _sW=0):
        scale = getattr(self,'_scale',1.0)
        truncate = self.mode=='truncate'
        ss = scale!=1.0 or truncate
        if ss:
            canv.saveState()
            if truncate:
                p = canv.beginPath()
                p.rect(x, y, self.width,self.height)
                canv.clipPath(p,stroke=0)
            else:
                canv.translate(x,y)
                x=y=0
                canv.scale(1.0/scale, 1.0/scale)
        _Container.drawOn(self, canv, x, y, _sW=_sW, scale=scale)
        if ss: canv.restoreState()
    """
    
def _width(value=None):
    if value is None:
        return None
    value = str(value)
    if value.endswith("%"):
        return value
    return getSize(value)

class TableData:

    def __init__(self):
        self.data = []
        self.styles = []
        self.span = []
        self.mode = ""
        self.padding = 0

    def add_cell(self, data=None):
        self.col += 1
        self.data[len(self.data) - 1].append(data)

    def add_style(self, data):
        # print self.mode, data
        self.styles.append(copy.copy(data))

    def add_empty(self, x, y):
        self.span.append((x, y))

    def get_data(self):
        data = self.data
        for x, y in self.span:
            try:
                data[y].insert(x, '')
            except:
                pass
        return data
   
    def add_cell_styles(self, c, begin, end, mode="td"):
        def getColor(a, b): return a
        self.mode = mode.upper()
        if c.frag.backColor and mode != "tr": # XXX Stimmt das so?
            self.add_style(('BACKGROUND', begin, end, c.frag.backColor))
            # print 'BACKGROUND', begin, end, c.frag.backColor
        if 0:
            log.debug("%r", (
                begin,
                end,
                c.frag.borderTopWidth,
                c.frag.borderTopStyle,
                c.frag.borderTopColor,
                c.frag.borderBottomWidth,
                c.frag.borderBottomStyle,
                c.frag.borderBottomColor,
                c.frag.borderLeftWidth,
                c.frag.borderLeftStyle,
                c.frag.borderLeftColor,
                c.frag.borderRightWidth,
                c.frag.borderRightStyle,
                c.frag.borderRightColor,
                ))
        if getBorderStyle(c.frag.borderTopStyle) and c.frag.borderTopWidth:
            self.add_style(('LINEABOVE', begin, (end[0], begin[1]),
                c.frag.borderTopWidth,
                getColor(c.frag.borderTopColor, c.frag.textColor),
                "squared"))
        if getBorderStyle(c.frag.borderLeftStyle) and c.frag.borderLeftWidth:
            self.add_style(('LINEBEFORE', begin, (begin[0], end[1]),
                c.frag.borderLeftWidth,
                getColor(c.frag.borderLeftColor, c.frag.textColor),
                "squared"))
        if getBorderStyle(c.frag.borderRightStyle) and c.frag.borderRightWidth:
            self.add_style(('LINEAFTER', (end[0], begin[1]), end,
                c.frag.borderRightWidth,
                getColor(c.frag.borderRightColor, c.frag.textColor),
                "squared"))
        if getBorderStyle(c.frag.borderBottomStyle) and c.frag.borderBottomWidth:
            self.add_style(('LINEBELOW', (begin[0], end[1]), end,
                c.frag.borderBottomWidth,
                getColor(c.frag.borderBottomColor, c.frag.textColor),
                "squared"))
        self.add_style(('LEFTPADDING', begin, end, c.frag.paddingLeft or self.padding))
        self.add_style(('RIGHTPADDING', begin, end, c.frag.paddingRight or self.padding))
        self.add_style(('TOPPADDING', begin, end, c.frag.paddingTop or self.padding))
        self.add_style(('BOTTOMPADDING', begin, end, c.frag.paddingBottom or self.padding))

class pisaTagTABLE(pisaTag):
    
    def start(self, c):
        c.addPara()
    
        attrs = self.attr
        
        # Swap table data
        c.tableData, self.tableData = TableData(), c.tableData
        tdata = c.tableData

        # border
        #tdata.border = attrs.border
        #tdata.bordercolor = attrs.bordercolor

        begin = (0, 0)
        end = (- 1, - 1)
            
        if attrs.border:
            tdata.add_style(("GRID", begin, end, attrs.border, attrs.bordercolor))
        
        tdata.padding = attrs.cellpadding
        
        #if 0: #attrs.cellpadding:
        #    tdata.add_style(('LEFTPADDING', begin, end, attrs.cellpadding))
        #    tdata.add_style(('RIGHTPADDING', begin, end, attrs.cellpadding))
        #    tdata.add_style(('TOPPADDING', begin, end, attrs.cellpadding))
        #    tdata.add_style(('BOTTOMPADDING', begin, end, attrs.cellpadding))
            
        # alignment
        #~ tdata.add_style(('VALIGN', (0,0), (-1,-1), attrs.valign.upper()))

        # Set Border and padding styles
        
        tdata.add_cell_styles(c, (0, 0), (- 1, - 1), "table")

        # bgcolor
        #if attrs.bgcolor is not None:
        #    tdata.add_style(('BACKGROUND', (0, 0), (-1, -1), attrs.bgcolor))

        tdata.align = attrs.align.upper()
        tdata.col = 0
        tdata.row = 0        
        tdata.colw = []
        tdata.rowh = []
        tdata.repeat = attrs.repeat
        tdata.width = _width(attrs.width)

        # self.tabdata.append(tdata)

    def end(self, c):
        tdata = c.tableData
        data = tdata.get_data()        
        try:
            if tdata.data:
                # log.debug("Table sryles %r", tdata.styles)
                t = PmlTable(
                    data,
                    colWidths=tdata.colw,
                    rowHeights=tdata.rowh,
                    # totalWidth = tdata.width,
                    splitByRow=1,
                    # repeatCols = 1,
                    repeatRows=tdata.repeat,
                    hAlign=tdata.align,
                    vAlign='TOP',
                    style=TableStyle(tdata.styles))
                t.totalWidth = _width(tdata.width)
                t.spaceBefore = c.frag.spaceBefore
                t.spaceAfter = c.frag.spaceAfter
                # t.hAlign = tdata.align
                c.addStory(t)
            else:
                log.warn(c.warning("<table> is empty"))
        except:            
            log.warn(c.warning("<table>"), exc_info=1)

        # Cleanup and re-swap table data
        c.clearFrag()
        c.tableData, self.tableData = self.tableData, None
    
class pisaTagTR(pisaTag):
    
    def start(self, c):            
        tdata = c.tableData
        row = tdata.row
        begin = (0, row)
        end = (- 1, row)
        
        tdata.add_cell_styles(c, begin, end, "tr")       
        c.frag.vAlign = self.attr.valign or c.frag.vAlign
          
        tdata.col = 0
        tdata.data.append([])

    def end(self, c):
        c.tableData.row += 1        

class pisaTagTD(pisaTag):
    
    def start(self, c):

        if self.attr.align is not None:
            #print self.attr.align, getAlign(self.attr.align)
            c.frag.alignment = getAlign(self.attr.align)
            
        c.clearFrag()
        self.story = c.swapStory()
        # print "#", len(c.story)
        
        attrs = self.attr
        
        tdata = c.tableData

        cspan = attrs.colspan
        rspan = attrs.rowspan

        row = tdata.row
        col = tdata.col
        while 1:
            for x, y in tdata.span:
                if x == col and y == row:
                    col += 1
                    tdata.col += 1
            break
        #cs = 0
        #rs = 0

        begin = (col, row)
        end = (col, row)
        if cspan:
            end = (end[0] + cspan - 1, end[1])
        if rspan:
            end = (end[0], end[1] + rspan - 1)
        if begin != end:
            #~ print begin, end
            tdata.add_style(('SPAN', begin, end))
            for x in range(begin[0], end[0] + 1):
                for y in range(begin[1], end[1] + 1):
                    if x != begin[0] or y != begin[1]:
                        tdata.add_empty(x, y)

        # Set Border and padding styles
        tdata.add_cell_styles(c, begin, end, "td")

        # Calculate widths
        # Add empty placeholders for new columns
        if (col + 1) > len(tdata.colw):
            tdata.colw = tdata.colw + ((col + 1 - len(tdata.colw)) * [_width()])
        # Get value of with, if no spanning
        if not cspan:
            # print c.frag.width
            width = c.frag.width or self.attr.width #self._getStyle(None, attrs, "width", "width", mode)
            # If is value, the set it in the right place in the arry
            # print width, _width(width)
            if width is not None:
                tdata.colw[col] = _width(width)

        # Calculate heights
        if row + 1 > len(tdata.rowh):
            tdata.rowh = tdata.rowh + ((row + 1 - len(tdata.rowh)) * [_width()])
        if not rspan:
            height = None #self._getStyle(None, attrs, "height", "height", mode)
            if height is not None:
                tdata.rowh[row] = _width(height)
                tdata.add_style(('FONTSIZE', begin, end, 1.0))
                tdata.add_style(('LEADING', begin, end, 1.0))

        # Vertical align      
        valign = self.attr.valign or c.frag.vAlign
        if valign is not None:
            tdata.add_style(('VALIGN', begin, end, valign.upper()))

        # Reset border, otherwise the paragraph block will have borders too
        frag = c.frag
        frag.borderLeftWidth = 0
        frag.borderLeftColor = None
        frag.borderLeftStyle = None
        frag.borderRightWidth = 0
        frag.borderRightColor = None
        frag.borderRightStyle = None
        frag.borderTopWidth = 0
        frag.borderTopColor = None
        frag.borderTopStyle = None
        frag.borderBottomWidth = 0
        frag.borderBottomColor = None
        frag.borderBottomStyle = None

    def end(self, c):
        tdata = c.tableData
        
        c.addPara()
        cell = c.story
        
        # Handle empty cells, they otherwise collapse
        if not cell:
            cell = ' '        
            
        # Keep in frame if needed since Reportlab does no split inside of cells
        elif c.frag.keepInFrameMode is not None:
            # tdata.keepinframe["content"] = cell
            cell = PmlKeepInFrame(
                maxWidth=0,
                maxHeight=0,
                mode=c.frag.keepInFrameMode,
                content=cell)

        c.swapStory(self.story)
              
        tdata.add_cell(cell)
        
class pisaTagTH(pisaTagTD):
    pass

'''
    end_th = end_td

    def start_keeptogether(self, attrs):
        self.story.append([])
        self.next_para()

    def end_keeptogether(self):
        if not self.story[-1]:
            self.add_noop()
        self.next_para()
        s = self.story.pop()
        self.add_story(KeepTogether(s))

    def start_keepinframe(self, attrs):
        self.story.append([])
        self.keepinframe = {
            "maxWidth": attrs["maxwidth"],
            "maxHeight": attrs["maxheight"],
            "mode": attrs["mode"],
            "name": attrs["name"],
            "mergeSpace": attrs["mergespace"]
            }
        # print self.keepinframe
        self.next_para()

    def end_keepinframe(self):
        if not self.story[-1]:
            self.add_noop()
        self.next_para()
        self.keepinframe["content"] = self.story.pop()
        self.add_story(KeepInFrame(**self.keepinframe))
'''