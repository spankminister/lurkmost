#!/usr/bin/python
import os
import sys
import getopt
import re

# Globals
DEBUG=False

# Supported sites
supported_boards = ['4chan',
                    '4chanarchive',
                    'wakachan']

#TODO: allow wait to be specified
#TODO: output to tempfile, grep or re search file

def usage():
    print "\nUsage:\n\tpython getter.py [options] [thread url]\n"

def processUrl(url):
    # Returns a tuple of the thread id and grepstring
    if url.find('archive') != -1:
        # thread url is of form: http://4chanarchive.org/brchive/dspl_thread.php5?thread_id=21048406&x=Space+Ghost+Is+Back+On+The+Air2C+Due+To+A+TechnicalityTimewarp
        restring = "thread_id=[0-9]+"
        r = re.compile(restring)
        match = r.search(url)

        siteName = "4chanarchive"
        grepstring = "'http://4chanarchive.org/images/[a-z0-9]+/[a-z0-9]+/([0-9]*).(jpg|png|gif)'"
        threadId = int(url[match.start()+10:match.end()])

    elif url.find('4chan') != -1:
        # thread url is of form: http://boards.4chan.org/co/res/21649743
        siteName = "4chan"
        resting = "res/[0-9]+"
        grepstring = "'http://images.4chan.org/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"
   
    elif url.find('wakachan') != -1:
        # thread url is of form: http://www.wakachan.org/yuu/res/8733.html
        siteName = "wakachan"
        restring = "res/[0-9]"
        grepstring = "'http://wakachan.org/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"
        # http://wakachan.org/yuu/res/7182.html
        # http://wakachan.org/yuu/src/1255816373491.jpg
        # wget -O- http://wakachan.org/yuu/res/7182.html | egrep "/[a-z]+/res/([0-9]*).(jpg|png|gif)" > out.txt
        # blarg, this all may show up on the same line, and need to be parsed out further?

    else:
        print "Specified URL appears does not appear to be valid. Supported sites:"
        for board in supported_boards:
            print board
        sys.exit(2)

    retTuple = (siteName, threadId, grepstring)
    print "Downloading %s thread id %d\ngrepstring is: ***%s***" % retTuple
    return retTuple

def dispatch(url):
    siteName, threadId, grepString = processUrl(url)
    #grepString = getGrepString(url)
    #threadname = getThreadName(url)

    os.system("wget -O- \"%s\" | egrep %s -o | sort -u | xargs wget -nd --continue --wait 2" % (url, grepString)) 

    # TODO: if debug, do this instead
    #print grepstring
    #os.system("wget -O- \"%s\" | egrep %s -o | sort -u | xargs wget -nd --continue --wait 2" % (url, grepstring))

def main():
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
        print arg
        dispatch(arg)

if __name__ == "__main__":
    main()

