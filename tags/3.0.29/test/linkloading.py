# -*- coding: ISO-8859-1 -*-
#############################################
## (C)opyright by Dirk Holtwick            ##
## All rights reserved                     ##
#############################################

__version__ = "$Revision: 194 $"
__author__  = "$Author: holtwick $"
__date__    = "$Date: 2008-04-18 18:59:53 +0200 (Fr, 18 Apr 2008) $"

import ho.pisa as pisa

import logging
log = logging.getLogger(__file__)

def dummyLoader(name):
    return '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00F\x00\x00\x00\x89\x04\x03\x00\x00\x00c\xbeS\xd6\x00\x00\x000PLTE\x00\x00\x00\n\x06\x04\x18\x14\x0f-&\x1eLB6w`E\x8f\x80q\xb2\x9c\x82\xbe\xa1{\xc7\xb0\x96\xd1\xbd\xa9\xd9\xd0\xc6\xef\xeb\xe6\xf8\xf3\xef\xff\xfb\xf7\xff\xff\xffZ\x83\x0b|\x00\x00\x0c\xedIDATx^u\x97]l\x1bWv\xc7g\xe2`\x81\xbe\xcd%Gr\xd3\xa7P\x12e\xb7\x01\x8a\xd0")E\x01\x02\x8f\xf8!\x8bI\x17\x10\xc5!))5`\xf1C\xb4\xb25`S\xb2l\xb95\x90H\xa4.\xb9/u$K3\xe3\xa2\x80W\x12\xc59L\xf6a\xb3\x8dcN\xd6@\xb7\x1f\x01\x8a\x85\x16\x9b-\xfa\x81M\xb8@\x83l\xd1\xd8\xbc|)\xd0\x97\x82\xea\xb93\x92\xec"\xce\x11 \t3?\xfe\xcf\xff\x9e{\xce\x01(\x1c>7\x18\xfb\xc2\xfaE\xffk_\xb6\x18\xeb\x1e>\x8f\xe92d\xfe%T\xa8\x98\xfa\x07\x1f $<\x0f\xe1\x91\xabT\xc1\xacT\xf2\xbfd\xec\xbb\x98\xdfM\xeb\x86aYP\xfa\xd3\xd6\xf3\x98C[\xa6\xaaU\xa1a5\xe9\x1b\xad\xef\xd0i}\x91\xccy+\xc8X\xf5E\xf6]:\xff0\xd8\x97\xce7\xb9P\xf1\xd1\xb7\x98\xaec\xe7/\xd3\xa1\xeb\x81{\x96e5\xd7.\xb6\x85\xe7\x99aO\x94\xf1R(\xfeC\xce\xd4F\xbf\xc50\x1b\xfa\xefS\xa9\xb2\x12p\x98({\x8eN\x9b\xb1\xbf\xf5O\xa5\xd7\x0b\xb4\xc9\x0f\x96\xec<G\xa7\xc5\x1e\xbf\xfa\xe2b\x90\x16\xb2\x00\x96E\x93O\x9e\xe7\xe77\x8b\xd2@ \xa3\xa7\x96\xe6\r\xab\xb9\x97\xfc\xf6\xb90WV\x0e\x8d(\xa1\xa5dd*\x06PL\xa2\xe7g\xdfw\xba\xe8\xe6o\x06\xc6\xd5\x80\xc7\xe5s\xbb|\xbd\x91\xd2\xb9 \x13\x9e1\xc2\x13\xb5\xfeN\rn\xa5\xd5a\xc5+\xe7\xb7\xf5\xa2\xcbC\xde>a\x9c\xd2\xb5\xad\x07\xdbS\x0b\xb0\xa5z\xeb\x94\xd2y\x80kD\xee<e\x10h\x7fs]\xf4g\xa7\x01\xb6\x12\x91z\xa9P\x8a\\\xcfg\xfdQ\xf6\x0c\x83\xb1CD?\x05\x80\xf2\xa4;z)\xb8\x11\xf1\x11\xf7\xe5\x8b\x9d\xff\xcf\\\x92H\x846\x80f\x91Ys/\x11\xe2r\x85\xfe\x98u\x9e\xf5\xf3_\x1eB\xd2U\x00\x9a\xf3\xc9\xc92\xb9\xbc\xbc\xec\x93N?:\xce\xd59\xect\xdb\xec_\xbdC\xa4\x1f\x99\xb9\x81\x97\xddj\xb9g\x8c\xf4\xaf\xe8\x8f\xba\xc8\x1cwy\xbb\xd3\xb8\xab.\xfb\x0bU\xd03S\xa2\xac\x96\x03k\xe1\x02\xe4\x19\xbe\x12N\xcc|3<U\xd8O\x02\xd4iQ\x12\\j\x81R\x80\xbd\x14\x16\xed\x88\xc1\xfavw&\x02isj\xa2\xa9\xd1\x12\x91\xc4\xfe$\xa5\xe1\xbc\xf2f\xbbs\xcc \xc2\xb2\xc6\xcd\xec\xe8\xfe\xa2\x05\xb4F$A\x0c\x94\n\xee\x9b\xc5\xec_\xb3\xa7\x0c\xfb\xf7q\xad\xb2\xb6b5?h\xea\xe6$\x11\t\xe9\xebs\r\xbdv\xf5\xf6\t\xd3a\xec#5\xb8\x9c\x08\xdf\xb4\xc0J\xc1\x9a$\x11\x7f8\x1c\x01\xb8\xf4\x17\xec\xb0s\xe29\x93\x18\x08\xa5\xcc\xa4eA\xaep\xd7#\xca\xa0\xeb\xd7o\xd5\x8a\xb7\x19;a:.\x1f\x11\xdd7\x1b8R\xcb\x83\xf5\xac<\xbf\x1e.,\xce~<\xff\xe3N\x9b\x1d3m\x0f\xea\x8b\x85{\xd6\xa7\xd6\xc3\xf8e}\xd9\xdc C\xd1\xd9f\xfe\x9d\x16;f\xba\x7f/\x12A\x10\xce\xe2\x88[\xffT\x9a\x99\xc8\x0co\xf5\xf5\x05g\xad\xda\x0fX\xeb\xa4\xceqQ\x10$\xb1\xb7\xd2@\xa86x\x7f8>h._\x9dh4\x8d\xa7:\x8f#X\x13At\xdb3nF\xee\xc8\x19wV^\xf4\x1b\xd6\xdc\xed\x13\xe6w\x01I\x90\x90\xa1F\x05\x99\xdc}B\x88(\x87}\xb7\xac\xda\x99\x13\xe6\xa7\xa1\xf3\x02fs\xa5)\xbd\xd70\r\xceH"\x91\xc2\x15\xc8\x1e\x9f\xbd\xbd\x17\xf7\x8b\x04m\x07\xd2\xb4\x02\xc8 !\xcf\xe1\x83\x0b\xc6\x9d+\\\x87u;\xedl\xdc{^\x12\x05\x89$\x0b\xd40\xef\x12\tu\xd2\x99!\xec\xc4\xab\x17\x8f\x98\xc7/\xc6\x07\xc6$;\xc1YZ\xd1+\n\x11E\x12\xa0\xe0\x1b\x18G\xd3\x0e\xf3\xb57\xeeN\xbc,\x89\xa2@z\xd0\x12]\xc34C\x11d\xbct\x809\x0c\xfbU N"\x1eA\x92\xf0l\x03\xd8]\xeb\nq/\xc9\xb4\xe6\x91\x13\xf2\x97\xc8t\x1dF\xea#\xa2\xc0\xebH\x06)\x98\x8b\xc4\xbd\xd73\x12\x17e\xe5\x956g\xb0C~\x15P\x89(\t<\x08\xe9\xbda\xc0]\xcf\x1f\xed\x91\xbcBd\xe5\rv\xc4\xfc:\xac\xe2Qlf\xc8G\x82\x95\xc6\'\xf1\x18(><\xa6\xfb\xc0\xf6\x83\xcc\xe7\t\xd5G\x1c&\x8d\xc3E\x1b\x0fK\x00\x8a"\xc8\xd9\xde\x93\xfb\xfa\\U\xa7\x08\xcf\x85\x96\xd3\xf9\xb1\xf4\x0f\x9b\x9c\x11\xa4q_\xf8\xe0)3\xa5\x9e\x97\x1c;^\xbaU\xa8Z[1x\x9f\xbcX$3_v9\xd3\xedt?W\xe3^\x14r\xa04T\xc0\xfad\x14\xc6r\x83\xf7\xa5\xc4\x91\x1f\xc6\x90!r\x9fs0\xb1\xa76\xdd\xb0\x1e\xc66\xcf\\\x9ay\xf5\x85\xc4\xc1aW\xb0\x97\xd355A\x88,8AjA\x1d\x1b-S\x98Ly\xe4\xe4m\xe7\xec-\xe6WU\x82%\x94\x1cF\xed\xa1Uk/\xa2\xb9\xb3\xe4T\xee\r\xf6[dZ-\x16@F\xc2{w\x92\x05C#\xd4\x1a\x1f\xae\xcbe\x8f\xff\\\xaf\xe3\xa7\xfd\xf5\xd9\xb2:\x89wu\x14\xb2\xe2\xbeqO_\xa9\x0f\xaf\xfb\xfa\x06\xe7\xae\xb4m?\xff\xdc[\x8a\xa8\xca1$\x8a!\xf2Zc\x13\xea\x17\xd6\\I(\xcd\xb4\x84\xeea\x9b}\xe4\xce\x8f\x85\x13\xce\x8d\x89\xc8HR\x10\xb2P\xa7\x19w\x0c\xf6\x93\xbf\xe4L\xeb\x12\x89\x95\\\x11\xc5\xbe1" *\xca\xc6\x80Ik\xbe\xf0\x02\xd4s\x8f\xb8\x9fo|\xbd\x83\xda\x80+\xc7\xdbPD\x10\x8f\xf8\xc2B?\xadlD\x8b\x00\x943]\xf6?\xa9\xfe\x1e\xdc\xd6\x83\x08\t\xbc\x00\xc3\x8aH\xd2\xfd\x85\x8a_\x1b?a~\xb4\xb0\x99\xf1-g\xfc\x86\x11\x1a\x1a:\xd7G\x00\xce\x8b\xbd\xef\x176a\xed\xb5f\xb3\x9e{\x9b\xe7\xda\xbde\xc1^h\x1cj\x97s*\xc69\x80]B2\x05]\xcb.\x00\xd4\xcb\xafs\x9d\xfb\xef\xe0\x90\xefG\r\x8d\xaa\xe10\x9aA\x8eH\xee\x02-\xab^\x00\xd3f\xba\xbb\xc6\xa7V\xb3\xa9Uu]\xcf\x86\xb1\xda\xf6\x8c\xbe\x90,\xe4\x16]Q\xd08s\xd8\xde\xc5=\xd0\x040\xa0\x01e\x1f\x8e\xab\xcd\x90Hr\xdd\xf4yS\xb0\xc5\x99\xc71\x04@\xdf\x1c6\x00\xeeb\x89$\xde\xb5\xc4C\xfa\x01v\x86\xd2\xb0\x8f\x9e\xbb\xffV\x05\x93\x96\t\x99\x9b\x013DPG$R\xdf\xa9bx\x85\x7f\x12\xac\x07\x9c\xf9\xa4\n:\x8d\xe3h\xcfC.\xcb\xcbH\xdc\x03j\x90\xa2]\xdd\xc0\x9de\xfe\x00\x99T\x15\xa0\xe6!\x0159\x9f\xcf\xc7\t"I\x7f\xb9@\xab\x1a\xa5Z\xf5SK{\x13\x99\xf1*\xd4\xe7\xc8 \x8e\xf0\xe5\x89p\xde#{\xe3\xe9<\xb5\xa3R\xbfgY\x9a\x1f=GQg{\xfe\x06\xc5X\xd0\xebD.\xac\xf3\xff\xcb\xaa\x9a\xac\\\xc0\x9a\x94\\\x8e\x0e\x0f\xcd\xf9\xa4G.P\x8cuU\x8dxw\x0b\r0Koq\x86\x1aO!\x9a\x90\xd3\x1c\xc9*\x84\x8c\x16/7\xabu\xfa\xe7\xc8Di\xc5fL\x8a&\xe9v8\x89\x7fscD\x92\x17&W\x1e\xde\xd3J\xaf\xd8\x0c\xad\xd8\x14\xbe\x03C_T\xf3\xf9\\\xe2eB\xdc\xb1\x84F\xf5\xf0\x1a?{\x84[D\xa4\x01u\x8a\xbf\xf6T\x1e\xb83\xce\x04\xbd\xa6\xaa\xcd\xaf}\x88\xe7:?L\xb5\xfcM\'\x1b`(X*\xf5UQL-\xf5>\x18\xce\x8c$\x99\xc0\x98\x12\xa4tJ\xbd\xac\xeb<\x1bX\xcd\x1d{w\xf2\xae\x1d\xfeI\x94,q\xa6\xa3\x04\n\xebJ\x00\x97.\xcc\xeb\xb4\n\xf0>2|d%\x12\xfbI\xbe\'\x94\xecp\x9d@j]q\x0f\x8d\xd3\x9a?\xa6\x1b\x00\xef\x11I\xe0\xbb\x91\xb8\xa6wj\xd3\xc1 \xcf\xf5sY\xcdM\x11\x12(\x94\x88\\\xb1>K\xbf\xe7\x91\x88\xc8\xb5\xdc\xc9\xd0\xb5\xec\x99\xb78\xf3\xebS\xaa\x8a\x03\x88\x8c\x87\\\xf8\xf4\xfe\xcc5\xb4\x83\x86\x029\xf7\xd4\xe9\x9b\xa1\xa5/\xb9\x9f\xff\x15#jbh(\x92\xc6\x06\t6\xe6.\xfb\xb1\xc4\xfdb\x8fV\xf2\x89\xa2\x1c\xb9\xd2\xe6\xcc\x93\xc9\x80\x8a\x81\xf5\xc5d\xd5D\xed\x0f\xefr\xdd\x0b\xb4<\x89\xae\xc8\x15\xc6\x84\x0e\xeb~\x16Bh\x8a\xa8\xe5\xb0+Y\xd9\xdc\x9b\xb5,S!7hi\nG\x92\x1cp\xe6\xf0\xb7\x1fo\xf7\xf5\xf5\xbdL\x06K\x02\xb9P\x9d\xd8\xbbeY;\xa4\x07\xef,!\x89\xd2\xe9N\xf7\x10\x99v\x13\xee\xa0K\xd2["nZ\x81M\xec\xab;\x9e42\x93\x82$\xbe\xd29\xe4\xcc\x93\x18lp\xd5`\x89\x04\x0bU\x98Z\xb1\x9a\xfex\x9a\x96\xf9\xfa#\xb79\xc3\xba\xc8\x94\xf9|\xde(\x91\xe84@\xb2a}\x9c\x0c\xdb\xa9\x04\xe1\xd4#\x9ba\xc8`k\x89\xb2^"\x91\n\xec\xa7,kiKFF\xc1\x91\xc5m\x88\xcc!{2\x08\xb4\xe4\x11\'\x00sU\xeb\xc5\xd9fx\xa6&\xd3r\x02\'Q|\xb3c3\x87\xed\xbbP_#d\xc6\x98\x93\xd3\xd5\xd5\xc0\xec\xc3\x01(\xcbeu\n\x19r\x91ul\xa6\xb3\x07u\xac\xde\xeeK\x97\x08\xf6Vpv\'\x06\xef\x8e\xe4T\x85\x88\x92\xcc\x1c\xa6\xcb\x90YC\xe6\xb4B\xc2!wa=\x07\xf5w\xc7U,\x0e\x91\xfe\xa4\xd5:a\xcc\xb2O\xde\xed%\x18=t{\x06\xb4w\x83\t\x9f\x84%\xfbY\xf7(\x17\xdbY\x00\xaa\xc8\xbbI>\xea\x11\xdee\x9a\x12T\xb0b\xe2\xf7\x0eP\xc7\xf1|\x9f3$Q\xe4\xdb9J\rd\xce\xe5}\x9c\xf9\xb36;\xd6\xb9?\x83\x8c\x18\xbe\x86\x0c\x19__\x01s\xcd\xbd\xf8\x02\xf6*\x16\x87\xb5\x8f\xfc\xd8:b\xe2\x9a$H\xaedy\x01\xccLOv@\xb2\xdb\x82u\x1d\xa6\xbd\xb3b3s(\xe3N\xa1\x9fm_$\x11\x97D^c\xac\xa0\xe3g\x0f\x00\xeb<4\x87\x1f\x95SK\xbcX\xc3XA\xe9-4s\xc4t\x9f\xf8\x01\xd6\xf0H\xd8\xc7DNfM:\xd7sF\x9d\x12\xe5\x1f?\xcb\x8c\xa2K\x91\xb8\xe6DI\x94\xd3\xa3Z\x9ex\x83\x81\xb1\x84\xf7g\xfcP\xc7L\x8c\xdf\xa9\xf0\xa2\xffUQ\x08\xa4\xce\xe6|$\x91\x95U5\xf8\x08\x99\xae\xc3`\x8f\x99\x94*\x828\x91\x11p\x80\x06}\xe2)\xf5\xd2@^M\x7f\x88\x9e\x9f\xea\xd4)\x9d#\xe2BV\x10\x02\xd9~\\\x18\xd7\xc7\x92TM\xbf\xdd:a\x0e\xbf\x18EfU +\x8b\xc8d\xb0\xbe\xc1\xa4/J\xf37^G\xe4X\xe7q\xcc\x04Z&\xc2K\x0eC\\Y\x1a\xb8`,\x9a\xb7Z\xad\xa7\xb9Fu\x13u\xa4\x97\xb26#}\xcfK#\xd4\xd85W\xdb\xec\x19\xc6\x00\r\xeb\xfaR\xc9a\xc6F\xea\xab\x9aQ\x87U\xf6\x8cN\x0c\x1a\xday"\xfe\x9e\xc3\x90k#\xf52gJWX\x17\xef\xeb\x98\x01\x9a\xc7\xfa\x95\x88\xcd\xcc\x05\xa3U\xce\xd4\xdf\xc0+\xed:3\xf8x\x14\x99u\t\xbd\x12\x11\x19W1\xd0c\xd8\x8c\xcaX\x8b9\xf3\xf5\x1f1\xa8\xd3UIt\xe1p\xb8\xb3~Z\xf1\x91\r\xcd\xa85\xcc\xdc\x01k\x1f33\x00\xda\xaa\xe4\x0e/\x12\x89\xa4\xb1V\x8b\xbe\xa2\x06\xc5\x15(\xf1\x9b?\xb4\x99\xaf\x00\x80\xc6\xdd)\xc8\x12B\xfc\xcd\n\xad\x14s\xbay\x15\'|\x98\xb1\x13\x1d\x03h$U\x1b?\'\x86C\xa4\x01\x94\xee\x8e\xe8p\x15\x1b8\x8c\xd7\xeax\xfe\xeaF\xb5^\xd1k\xe7z\xb13\xae\xfb\x1aVS\xd39\x13\x03\x9ayttv\x16\xa2\x06\x98EQ\xec\x15"xo\xb8\xa1\x00Ftc\xaf\x17\x05\xdf\xec:\xf3\xce\xa2\x94\xc2&\x1f?\x92\xa6\xd5\xcd3M\x1d`\xa62\xbf\x13Df\x03\r\xd9~\xc2i\n\x97H8\xac\x88i\xdd0\x07,]\xdfZ\xd9^\xd9\xcf\x1b\x94\x96n\x1f1\xf7\xbdUXR)}\xcf\xfe\xa27`\x81V6\xf6rZn\x85\xd2\xf2\xf7\x8f\xcf%\xc3\x05\n\xf8@\xec\x1f1`\xee\x9df}j\xc5\xdc\x18Voit\xf5\xfb-\xc7\xf3\xcf\'\x8a\x7f\x00\x1a\xa5\xeb\xc4C&\xe0\xfdY\x0b&\x0bK\x99A\xafQ\xa7k\x07-\x9e\xab\xc3\xc6\xb6\x94\xd3\x00uZ\x96T%X\xd9\x8b!\x93t\'\x06\xaf\x83I\xd7o\xb7\x9c\\\x91\xc5p\xbfa\xeat]I\xff\xc8O\xf7\x83M\xc8\x10w\xc0\xbb\xb4b\xd2\xf2\xa8\xc3\xfc\xe7|\x94\xc6\xa7ML\x86_m\xb3\x14\x96\x8cz9G\xc8\xd9\xaca\x96\xe6C\x1fr\xa6\xf5@+\x18\xa5A\xd3\x04\x9a\xed\xd9\xc8j\xb0\x1f\xa6\xd4X"\xeei0\xd6\n\xea\x01g\xday\x8dB=~\x06\x1d\x95zV\xb7\xab`\xea\x1aB\xba\xc9\x1d\x06\xdf\xb6\xeb\xf3\x9b\n4\xf9N\xd8\xc6c(Y\xb3\x02{\xf3\x0f\n\x15@\xc3\x18\xfeN\xd7f(>\xc0\x9e\xbf3\x0e\x1a\xda\xd2\xa1\xe6\xc9O\xa0\xa8\x81H\xeeb\xdb\xd6\xf9G.\x0c\xb0zU\x9e\x81\xcd\xdf7\x00\x96<\xde( \xab\xd1l\xe0\xc0\xe9\xc3\x8f\x90G\xa9\xf8\xc6\xbc\x1fv\xe5J\xb5\xba\xd9#\'\x81K\xaf\xc5>hu\xed>\xfc)\xe5a\x8cm\xc2F\xcc\x1cZ\xde\xdc\x9f\x0ef\xd1\xf8:-\xfd\xd5\x01;\xea\xc3S\xd4\x8e\xdd\xe5\x19\x80\x86\x8fd\xca\x13\xd1\x1e\xa3\x9e\x0fEX\x1b\x7f\x1c\x1dU-\xd8\xd9F5t\x95 \xa1\xa5\x89\xa8:\xddTg\xf9N\xc5\xc9\xb1\x99\xc7J\xc4\x16\x9a\xd6\xd0\x95\x99 J4\xb5\x7f\xab\x85D\x8b\xffr\xf6<{\xb8\x1d\x0e\xf9\xa9\x13\xb0GnZ\xd6/Z\xfc%\xb3\x99\xae\xcd0f\xe1c\x1e\x9f\r\r\x05\xad\x16{&\x10\xc0\xf8?Z\n\xf1+\xfb\x81\xd5F\x00\x00\x00\x00IEND\xaeB`\x82'

