import sys
import glob
import subprocess
import tempfile
import os
import os.path

__version__ = "0.1"

class VisualObject:

    CONVERT = r"C:\Programme\ImageMagick-6.3.8-Q16\convert.exe"
    DIFF = r"C:\Programme\TortoiseSVN\bin\tortoiseidiff.exe"

    def __init__(self):
        self.files = []
        self.files4del = []
        self.folder4del = None

    def __del__(self):
        for file in self.files4del:
            os.remove(file)
        self.files4del = []
        if self.folder4del:
            os.rmdir(self.folder4del)
        self.folder4del = None

    def execute(self, *a):
        # print "EXECUTE", " ".join(a)
        r = subprocess.Popen(a, stdout=subprocess.PIPE).communicate()[0]
        # print r
        return r

    def getFiles(self, folder, pattern="*.*"):
        pattern = os.path.join(folder, pattern)
        self.files = [os.path.abspath(x) for x in glob.glob(pattern)]
        self.files.sort()
        # print "FILES", self.files
        return self.files

    def loadFile(self, file, folder=None, delete=True):
        if folder is None:
            folder = self.folder4del = tempfile.mkdtemp(prefix="visualdiff-tmp-")
            delete = True
        # print "FOLDER", folder, "DELETE", delete
        source = os.path.abspath(file)
        destination = os.path.join(folder, os.path.basename(file) + ".png")
        self.execute(self.CONVERT, source, destination)
        self.getFiles(folder, os.path.basename(file)  + "*.png")
        if delete:
            self.files4del = self.files
        return folder

    def showDiff(self, left, right):
        return self.execute(self.DIFF, "/left:" + left, "/right:" + right, "/fit", "/overlay")

    def compare(self, other, chunk=16*1024, show=True):
        if not self.files:
            return False
        if len(self.files) <> len(other.files):
            return False
        for i in range(len(self.files)):
            left = self.files[i]
            right = other.files[i]
            a = open(left, "rb")
            b = open(right, "rb")
            if a.read() <> b.read():
                if show:
                    self.showDiff(left, right)
                return False
        return True

'''
def getoptions():
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"
    description = """
    Visual Differences
    """.strip()
    version = __version__
    parser = OptionParser(
        usage,
        description=description,
        version=version,
        )
    #parser.add_option(
    #    "-c", "--css",
    #    help="Path to default CSS file",
    #    dest="css",
    #    )
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.set_defaults(
        # css=None,
        )
    (options, args) = parser.parse_args()

    #if not (0 < len(args) <= 2):
    #    parser.error("incorrect number of arguments")

    return options, args

def main_command():

    options, args = getoptions()

    print args

    a = VisualObject()
    b = VisualObject()

    a.loadFile("expected/test-loremipsum.pdf")
    b.files = a.files

    print a.compare(b)
'''

import unittest
import sx.pisa3.pisa as pisa
import shutil

here = os.path.abspath(os.path.join(__file__, os.pardir))

pisa.showLogging()

class TestCase(unittest.TestCase):

    def testSamples(self):

        folder = os.path.join(here, "tmp")
        left = os.path.join(folder, "left")
        right = os.path.join(folder, "right")

        # Cleanup old tests and create new structure
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(left)
        os.makedirs(right)

        for name in glob.glob(os.path.join(here, "samples", "*.html")):
            print name

            bname = os.path.basename(name)
            fname = os.path.join(right, bname[:-5] + ".pdf")

            pdf = pisa.pisaDocument(
                open(name, "rb"),
                open(fname, "wb"))

            if pdf.err:
                print "*** %d ERRORS OCCURED" % pdf.err

            assert not pdf.err == True

            r = VisualObject()
            r.loadFile(fname, right, delete=False)

            l = VisualObject()
            l.loadFile(name[:-5] + ".pdf", left, delete=False)

            assert l.compare(r) == True

def buildTestSuite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

def main():
    buildTestSuite()
    unittest.main()

if __name__ == "__main__":
    main()
