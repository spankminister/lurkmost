#!/usr/bin/python
import os
import sys
import getopt

#TODO: allow wait to be specified


def dispatch(url):
    if url.find('archive') != -1:
        print "Downloading 4chanarchive.org thread"
        grepstring = "'http://4chanarchive.org/images/[a-z0-9]+/[a-z0-9]+/([0-9]*).(jpg|png|gif)'"

    elif url.find('4chan') != -1:
        print "Downloading 4chan.org thread"
        grepstring = "'http://images.4chan.org/[a-z0-9]+/src/([0-9]*).(jpg|png|gif)'"

    os.system("wget -O- \"%s\" | egrep %s -o | sort -u | xargs wget -nd --continue --wait 2" % (url, grepstring)) 

    # TODO: if debug, do this instead
    #print grepstring
    #os.system("wget -O- \"%s\" | egrep %s -o | sort -u | xargs wget -nd --continue --wait 2" % (url, grepstring))

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h",["help"])
    except getopt.error:
        print "Error"
        sys.exit(2)

    for arg in args:
        print arg
        dispatch(arg)

if __name__ == "__main__":
    main()

