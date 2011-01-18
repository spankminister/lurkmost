import os
import subprocess
import re

TMPDIR = 'tmp'

# FIXME: In general, should output external commands to bytestrings
#           using subprocess.check_call

class ChanHandler(object):
    def __init__(self):
        # WIP
        self.threadId = self.getThreadId()
        raise NotImplementedError

    def check404(self):
        try:
            response = subprocess.check_call(["wget", "--server-response", self.url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return False
        except subprocess.CalledProcessError:
            print "Thread 404'd, stopping get"
            return True

    def getThreadId(self):
        # Let's consider 4chan and wakachan the base case
        # format is "res/[threadid]
        r = re.compile(self.restring)
        match = r.search(self.url)
        return int(self.url[match.start()+4:match.end()])

    def makeImageList(self):
        # Use wget and grep to get the file names, 
        self.imageLinks = []
        #FIXME change next line to use subprocess.check_call
        os.system("wget -O- \"%s\" | egrep %s -o | sort -u > %s/%d.tmp" % (self.url, self.grepstring, TMPDIR, self.threadId)) 

        # Read the file into a list, adding the base to relative links
        filelist = open('%s/%d.tmp' % (TMPDIR, self.threadId), 'r')
        for link in filelist:
            link = link.strip()
            if self.relativeLinks:
                self.imageLinks.append(self.baseHost + link)
            else:
                self.imageLinks.append(link)

    def download(self):
        # Return False if the thread has 404'd, else return True
        if self.check404():
            return False

        #TODO make thread dir a class var
        threadDir = self.siteName + "/" + str(self.threadId)
        for link in self.imageLinks:
            os.system("wget --continue --wait 2 -P %s %s" % (threadDir, link))
        return True
        

class IiChanHandler(ChanHandler):
    def __init__(self, url):
        self.url = url
        self.restring = "res/[0-9]+"
        self.relativeLinks = True
        # TODO get this from the url or something in case the
        # subdomain is different
        self.baseHost = "http://kei.iichan.net"

        self.siteName = "iichan"
        self.grepstring = "'/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"
        self.threadId = self.getThreadId()

class FourChanArchiveHandler(ChanHandler):
    # thread url is of form: http://4chanarchive.org/brchive/dspl_thread.php5?thread_id=21048406&x=Space+Ghost+Is+Back+On+The+Air2C+Due+To+A+TechnicalityTimewarp
    def __init__(self, url):
        self.url = url
        self.restring = "thread_id=[0-9]+"
        self.relativeLinks = False

        self.siteName = "4chanarchive"
        self.grepstring = "'http://4chanarchive.org/images/[a-z0-9]+/[a-z0-9]+/([0-9]*).(jpg|png|gif)'"
        self.threadId = self.getThreadId()

    def getThreadId(self):
        r = re.compile(self.restring)
        match = r.search(self.url)
        return int(self.url[match.start()+10:match.end()])
        
class FourChanHandler(ChanHandler):
    def __init__(self, url):
        # thread url is of form: http://boards.4chan.org/co/res/21649743
        self.url = url
        self.restring = "res/[0-9]+"
        self.relativeLinks = False

        self.siteName = "4chan"
        self.grepstring = "'http://images.4chan.org/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"
        self.threadId = self.getThreadId()

class WakaChanHandler(ChanHandler):
    def __init__(self, url):
        self.url = url
        self.restring = "res/[0-9]+"
        self.relativeLinks = True
        self.baseHost = "http://wakachan.org"

        self.siteName = "wakachan"
        self.grepstring = "'/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"
        self.threadId = self.getThreadId()

class TwoChanHandler(ChanHandler):
    def __init__(self, url):
        self.url = url
        self.restring = "res/[0-9]+"
        self.baseHost = "http://dat.2chan.net"
        self.relativeLinks = True

        self.siteName = "2chan"
        self.grepstring = "'/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"
        self.threadId = self.getThreadId()