class myLinkLoader:

    """
    This object is just a wrapper to track additional informations
    and handle temporary files after they are not needed any more.
    """

    def __init__(self, **kw):
        """
        The self.kw could be used in getFileName if you like
        """
        self.kw = kw
        self.tmpFileList = []

    def __del__(self):
        for path in self.tmpFileList:
            os.remove(path)
        self.tmpFileList = []

    def getFileName(self, path, relative=None):
        import os
        import tempfile

        log.info("myLinkLoader.getFileName: %r %r %r", path, relative, self.kw)
        try:
            if "." in path:
                new_suffix = "." + path.split(".")[-1].lower()
                if new_suffix in (".css", ".gif", ".jpg", ".png"):
                    suffix = new_suffix
            tmpPath = tempfile.mktemp(prefix="pisa-", suffix = suffix)
            tmpFile = file(tmpPath, "wb")
            try:
                # Here you may add your own stuff
                tmpFile.write(dummyLoader(path))
            finally:
                tmpFile.close()
            self.tmpFileList.append(tmpPath)
            return tmpPath
        except Exception, e:
            log.exception("myLinkLoader.getFileName")
        return None

def helloWorld():
    filename = __file__ + ".pdf"

    lc = myLinkLoader(database="some_name", port=666).getFileName

    pdf = pisa.CreatePDF(
        u"""
            <p>
            Hello <strong>World</strong>
            <p>
            <img src="apath/some.png">
        """,
        file(filename, "wb"),
        link_callback = lc,
        )
    if not pdf.err:
        pisa.startViewer(filename)

if __name__=="__main__":
    pisa.showLogging()
    helloWorld()

    # print repr(open("img/denker.png", "rb").read())
