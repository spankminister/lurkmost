#!/usr/bin/python
import os
import sys
import getopt

from handlers import *

# Globals
DEBUG=False
TMPDIR = 'tmp'

# Supported sites
supported_boards = ['2chan',
                    '4chan',
                    '4chanarchive',
                    'iichan',
                    'wakachan']

def usage():
    print "\nUsage:\n\tpython getter.py [options] [thread url]\n"

def processUrl(url):
    # Returns a tuple of the thread id and grepstring
    if url.find('archive') != -1:
        handler = FourChanArchiveHandler(url)   

    elif url.find('4chan') != -1:
        handler = FourChanHandler(url)

    elif url.find('2chan') != -1:
        handler = TwoChanHandler(url)
   
    elif url.find('wakachan') != -1:
        handler = WakaChanHandler(url)

    elif url.find('iichan') != -1:
        handler = IiChanHandler(url)

    else:
        print "Specified URL appears does not appear to be valid. Supported sites:"
        for board in supported_boards:
            print board
        sys.exit(2)

    print "Downloading %s thread id %d\ngrepstring is: ***%s***" % (handler.siteName, handler.threadId, handler.grepstring)
    return handler

def dispatch(url):
    handler = processUrl(url)
    handler.makeImageList()

    # TODO
    # For now, do this here since each run will grab one thread.
    # This should be moved to the handler's init once this becomes
    #   a service to run at intervals.
    #if not os.path.exists('%s' % handler.threadId):
    #    os.makedirs(str(handler.threadId))
    
    if DEBUG:
        print handler.imageLinks
    else:
        handler.download()
        #os.system("wget -O- \"%s\" | egrep %s -o | sort -u | xargs wget -nd --continue --wait 2" % (handler.url, handler.grepString)) 

def main():
    # Create temp directory if it doesn't exist
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dh",["help"])
    except getopt.error as exc:
        print "Syntax error %s" % exc
        usage()
        sys.exit(2)

    except Exception as exc:
        print exc
        usage()
        sys.exit(2)

    for opt in opts:
        if opt[0] == '-h':
            usage()
            sys.exit(2)
        
        elif opt[0] == '-d':
            global DEBUG
            DEBUG=True

    if len(args) < 1:
        raise Exception, "Need at least one argument!"

    for arg in args:
        #print arg
        dispatch(arg)

if __name__ == "__main__":
    main()

